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
from openstack import resource
from openstack import _log
from openstack import exceptions

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestCleanup(base.BaseFunctionalTest):
    def setUp(self):
        super(TestCleanup, self).setUp()

    def test_01_create(self):
        flavor = list(self.conn.dws.flavors())[0]
        network = list(self.conn.network.networks())[0]
        router = list(self.conn.network.routers())[0]
        security_group = list(self.conn.network.security_groups())[0]
        attrs = {
            'name': 'dws-1',
            'flavor': flavor['name'],
            'num_nodes': 3,
            'availability_zone': 'eu-de-01',
            'router_id': router['id'],
            'network_id': network['id'],
            'security_group_id': security_group['id'],
            'port': 8000,
            'user_name': 'dbadmin',
            'user_pwd': 'PasswordDbGauss!@',
            'public_ip': {
                'public_bind_type': 'auto_assign',
                'eip_id': ''
            }
        }
        self.conn.dws.create_cluster(**attrs)
        try:
            resource.wait_for_status(
                self.client, self.client.get_cluster(self.cluster.id),
                "AVAILABLE",
                ["CREATION FAILED", "UNAVAILABLE"],
                10,
                1200
            )
        except exceptions.ResourceFailure:
            self.client.delete_cluster(self.cluster.id)
        clusters = list(self.conn.dws.clusters())

    def test_02_delete(self):
        clusters = list(self.conn.dws.clusters())
        self.conn.dws._service_cleanup(dry_run=False)
        clusters = list(self.conn.dws.clusters())
        self.assertEqual(len(clusters), 0)
