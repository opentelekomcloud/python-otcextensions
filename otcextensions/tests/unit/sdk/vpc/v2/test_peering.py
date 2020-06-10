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
from keystoneauth1 import adapter

import copy
import mock

from openstack.tests.unit import base
from otcextensions.sdk.vpc.v2 import peering


IDENTIFIER = 'ID'
EXAMPLE = {
    "name": "test",
    "id": "22b76469-08e3-4937-8c1d-7aad34892be1",
    "request_vpc_info": {
        "vpc_id": "9daeac7c-a98f-430f-8e38-67f9c044e299",
        "tenant_id": "f65e9ebc-ed5d-418b-a931-9a723718ba4e"
    },
    "accept_vpc_info": {
        "vpc_id": "f583c072-0bb8-4e19-afb2-afb7c1693be5",
        "tenant_id": "f65e9ebc-ed5d-418b-a931-9a723718ba4e"
    },
    "status": "ACTIVE"
}


class TestPeering(base.TestCase):

    def setUp(self):
        super(TestPeering, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = peering.Peering()
        self.assertEqual('peering', sot.resource_key)
        self.assertEqual('peerings', sot.resources_key)
        path = '/vpc/peerings'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = peering.Peering(**EXAMPLE)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['request_vpc_info'], sot.request_vpc_info)
        self.assertEqual(EXAMPLE['accept_vpc_info'], sot.accept_vpc_info)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)

    def test_approval(self):
        sot = peering.Peering(id=IDENTIFIER)

        resp = mock.Mock()
        resp.body = {
            "name": "test",
            "id": "22b76469-08e3-4937-8c1d-7aad34892be1",
            "request_vpc_info": {
                "vpc_id": "9daeac7c-a98f-430f-8e38-67f9c044e299",
                "tenant_id": "f65e9ebc-ed5d-418b-a931-9a723718ba4e"
            },
            "accept_vpc_info": {
                "vpc_id": "f583c072-0bb8-4e19-afb2-afb7c1693be5",
                "tenant_id": "f65e9ebc-ed5d-418b-a931-9a723718ba4e"
            },
            "status": "REJECTED"
        }
        resp.json = mock.Mock(return_value=copy.deepcopy(resp.body))
        resp.headers = {}
        resp.status_code = 200
        self.sess.put.return_value = resp

        approval_resp = sot.approval(self.sess, 'reject')
        self.sess.put.assert_called_with(
            'vpc/peerings/ID/reject'
        )
        self.assertEqual(resp.body['name'], approval_resp.name)
        self.assertEqual(resp.body['id'], approval_resp.id)
