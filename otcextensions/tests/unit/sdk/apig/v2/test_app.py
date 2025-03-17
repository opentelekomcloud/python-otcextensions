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
from otcextensions.sdk.apig.v2 import app


EXAMPLE_APP = {
    'id': 'app-12345',
    'gateway_id': 'gateway-67890',
    'name': 'Test App',
    'remark': 'This is a test app',
    'app_key': 'key-abcdef',
    'app_secret': 'secret-12345',
    'creator': 'user-1',
    'update_time': '2025-02-07T12:30:00Z',
    'register_time': '2025-02-07T12:00:00Z',
    'status': 1,
    'app_type': 'web',
    'roma_app_type': 'roma-type-1',
    'bind_num': 10
}


class TestApp(base.TestCase):

    def test_basic(self):
        sot = app.App()
        self.assertEqual('/apigw/instances/%(gateway_id)s/apps', sot.base_path)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertEqual('apps', sot.resources_key)

    def test_make_it(self):
        sot = app.App(**EXAMPLE_APP)
        self.assertEqual(EXAMPLE_APP['id'], sot.id)
        self.assertEqual(EXAMPLE_APP['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_APP['name'], sot.name)
        self.assertEqual(EXAMPLE_APP['remark'], sot.remark)
        self.assertEqual(EXAMPLE_APP['app_key'], sot.app_key)
        self.assertEqual(EXAMPLE_APP['app_secret'], sot.app_secret)
        self.assertEqual(EXAMPLE_APP['creator'], sot.creator)
        self.assertEqual(EXAMPLE_APP['update_time'], sot.update_time)
        self.assertEqual(EXAMPLE_APP['register_time'], sot.register_time)
        self.assertEqual(EXAMPLE_APP['status'], sot.status)
        self.assertEqual(EXAMPLE_APP['app_type'], sot.app_type)
        self.assertEqual(EXAMPLE_APP['roma_app_type'], sot.roma_app_type)
        self.assertEqual(EXAMPLE_APP['bind_num'], sot.bind_num)
