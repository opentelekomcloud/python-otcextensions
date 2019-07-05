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
import time
import calendar
from openstack import format


class YNBool(format.Formatter):
    @classmethod
    def deserialize(cls, value):
        """Convert a boolean string to a boolean"""
        if isinstance(value, bool):
            return value
        expr = str(value).lower()
        if "y" == expr:
            return True
        elif "n" == expr:
            return False
        else:
            raise ValueError("Unable to deserialize boolean string: %s"
                             % value)

    @classmethod
    def serialize(cls, value):
        """Convert a boolean to a boolean string"""
        if value in ["Y", "N", "y", "n"]:
            return str(value).upper()
        if isinstance(value, bool):
            if value:
                return "Y"
            else:
                return "N"
        else:
            raise ValueError("Unable to serialize boolean string: %s"
                             % value)


class Bool_10(format.Formatter):
    @classmethod
    def deserialize(cls, value):
        """Convert a boolean string to a boolean"""
        if isinstance(value, bool):
            return value
        expr = str(value).lower()
        if "1" == expr:
            return True
        elif "0" == expr:
            return False
        else:
            raise ValueError("Unable to deserialize boolean string: %s"
                             % value)

    @classmethod
    def serialize(cls, value):
        """Convert a boolean to a boolean string"""
        if value in ["1", "0"]:
            return str(value).upper()
        if isinstance(value, bool):
            if value:
                return "1"
            else:
                return "0"
        else:
            raise ValueError("Unable to serialize boolean string: %s"
                             % value)


class BoolStr_1(format.BoolStr):
    """Deserialize bool, which can be either bool or string
    """

    @classmethod
    def deserialize(cls, value):
        """Convert a boolean string to a boolean"""
        if isinstance(value, bool):
            return value
        expr = str(value).lower()
        if "true" == expr:
            return True
        elif "false" == expr:
            return False
        else:
            raise ValueError("Unable to deserialize boolean string: %s"
                             % value)


class ListRef(format.Formatter):
    """A formatter used to serialize/deserialize list reference

    [{"id": "any-id"}] <-> ["any-id"], for example.
    """

    @classmethod
    def deserialize(cls, value):
        """Convert a list primitive to list reference"""
        if isinstance(value, list):
            return [item["id"] for item in value]
        else:
            raise ValueError("Unable to deserialize list reference: %s"
                             % value)

    @classmethod
    def serialize(cls, value):
        """Convert list reference to list primitive"""
        if isinstance(value, list):
            return [{"id": item} for item in value]
        else:
            raise ValueError("Unable to serialize list reference: %s"
                             % value)


class TimeTMsStr(format.Formatter):

    @classmethod
    def deserialize(cls, value):
        """Convert a time_t with msec precision to ISO8601"""
        _time = time.gmtime(value / 1000)
        # Embed MS placeholder into the format string directly
        _format = '%Y-%m-%dT%H:%M:%S.{ms}+00:00'
        return time.strftime(_format, _time).format(
            ms=int(value % 1000))

    @classmethod
    def serialize(cls, value):
        """Convert ISO8601 to time_t with ms"""
        if isinstance(value, str):
            _time_t = None
            try:
                _time_t = time.strptime(value, '%Y-%m-%dT%H:%M:%S+00:00')
            except ValueError:
                _time_t = time.strptime(value, '%Y-%m-%dT%H:%M:%S')
            if _time_t:
                return calendar.timegm(_time_t) * 1000
            else:
                raise ValueError("Unable to parse time reference: %s"
                                 % value)
        elif isinstance(value, int):
            raise value
        else:
            raise ValueError("Unable to serialize list reference: %s"
                             % value)
