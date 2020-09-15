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

from otcextensions.sdk.vpcep.v1 import endpoint


EXAMPLE = {
    "id": "4189d3c2-8882-4871-a3c2-d380272eed83",
    "service_type": "interface",
    "marker_id": 322312312312,
    "status": "creating",
    "vpc_id": "4189d3c2-8882-4871-a3c2-d380272eed83",
    "enable_dns": False,
    "endpoint_service_name": "test123",
    "endpoint_service_id": "test123",
    "project_id": "6e9dfd51d1124e8d8498dce894923a0d",
    "whitelist": [
        "127.0.0.1"
    ],
    "enable_whitelist": True,
    "created_at": "2018-01-30T07:42:01.174",
    "updated_at": "2018-01-30T07:42:01.174",
    "tags": [
        {
            "key": "test1",
            "value": "test1"
        }
    ]
}


class TestEndpoint(base.TestCase):

    def test_basic(self):
        sot = endpoint.Endpoint()
        self.assertEqual('endpoints', sot.resources_key)
        path = '/vpc-endpoints'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = endpoint.Endpoint(**EXAMPLE)
        for key in EXAMPLE.keys():
            if key == 'tags':
                tags_list = EXAMPLE[key]
                for i in range(len(tags_list)):
                    for sub_key in tags_list[i].keys():
                        self.assertEqual(tags_list[i][sub_key],
                                         getattr(sot.tags[i], sub_key))
            else:
                self.assertEqual(EXAMPLE[key], getattr(sot, key))
