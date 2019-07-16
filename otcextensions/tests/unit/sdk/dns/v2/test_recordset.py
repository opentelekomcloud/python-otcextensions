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

from otcextensions.sdk.dns.v2 import recordset


FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "id": FAKE_ID,
    "name": "example.com.",
    "type": "SOA",
    "ttl": 300,
    "records": [
        "ns1.hotrot.de. xx.example.com. (1 7200 900 1209600 300)"
    ],
    "status": "ACTIVE",
    "links": {
        "self": "some_link"
    },
    "zone_id": "2c9eb155587194ec01587224c9f90149",
    "zone_name": "example.com.",
    "create_at": "2016-11-17T11:56:03.439",
    "update_at": "2016-11-17T12:56:03.827",
    "default": True,
    "project_id": "e55c6f3dc4e34c9f86353b664ae0e70c"

}


class TestRecordSet(base.TestCase):

    def test_basic(self):
        sot = recordset.Recordset()

        self.assertEqual('/zones/%(zone_id)s/recordsets', sot.base_path)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):

        sot = recordset.Recordset(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['ttl'], sot.ttl)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['zone_id'], sot.zone_id)
        self.assertEqual(EXAMPLE['create_at'], sot.created_at)
        self.assertEqual(EXAMPLE['update_at'], sot.updated_at)
