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

import mock

from openstack.tests.unit import base
from otcextensions.sdk.vpc.v1 import route


IDENTIFIER = 'ID'
EXAMPLE = {
    "type": "peering",
    "nexthop": "60c809cb-6731-45d0-ace8-3bf5626421a9",
    "destination": "192.168.200.0/24",
    "vpc_id": "ab78be2d-782f-42a5-aa72-35879f6890ff",
    "tenant_id": "6fbe9263116a4b68818cf1edce16bc4f",
    "id": "3d42a0d4-a980-4613-ae76-a2cddecff054"
}


class TestRoute(base.TestCase):

    def setUp(self):
        super(TestRoute, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = route.Route()
        self.assertEqual('route', sot.resource_key)
        self.assertEqual('routes', sot.resources_key)
        path = '/v2.0/vpc/routes'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        sot = route.Route(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['destination'], sot.destination)
        self.assertEqual(EXAMPLE['nexthop'], sot.nexthop)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['vpc_id'], sot.router_id)
        self.assertEqual(EXAMPLE['tenant_id'], sot.project_id)
