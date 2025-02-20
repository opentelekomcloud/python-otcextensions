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
from otcextensions.sdk.apig.v2 import api

EXAMPLE = {
    "group_id": "id",
    "name": "test_api_001",
    "auth_type": "IAM",
    "backend_type": "HTTP",
    "req_protocol": "HTTP",
    "req_uri": "/test/http",
    "remark": "Mock backend API",
    "type": 2,
    "req_method": "GET",
    "result_normal_sample": "Example success response",
    "result_failure_sample": "Example failure response",
    "tags": ["httpApi"],
    "backend_api": {
        "req_protocol": "HTTP",
        "req_method": "GET",
        "req_uri": "/test/benchmark",
        "timeout": 5000,
        "retry_count": "-1",
        "url_domain": "192.168.189.156:12346"
    },
}


class TestApi(base.TestCase):

    def test_basic(self):
        sot = api.Api()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/apis',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)
        self.assertEqual('apis', sot.resources_key)

    def test_make_it(self):
        sot = api.Api(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['group_id'], sot.group_id)
        self.assertEqual(EXAMPLE['auth_type'], sot.auth_type)
        self.assertEqual(EXAMPLE['backend_type'], sot.backend_type)
        self.assertEqual(EXAMPLE['req_protocol'], sot.req_protocol)
