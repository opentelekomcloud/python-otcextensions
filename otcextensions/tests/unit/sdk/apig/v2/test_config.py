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
from otcextensions.sdk.apig.v2 import config

EXAMPLE_CONFIG = {
    'config_id': 'conf-123',
    'config_name': 'flow_control',
    'config_value': '1000',
    'config_time': '2025-01-01T12:00:00Z',
    'remark': 'Maximum requests per second',
    'used': '350'
}


class TestConfig(base.TestCase):

    def test_basic(self):
        sot = config.Config()
        self.assertEqual('/apigw/instance/configs', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertEqual('configs', sot.resources_key)

    def test_make_it(self):
        sot = config.Config(**EXAMPLE_CONFIG)
        self.assertEqual('conf-123', sot.config_id)
        self.assertEqual('flow_control', sot.config_name)
        self.assertEqual('1000', sot.config_value)
        self.assertEqual('2025-01-01T12:00:00Z', sot.config_time)
        self.assertEqual('Maximum requests per second', sot.remark)
        self.assertEqual('350', sot.used)
