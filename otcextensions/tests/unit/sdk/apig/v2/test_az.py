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
from otcextensions.sdk.apig.v2 import az


EXAMPLE_AZ = {
    'name': 'eu-de-1a',
    'id': 'az-12345',
    'code': 'eu-de-1a',
    'port': 443,
    'local_name': {'en_us': 'Europe Germany AZ1', 'zh_cn': '欧洲德国AZ1'},
    'specs': {'max_bandwidth': 1000, 'min_bandwidth': 50}
}


class TestAZ(base.TestCase):

    def test_basic(self):
        sot = az.AZ()
        self.assertEqual('/apigw/available-zones', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertEqual('AZ', sot.resource_name)
        self.assertEqual('available_zones', sot.resources_key)

    def test_make_it(self):
        sot = az.AZ(**EXAMPLE_AZ)
        self.assertEqual(EXAMPLE_AZ['name'], sot.name)
        self.assertEqual(EXAMPLE_AZ['id'], sot.id)
        self.assertEqual(EXAMPLE_AZ['code'], sot.code)
        self.assertEqual(EXAMPLE_AZ['port'], sot.port)
        self.assertEqual(EXAMPLE_AZ['local_name']['en_us'], sot.local_name.en_us)
        self.assertEqual(EXAMPLE_AZ['local_name']['zh_cn'], sot.local_name.zh_cn)
        self.assertEqual(EXAMPLE_AZ['specs'], sot.specs)
