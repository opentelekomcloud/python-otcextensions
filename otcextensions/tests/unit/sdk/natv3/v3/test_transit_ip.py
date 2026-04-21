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
from otcextensions.sdk.natv3.v3 import transit_ip

INSTANCE_ID = "c36a5fb7-3a71-4ed6-9bb1-9a7649d73b0e"

EXAMPLE = {
    "id": INSTANCE_ID,
    "project_id": "da261828016849188f4dcc2ef94d9da9",
    "network_interface_id": "7c5a3826-5b4c-44c6-a4aa-74f8249f61b5",
    "ip_address": "172.20.1.10",
    "gateway_id": "0adefb29-a6c2-48a5-8637-2be67fa03fec",
    "created_at": "2019-04-29T07:10:01",
    "updated_at": "2019-04-29T07:10:01",
    "tags": [
        {
            "key": "env",
            "value": "test",
        }
    ],
    "virsubnet_id": "95df1b88-d9bc-4edd-a808-a771dd4ded32",
    "status": "ACTIVE",
    "enterprise_project_id": "2759da7b-8015-404c-ae0a-a389007b0e2a",
}


class TestPrivateTransitIp(base.TestCase):

    def test_basic(self):
        sot = transit_ip.PrivateTransitIp()
        self.assertEqual("transit_ip", sot.resource_key)
        self.assertEqual("transit_ips", sot.resources_key)
        self.assertEqual("/private-nat/transit-ips", sot.base_path)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = transit_ip.PrivateTransitIp(**EXAMPLE)
        self.assertEqual(EXAMPLE["id"], sot.id)
        self.assertEqual(EXAMPLE["project_id"], sot.project_id)
        self.assertEqual(EXAMPLE["network_interface_id"], sot.network_interface_id)
        self.assertEqual(EXAMPLE["ip_address"], sot.ip_address)
        self.assertEqual(EXAMPLE["gateway_id"], sot.gateway_id)
        self.assertEqual(EXAMPLE["created_at"], sot.created_at)
        self.assertEqual(EXAMPLE["updated_at"], sot.updated_at)
        self.assertEqual(1, len(sot.tags))
        self.assertIsInstance(sot.tags[0], transit_ip.TransitIpTag)
        self.assertEqual(EXAMPLE["tags"][0]["key"], sot.tags[0].key)
        self.assertEqual(EXAMPLE["tags"][0]["value"], sot.tags[0].value)
        self.assertEqual(EXAMPLE["virsubnet_id"], sot.virsubnet_id)
        self.assertEqual(EXAMPLE["status"], sot.status)
        self.assertEqual(EXAMPLE["enterprise_project_id"], sot.enterprise_project_id)
