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

import copy
import mock

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

DATA = {
    "links": {
        "self": "https://dns.eu-de.otc.t-systems.com/v2/zones/ff80808261418b240161d163e39e11a0/recordsets"
    },
    "recordsets": [
        {
            "id": "ff80808261418b240161d163e39e11a1",
            "name": "prod.otc.appagile.",
            "description": None,
            "type": "SOA",
            "ttl": 300,
            "records": [
                "ns1.open-telekom-cloud.com. dl-otc-domains.telekom.de. (1 7200 900 1209600 300)"
            ],
            "status": "ACTIVE",
            "zone_id": "ff80808261418b240161d163e39e11a0",
            "zone_name": "prod.otc.appagile.",
            "create_at": "2018-02-26T09:13:59.954",
            "update_at": None,
            "default": True,
            "project_id": "09781c0169b34685ba2c2f38f45e96e1",
            "links": {
                "self": "https://dns.eu-de.otc.t-systems.com/v2/zones/ff80808261418b240161d163e39e11a0/recordsets/ff80808261418b240161d163e39e11a1"
            }
        },
        {
            "id": "ff80808261418b240161d163e39e11a3",
            "name": "prod.otc.appagile.",
            "description": None,
            "type": "NS",
            "ttl": 172800,
            "records": [
                "ns1.open-telekom-cloud.com."
            ],
            "status": "ACTIVE",
            "zone_id": "ff80808261418b240161d163e39e11a0",
            "zone_name": "prod.otc.appagile.",
            "create_at": "2018-02-26T09:13:59.954",
            "update_at": None,
            "default": True,
            "project_id": "09781c0169b34685ba2c2f38f45e96e1",
            "links": {
                "self": "https://dns.eu-de.otc.t-systems.com/v2/zones/ff80808261418b240161d163e39e11a0/recordsets/ff80808261418b240161d163e39e11a3"
            }
        },
        {
            "id": "ff80808261418b240161d164409a11a7",
            "name": "satellite.central.prod.otc.appagile.",
            "description": None,
            "type": "A",
            "ttl": 300,
            "records": [
                "192.168.255.140"
            ],
            "status": "ACTIVE",
            "zone_id": "ff80808261418b240161d163e39e11a0",
            "zone_name": "prod.otc.appagile.",
            "create_at": "2018-02-26T09:14:23.766",
            "update_at": "2018-02-26T09:14:23.779",
            "default": False,
            "project_id": "09781c0169b34685ba2c2f38f45e96e1",
            "links": {
                "self": "https://dns.eu-de.otc.t-systems.com/v2/zones/ff80808261418b240161d163e39e11a0/recordsets/ff80808261418b240161d164409a11a7"
            }
        }
    ],
    "metadata": {
        "total_count": 7
    }
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

    def test_get_next_link(self):
        sot = recordset.Recordset.new()
        response = mock.Mock()
        response.status_code = 200
        uri = '/zones/ff80808272701cbe0172cbca17f91882/recordsets'
        data = copy.deepcopy(DATA)
        dict_marker = {'marker': 'ff80808261418b240161d164409a11a7'}
        marker = dict_marker.get("marker")
        limit = None
        total_yielded = 3
        result = sot._get_next_link(
            uri=uri,
            response=response,
            data=data,
            marker=marker,
            limit=limit,
            total_yielded=total_yielded
        )
        self.assertEqual(uri, result[0])
        self.assertEqual(dict_marker, result[1])
