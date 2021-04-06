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
import uuid
from openstack.tests.unit import base

from otcextensions.sdk.vpcep.v1 import endpoint_service


ID = uuid.uuid4().hex
DOMAIN_ID = uuid.uuid4().hex

EXAMPLE = {
    "id": ID,
    "status": "accepted",
    "marker_id": 16777510,
    "domain_id": DOMAIN_ID,
    "created_at": "2018-09-17T11:10:11Z",
    "updated_at": "2018-09-17T11:10:12Z"
}

EXAMPLE_CONNECTIONS = {
    "connections":
    [
        {
            "id": ID,
            "status": "accepted",
            "marker_id": 16777510,
            "domain_id": DOMAIN_ID,
            "created_at": "2018-09-17T11:10:11Z",
            "updated_at": "2018-09-17T11:10:12Z"
        },
        {
            "id": ID,
            "status": "accepted",
            "marker_id": 16777513,
            "domain_id": DOMAIN_ID,
            "created_at": "2018-09-17T07:28:56Z",
            "updated_at": "2018-09-17T07:28:58Z"
        }
    ],
    "total_count": 2
}


class TestEndpointConnection(base.TestCase):

    def test_basic(self):
        sot = endpoint_service.Connection()
        self.assertEqual('connections', sot.resources_key)
        path = '/vpc-endpoint-services/%(endpoint_service_id)s/connections'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = endpoint_service.Connection(**EXAMPLE)
        for key, value in EXAMPLE.items():
            self.assertEqual(getattr(sot, key), value)


class TestEndpointManageConnection(base.TestCase):

    def test_basic(self):
        sot = endpoint_service.ManageConnection()
        path = ('/vpc-endpoint-services/%(endpoint_service_id)s'
                '/connections/action')
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = endpoint_service.ManageConnection(**EXAMPLE_CONNECTIONS)
        connections_list = EXAMPLE_CONNECTIONS['connections']
        for i in range(len(connections_list)):
            for key, value in connections_list[i].items():
                self.assertEqual(getattr(sot.connections[i], key), value)
