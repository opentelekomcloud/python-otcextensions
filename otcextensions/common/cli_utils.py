#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
"""Formatters for cli outputs"""
import datetime

import yaml
from cliff import columns as cliff_columns


class literal(str):
    pass


def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')


yaml.add_representer(literal, literal_presenter)


def scrub_dict(d):
    new_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = scrub_dict(v)
        if v not in ('', None, {}):
            new_dict[k] = v
    return new_dict


def wrap_text(s):
    length = 100
    if isinstance(s, str) and len(s) >= length:
        return '\n'.join([s[i:i + length] for i in range(0, len(s), length)])
    return s


class WrapText(cliff_columns.FormattableColumn):
    def human_readable(self):
        return wrap_text(self._value)


class UnixTimestampFormatter(cliff_columns.FormattableColumn):
    """Generate a formatted string of a hostname."""

    def human_readable(self):
        if self._value is None:
            return ''

        # Convert Unix timestamp to GMT+1
        gmt_offset = 1
        if not isinstance(self._value, int):
            self._value = int(self._value) / 1000
        else:
            self._value = self._value / 1000
        timestamp = datetime.datetime.fromtimestamp(self._value)
        timezone_offset = datetime.timezone(
            datetime.timedelta(hours=gmt_offset)
        )
        timestamp_gmt = timestamp.astimezone(timezone_offset)

        # Format the timestamp as a string with the timezone offset
        timezone_offset_str = timestamp_gmt.strftime('%z')
        timezone_offset_formatted = (
            f'GMT{timezone_offset_str[:3]}:{timezone_offset_str[3:]}'
        )
        return (
            timestamp_gmt.strftime('%Y-%m-%d %H:%M:%S ')
            + timezone_offset_formatted
        )
        # Format GMT+1 timestamp as string


class YamlFormat(cliff_columns.FormattableColumn):
    def remove_null_values(self, data):
        if isinstance(data, dict):
            if (
                'record_delimiter' in data.keys()
                and '\n' in data['record_delimiter']
            ):
                data['record_delimiter'] = '\\n'
            return {
                k: self.remove_null_values(v)
                for k, v in data.items()
                if v is not None
            }
        elif isinstance(data, list):
            return [self.remove_null_values(v) for v in data if v is not None]
        else:
            return data

    def human_readable(self):
        data = self._value
        if type(data) not in (dict, list):
            data = self._value.to_dict(computed=False)
        data = self.remove_null_values(data)
        return yaml.dump(data, width=100)
