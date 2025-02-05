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
from otcextensions.sdk.apig.v2 import apienvironment as env

EXAMPLE_ENVIRONMENT = {
    'name': 'test-environment',
    'id': 'env-12345',
    'remark': 'This is a test environment',
    'create_time': '2024-02-05T12:34:56Z',
}


class TestApiEnvironment(base.TestCase):

    def test_basic(self):
        sot = env.ApiEnvironment()
        self.assertEqual('/apigw/instances/%(gateway_id)s/envs', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertEqual('envs', sot.resources_key)

    def test_make_it(self):
        sot = env.ApiEnvironment(**EXAMPLE_ENVIRONMENT)
        self.assertEqual(EXAMPLE_ENVIRONMENT['name'], sot.name)
        self.assertEqual(EXAMPLE_ENVIRONMENT['id'], sot.id)
        self.assertEqual(EXAMPLE_ENVIRONMENT['remark'], sot.remark)
        self.assertEqual(EXAMPLE_ENVIRONMENT['create_time'], sot.create_time)
