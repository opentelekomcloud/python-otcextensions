# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import proxy
from typing import Optional
import requests


def normalize_metric_name(name):
    name = name.replace('.', '_')
    name = name.replace(':', '_')
    return name


class Proxy(proxy.Proxy):

    def _report_stats_statsd(
            self,
            response: Optional[requests.Response],
            url: Optional[str] = None,
            method: Optional[str] = None,
            exc: Optional[BaseException] = None,
    ) -> None:
        if not self._statsd_prefix:
            return None

        if not self._statsd_client:
            return None

        try:
            if response is not None and not url:
                url = response.request.url
            if response is not None and not method:
                method = response.request.method

            # narrow types
            assert url is not None
            assert method is not None
            assert self.service_type is not None

            name_parts = [
                normalize_metric_name(f)
                for f in self._extract_name(
                    url, self.service_type, self.session.get_project_id()
                )
            ]
            key = '.'.join(
                [
                    self._statsd_prefix,
                    normalize_metric_name(self.service_type),
                    method,
                    '_'.join(name_parts),
                ]
            )
            with self._statsd_client.pipeline() as pipe:
                if response is not None:
                    duration = int(response.elapsed.total_seconds() * 1000)
                    metric_name = f'{key}.{str(response.status_code)}'
                    pipe.timing(metric_name, duration)
                    pipe.incr(metric_name)
                    if duration > 1000:
                        pipe.incr(f'{key}.over_1000')
                elif exc is not None:
                    pipe.incr(f'{key}.failed')
                pipe.incr(f'{key}.attempted')
        except Exception:
            # We do not want errors in metric reporting ever break client
            self.log.exception("Exception reporting metrics")

    def _report_stats_influxdb(
            self,
            response: Optional[requests.Response],
            url: Optional[str] = None,
            method: Optional[str] = None,
            exc: Optional[BaseException] = None,
    ) -> None:
        if not self._influxdb_client:
            return None

        if not self._influxdb_config:
            return None

        # NOTE(gtema): status_code is saved both as tag and field to give
        # ability showing it as a value and not only as a legend.
        # However Influx is not ok with having same name in tags and fields,
        # therefore use different names.
        if response is not None and not url:
            url = response.request.url
        if response is not None and not method:
            method = response.request.method
        tags = {
            'method': method,
            'name': '_'.join(
                [
                    normalize_metric_name(f)
                    for f in self._extract_name(
                        url, self.service_type,
                        self.session.get_project_id()
                    )
                ]
            ),
        }
        fields = {'attempted': 1}
        if response is not None:
            fields['duration'] = int(response.elapsed.total_seconds() * 1000)
            tags['status_code'] = str(response.status_code)
            # Note(gtema): emit also status_code as a value (counter)
            fields[str(response.status_code)] = 1
            fields[f'{method}.{response.status_code}'] = 1
            # Note(gtema): status_code field itself is also very helpful on the
            # graphs to show what was the code, instead of counting its
            # occurences
            fields['status_code_val'] = response.status_code
        elif exc:
            fields['failed'] = 1
        if 'additional_metric_tags' in self._influxdb_config:
            tags.update(self._influxdb_config['additional_metric_tags'])
        measurement = (
            self._influxdb_config.get('measurement', 'openstack_api')
            if self._influxdb_config
            else 'openstack_api'
        )
        # Note(gtema) append service name into the measurement name
        measurement = f'{measurement}.{self.service_type}'
        data = [{'measurement': measurement, 'tags': tags, 'fields': fields}]
        try:
            self._influxdb_client.write_points(data)
        except Exception:
            self.log.exception('Error writing statistics to InfluxDB')
