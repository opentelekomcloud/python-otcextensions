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
from otcextensions.sdk.apig.v2 import appcode


EXAMPLE_APP_CODE = {
    'gateway_id': 'gateway-67890',
    'app_id': 'app-12345',
    'app_code': 'code-12345',
    'id': 'code-1',
    'create_time': '2025-02-07T12:45:00Z'
}


class TestAppCode(base.TestCase):

    def test_basic(self):
        sot = appcode.AppCode()
        self.assertEqual('/apigw/instances/%(gateway_id)s/apps/'
                         '%(app_id)s/app-codes',
                         sot.base_path)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = appcode.AppCode(**EXAMPLE_APP_CODE)
        self.assertEqual(EXAMPLE_APP_CODE['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_APP_CODE['app_id'], sot.app_id)
        self.assertEqual(EXAMPLE_APP_CODE['app_code'], sot.app_code)
        self.assertEqual(EXAMPLE_APP_CODE['id'], sot.id)
        self.assertEqual(EXAMPLE_APP_CODE['create_time'], sot.create_time)
