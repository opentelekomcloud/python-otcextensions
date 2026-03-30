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

from openstack.tests.unit import base
from otcextensions.common.utils import normalize_tags


class TestUtils(base.TestCase):

    def test_normalize_tags(self):
        tags = ["key1=value", "key2=", "key3"]

        verify_result = [
            {"key": "key1", "value": "value"},
            {"key": "key2", "value": ""},
            {"key": "key3", "value": ""},
        ]

        result = normalize_tags(tags)

        self.assertEqual(result, verify_result)
