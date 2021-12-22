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
from openstack import resource

from otcextensions.sdk.vpc.v1 import vpc
from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestService(base.BaseFunctionalTest):
    _vpc: vpc.Vpc
    _seed: str

    @property
    def seed(self):
        if not hasattr(self, '_seed') or self._seed is None:
            self._seed = uuid.uuid4().hex[:8]
        return self._seed

    def setUp(self):
        super().setUp()

        self.client = self.conn.vpc
        attrs = {
            'name': 'test-vpc-' + self.seed,
            'cidr': '192.168.0.0/16'
        }
        self.vpc = self.conn.vpc.create_vpc(**attrs)
        self.addCleanup(self.conn.vpc.delete_vpc, self.vpc)

    def test_initialize(self):
        client = self.conn.vpc
        self.assertIsNotNone(client)

    def test_create_subnet(self):
        cidr = self.vpc.cidr
        gateway, _ = cidr.split("/")
        gateway = gateway[:-2] + ".1"  # .0 -> .1

        attrs = {
            'vpc_id': self.vpc.id,
            'name': 'test-subnet-' + self.seed,
            'cidr': cidr,
            'gateway_ip': gateway,
            'dns_list': [
                "100.125.4.25",
                "100.125.129.199",
            ],
        }
        subnet = self.conn.vpc.create_subnet(**attrs)
        self.assertIsNotNone(subnet.id)
        self.addCleanup(self._delete_subnet, subnet)

        self.assertIsNotNone(subnet.status)
        self.assertIsNotNone(subnet.neutron_subnet_id)
        self.assertIsNotNone(subnet.neutron_network_id)

    def test_get_subnet(self):
        subnet = self._create_subnet()
        found = self.conn.vpc.get_subnet(subnet.id)

        self.assertEqual(found, subnet)

    def test_find_subnet(self):
        subnet = self._create_subnet()
        found = self.conn.vpc.find_subnet(subnet.name)

        self.assertEqual(found, subnet)

    def test_update_subnet(self):
        subnet = self._create_subnet()

        new_attrs = {
            'name': 'test-updated-' + self.seed,
            'dns_list': [
                "100.125.4.25",
                "8.8.8.8",
            ],
        }
        updated = self.conn.vpc.update_subnet(subnet, **new_attrs)
        self.assertEqual(updated.name, new_attrs['name'])
        self.assertEqual(updated.dns_list, new_attrs['dns_list'])

    def test_delete_subnet(self):
        subnet = self._create_subnet(False)
        self.conn.vpc.delete_subnet(subnet, ignore_missing=False)
        resource.wait_for_delete(self.conn.vpc, subnet, 2, 120)

    def test_list_subnets(self):
        subnet = self._create_subnet()

        subnets = list(self.conn.vpc.subnets())
        self.assertGreaterEqual(len(subnets), 1)

        self.assertIn(subnet, subnets)

    def _create_subnet(self, remove=True):
        cidr: str = self.vpc.cidr
        gateway, _ = cidr.split("/")
        gateway = gateway[:-2] + ".1"  # .0 -> .1

        attrs = {
            'vpc_id': self.vpc.id,
            'name': 'test-subnet-' + self.seed,
            'cidr': cidr,
            'gateway_ip': gateway,
            'dns_list': [
                "100.125.4.25",
                "100.125.129.199",
            ],
        }
        subnet = self.conn.vpc.create_subnet(**attrs)
        resource.wait_for_status(self.conn.vpc, subnet, "ACTIVE", None, 2, 20)

        if remove:
            self.addCleanup(self._delete_subnet, subnet)
        return subnet

    def _delete_subnet(self, subnet):
        resource.wait_for_status(self.conn.vpc, subnet, "ACTIVE", None, 2, 20)
        self.conn.vpc.delete_subnet(subnet, ignore_missing=False)
        resource.wait_for_delete(self.conn.vpc, subnet, 2, 60)
