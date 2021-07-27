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

from otcextensions.sdk.vlb.v3 import listener

EXAMPLE = {
    'loadbalancer_id': '',
    'protocol_port': 80,
    'protocol': 'TCP',
    'insert_headers': {'X-Forwarded-ELB-IP': True},
    'name': 'listener',
    'admin_state_up': True,
    'tags': [{
                "key": "test",
                "value": "api"
            }],
}


class TestLoadBalancer(base.TestCase):

    def test_basic(self):
        sot = listener.Listener()
        path = '/elb/listeners'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = listener.Listener(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['insert_headers'], sot.insert_headers)
        self.assertEqual(EXAMPLE['protocol_port'], sot.protocol_port)
        self.assertEqual(EXAMPLE['protocol'], sot.protocol)
