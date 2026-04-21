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
from otcextensions.sdk.natv3.v3 import snat

INSTANCE_ID = "8a522ff9-8158-494b-83cd-533b045700e6"

EXAMPLE = {
    "id": INSTANCE_ID,
    "project_id": "cfa563efb77d4b6d9960781d82530fd8",
    "description": "snat rule description",
    "gateway_id": "80da6f26-94eb-4537-97f0-5a56f4d04cfb",
    "cidr": "",
    "virsubnet_id": "95df1b88-d9bc-4edd-a808-a771dd4ded32",
    "transit_ip_associations": [
        {
            "transit_ip_id": "bbe7c2e7-3bad-445b-a067-b30acce66053",
            "transit_ip_address": "172.20.1.98",
        }
    ],
    "created_at": "2019-10-22T03:33:07",
    "updated_at": "2019-10-22T03:33:07",
    "enterprise_project_id": "2759da7b-8015-404c-ae0a-a389007b0e2a",
    "status": "ACTIVE",
}


class TestPrivateSnat(base.TestCase):

    def test_basic(self):
        sot = snat.PrivateSnat()
        self.assertEqual("snat_rule", sot.resource_key)
        self.assertEqual("snat_rules", sot.resources_key)
        self.assertEqual("/private-nat/snat-rules", sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = snat.PrivateSnat(**EXAMPLE)
        self.assertEqual(EXAMPLE["id"], sot.id)
        self.assertEqual(EXAMPLE["project_id"], sot.project_id)
        self.assertEqual(EXAMPLE["description"], sot.description)
        self.assertEqual(EXAMPLE["gateway_id"], sot.gateway_id)
        self.assertEqual(EXAMPLE["cidr"], sot.cidr)
        self.assertEqual(EXAMPLE["virsubnet_id"], sot.virsubnet_id)
        self.assertIsNone(sot.transit_ip_ids)
        self.assertEqual(1, len(sot.transit_ip_associations))
        self.assertIsInstance(sot.transit_ip_associations[0], snat.AssociatedTransitIp)
        self.assertEqual(
            EXAMPLE["transit_ip_associations"][0]["transit_ip_id"],
            sot.transit_ip_associations[0].transit_ip_id,
        )
        self.assertEqual(
            EXAMPLE["transit_ip_associations"][0]["transit_ip_address"],
            sot.transit_ip_associations[0].transit_ip_address,
        )
        self.assertEqual(EXAMPLE["created_at"], sot.created_at)
        self.assertEqual(EXAMPLE["updated_at"], sot.updated_at)
        self.assertEqual(EXAMPLE["enterprise_project_id"], sot.enterprise_project_id)
        self.assertEqual(EXAMPLE["status"], sot.status)
