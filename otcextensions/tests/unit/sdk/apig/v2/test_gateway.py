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
from otcextensions.sdk.apig.v2 import gateway

EXAMPLE = {
    'description': 'Test API Gateway',
    'maintain_begin': '22:00',
    'maintain_end': '02:00',
    'instance_name': 'test-gateway',
    'security_group_id': 'sg-12345',
    'vpcep_service_name': 'vpcep-test-service'
}


class TestGateway(base.TestCase):

    def test_basic(self):
        sot = gateway.Gateway()
        self.assertEqual('/apigw/instances', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = gateway.Gateway(**EXAMPLE)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['maintain_begin'], sot.maintain_begin)
        self.assertEqual(EXAMPLE['maintain_end'], sot.maintain_end)
        self.assertEqual(EXAMPLE['instance_name'], sot.instance_name)
        self.assertEqual(EXAMPLE['security_group_id'], sot.security_group_id)
        self.assertEqual(EXAMPLE['vpcep_service_name'], sot.vpcep_service_name)
