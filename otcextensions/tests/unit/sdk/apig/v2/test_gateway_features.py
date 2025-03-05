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
from otcextensions.sdk.apig.v2 import gateway_features

EXAMPLE = {
    "config": "on",
    "enable": True,
    "id": "db9a9260cd3e4a16a9b5747a65d3ffaa",
    "gateway_id": "eddc4d25480b4cd6b512f270a1b8b341",
    "name": "app_api_key",
    "updated_at": "2020-08-24T01:17:31.041984021Z"
}


class TestGatewayFeatures(base.TestCase):

    def test_basic(self):
        sot = gateway_features.GatewayFeatures()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/features',
            sot.base_path
        )
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)

    def test_make_it(self):
        sot = gateway_features.GatewayFeatures(**EXAMPLE)
        self.assertEqual(EXAMPLE['config'], sot.config)
        self.assertEqual(EXAMPLE['enable'], sot.enable)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
