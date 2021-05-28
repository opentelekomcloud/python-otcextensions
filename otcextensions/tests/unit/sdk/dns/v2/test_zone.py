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
import mock

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.dns.v2 import zone


FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "id": FAKE_ID,
    "name": "example.com.",
    "description": "This is an example zone.",
    "email": "xx@example.com",
    "ttl": 300,
    "serial": 0,
    "masters": [],
    "status": "ACTIVE",
    "links": {
        "self": "https://Endpoint/v2/zones/ff8080825b8fc86c015b94bc6f8712c3"
    },
    "pool_id": "ff8080825ab738f4015ab7513298010e",
    "project_id": "e55c6f3dc4e34c9f86353b664ae0e70c",
    "zone_type": "private",
    "created_at": "2017-04-22T08:17:08.997",
    "updated_at": "2017-04-22T08:17:09.997",
    "record_num": 2,
    "routers": [
        {
            "status": "ACTIVE",
            "router_id": "19664294-0bf6-4271-ad3a-94b8c79c6558",
            "router_region": "xx"
        },
        {
            "status": "ACTIVE",
            "router_id": "f0791650-db8c-4a20-8a44-a06c6e24b15b",
            "router_region": "xx"
        }
    ]

}


class TestZone(base.TestCase):

    def setUp(self):
        super(TestZone, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

    def test_basic(self):
        sot = zone.Zone()

        self.assertEqual('/zones', sot.base_path)
        self.assertEqual('zones', sot.resources_key)
        self.assertIsNone(sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):

        sot = zone.Zone(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['email'], sot.email)
        self.assertEqual(EXAMPLE['ttl'], sot.ttl)
        self.assertEqual(EXAMPLE['serial'], sot.serial)
        self.assertEqual(EXAMPLE['masters'], sot.masters)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['pool_id'], sot.pool_id)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['zone_type'], sot.zone_type)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
        self.assertEqual(EXAMPLE['record_num'], sot.record_num)
        self.assertEqual(len(EXAMPLE['routers']), len(sot.routers))

    def test_associate_router(self):
        sot = zone.Zone(**EXAMPLE)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot.associate_router(
            self.sess, router_id=1, router_region='a'
        )

        self.sess.post.assert_called_once_with(
            'zones/%s/associaterouter' % FAKE_ID,
            json={'router': {'router_id': 1, 'router_region': 'a'}}
        )

    def test_disassociate_router(self):
        sot = zone.Zone(**EXAMPLE)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot.disassociate_router(
            self.sess, router_id=1
        )

        self.sess.post.assert_called_once_with(
            'zones/%s/disassociaterouter' % FAKE_ID,
            json={'router': {'router_id': 1}}
        )
