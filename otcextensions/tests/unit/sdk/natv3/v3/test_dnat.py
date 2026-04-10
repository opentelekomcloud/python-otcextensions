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
from otcextensions.sdk.natv3.v3 import dnat

INSTANCE_ID = "24dd6bf5-48f2-4915-ad0b-5bb111d39c83"

EXAMPLE = {
    "id": INSTANCE_ID,
    "project_id": "da261828016849188f4dcc2ef94d9da9",
    "description": "aa",
    "gateway_id": "0adefb29-a6c2-48a5-8637-2be67fa03fec",
    "transit_ip_id": "3faa719d-6d18-4ccb-a5c7-33e65a09663e",
    "enterprise_project_id": "2759da7b-8015-404c-ae0a-a389007b0e2a",
    "network_interface_id": "dae9393a-b536-491c-a5a2-72edc1104707",
    "type": "COMPUTE",
    "protocol": "any",
    "internal_service_port": 0,
    "transit_service_port": 0,
    "private_ip_address": "192.168.1.72",
    "created_at": "2019-04-29T07:10:01",
    "updated_at": "2019-04-29T07:10:01",
    "status": "ACTIVE",
}


class TestPrivateDnat(base.TestCase):

    def test_basic(self):
        sot = dnat.PrivateDnat()
        self.assertEqual("dnat_rule", sot.resource_key)
        self.assertEqual("dnat_rules", sot.resources_key)
        self.assertEqual("/private-nat/dnat-rules", sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = dnat.PrivateDnat(**EXAMPLE)
        self.assertEqual(EXAMPLE["id"], sot.id)
        self.assertEqual(EXAMPLE["project_id"], sot.project_id)
        self.assertEqual(EXAMPLE["description"], sot.description)
        self.assertEqual(EXAMPLE["gateway_id"], sot.gateway_id)
        self.assertEqual(EXAMPLE["transit_ip_id"], sot.transit_ip_id)
        self.assertEqual(EXAMPLE["enterprise_project_id"], sot.enterprise_project_id)
        self.assertEqual(EXAMPLE["network_interface_id"], sot.network_interface_id)
        self.assertEqual(EXAMPLE["type"], sot.type)
        self.assertEqual(EXAMPLE["protocol"], sot.protocol)
        self.assertEqual(EXAMPLE["internal_service_port"], sot.internal_service_port)
        self.assertEqual(EXAMPLE["transit_service_port"], sot.transit_service_port)
        self.assertEqual(EXAMPLE["private_ip_address"], sot.private_ip_address)
        self.assertEqual(EXAMPLE["created_at"], sot.created_at)
        self.assertEqual(EXAMPLE["updated_at"], sot.updated_at)
        self.assertEqual(EXAMPLE["status"], sot.status)
