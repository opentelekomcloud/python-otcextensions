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

from otcextensions.sdk.dns.v2 import ptr


EXAMPLE = {
    "id": "region_id:c5504932-bf23-4171-b655-b87a6bc59334",
    "ptrdname": "www.example.com.",
    "description": "Description for this PTR record",
    "address": "10.154.52.138",
    "action": "CREATE",
    "ttl": 300,
    "status": "ACTIVE"
}


class TestPTR(base.TestCase):

    def test_basic(self):
        sot = ptr.PTR()

        self.assertEqual('/reverse/floatingips', sot.base_path)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertTrue(sot.allow_update)

    def test_make_it(self):

        sot = ptr.PTR(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['ptrdname'], sot.ptrdname)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['address'], sot.address)
        self.assertEqual(EXAMPLE['action'], sot.action)
        self.assertEqual(EXAMPLE['ttl'], sot.ttl)
        self.assertEqual(EXAMPLE['status'], sot.status)
