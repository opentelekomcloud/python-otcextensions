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

from openstack import _log

from otcextensions.sdk.vpc.v1 import vpc
from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestService(base.BaseFunctionalTest):
    ID = None
    uuid = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestService, self).setUp()

        attrs = {
            'name': "test-vpc-" + self.uuid,
            'cidr': '192.168.0.0/24'
        }

        self.NAME = "test-vpc-" + self.uuid
        self.UPDATE_NAME = "test-vpc-upd-" + self.uuid

        self.vpc = self.conn.vpc.create_vpc(**attrs)
        assert isinstance(self.vpc, vpc.Vpc)
        self.assertEqual(self.NAME, self.vpc.name)
        self.ID = self.vpc.id
        self.addCleanup(self.conn.vpc.delete_vpc, self.vpc)

    def test_find_vpc(self):
        found = self.conn.vpc.find_vpc(self.NAME)
        self.assertEqual(found.id, self.ID)

    def test_get_vpc(self):
        found = self.conn.vpc.get_vpc(self.ID)
        self.assertEqual(found.name, self.NAME)
        self.assertEqual(found.id, self.ID)

    def test_list_vpcs(self):
        vpcs = [o.name for o in self.conn.vpc.vpcs()]
        self.assertIn(self.NAME, vpcs)

    def test_update_vpc(self):
        new_attrs = {
            'name': self.UPDATE_NAME,
            'cidr': '192.168.0.0/16'
        }
        updated = self.conn.vpc.update_vpc(self.ID, **new_attrs)
        self.assertEqual(updated.name, new_attrs['name'])
        self.assertEqual(updated.cidr, new_attrs['cidr'])
