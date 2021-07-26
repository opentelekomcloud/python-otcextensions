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
from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.ces.v1 import _proxy
from otcextensions.sdk.ces.v1 import alarm
from otcextensions.sdk.ces.v1 import event_data
from otcextensions.sdk.ces.v1 import metric
from otcextensions.sdk.ces.v1 import metric_data
from otcextensions.sdk.ces.v1 import quota


class TestCesProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestCesProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestCesAlarm(TestCesProxy):
    def test_alarm_create(self):
        self.verify_create(self.proxy.create_alarm, alarm.Alarm,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_alarm_delete(self):
        self.verify_delete(self.proxy.delete_alarm,
                           alarm.Alarm, True)

    def test_alarm_get(self):
        self.verify_get(self.proxy.get_alarm, alarm.Alarm)

    def test_alarms(self):
        self.verify_list(self.proxy.alarms, alarm.Alarm)

    def test_update_alarm_enabled(self):
        self._verify(
            'otcextensions.sdk.ces.v1.alarm.Alarm.change_alarm_status',
            self.proxy.switch_alarm_state,
            method_args=["alarm"],
            expected_args=[self.proxy]
        )

    def test_alarm_find(self):
        self.verify_find(self.proxy.find_alarm, alarm.Alarm)


class TestCesEventData(TestCesProxy):
    def test_event_data(self):
        self.verify_list(self.proxy.event_data, event_data.EventData)


class TestCesMetric(TestCesProxy):
    def test_metrics(self):
        self.verify_list(self.proxy.metrics, metric.Metric)


class TestCesMetricData(TestCesProxy):
    def test_metric_data(self):
        self.verify_list(self.proxy.metric_data, metric_data.MetricData)


class TestCesQuota(TestCesProxy):
    def test_quotas(self):
        self.verify_list(self.proxy.quotas, quota.Quota)


class TestExtractName(TestCesProxy):

    def test_extract_name(self):

        self.assertEqual(
            ['discovery'],
            self.proxy._extract_name(
                '/', project_id='123')
        )
        self.assertEqual(
            ['discovery'],
            self.proxy._extract_name(
                '/V1.0/', project_id='123')
        )
        self.assertEqual(
            ['alarms'],
            self.proxy._extract_name(
                '/V1.0/123/alarms', project_id='123')
        )
        self.assertEqual(
            ['alarm'],
            self.proxy._extract_name(
                '/V1.0/123/alarms/some_id', project_id='123')
        )
        self.assertEqual(
            ['alarm', 'action'],
            self.proxy._extract_name(
                '/V1.0/123/alarms/some_id/action', project_id='123')
        )
        self.assertEqual(
            ['metrics'],
            self.proxy._extract_name(
                '/V1.0/123/metrics', project_id='123')
        )
        self.assertEqual(
            ['metric-data'],
            self.proxy._extract_name(
                '/V1.0/123/metric-data?a=b', project_id='123')
        )
        self.assertEqual(
            ['batch-query-metric-data'],
            self.proxy._extract_name(
                '/V1.0/123/batch-query-metric-data', project_id='123')
        )
        self.assertEqual(
            ['event-data'],
            self.proxy._extract_name(
                '/V1.0/123/event-data', project_id='123')
        )
        self.assertEqual(
            ['quotas'],
            self.proxy._extract_name(
                '/V1.0/123/quotas', project_id='123')
        )
