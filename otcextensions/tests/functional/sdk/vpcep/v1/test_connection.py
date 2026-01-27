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
import time
from otcextensions.tests.functional.sdk.vpcep import TestVpcep


class TestConnection(TestVpcep):

    def setUp(self):
        super(TestConnection, self).setUp()
        self.network_data = self.create_network()
        self.addCleanup(self.destroy_network, self.network_data)
        self.port = self.create_port(self.network_data['network_id'])
        self.addCleanup(self.destroy_port, self.port.id)
        self.service = self.create_service_helper(approval=True)
        self.endpoint_name = 'sdk-vpcep-test-endpoint-' + uuid.uuid4().hex[:8]
        ep_attrs = {
            'router_id': self.network_data['router_id'],
            'network_id': self.network_data['network_id'],
            'endpoint_service_id': self.service.id,
            'enable_dns': False
        }
        self.endpoint = self.client.create_endpoint(**ep_attrs)
        self.addCleanup(self.client.delete_endpoint, self.endpoint.id)

    def _get_connection(self):
        for i in range(10):
            connections = list(self.client.service_connections(
                self.service.id))
            my_conn = next(
                (c for c in connections if c.id == self.endpoint.id), None)
            if my_conn:
                return my_conn
            time.sleep(2)
        return None

    def test_list_service_connections(self):
        """Test listing service connections."""
        my_conn = self._get_connection()
        self.assertIsNotNone(my_conn, "Connection not found")
        self.assertEqual('pendingAcceptance', my_conn.status)

    def test_accept_service_connections(self):
        """Test accepting a service connection."""
        my_conn = self._get_connection()
        self.assertIsNotNone(my_conn, "Connection not found")
        self.assertEqual('pendingAcceptance', my_conn.status)
        self.client.manage_service_connections(
            self.service.id, action='accept', endpoints=[self.endpoint.id])
        time.sleep(2)
        connections = list(self.client.service_connections(self.service.id))
        my_conn = next((c for c in connections if c.id == self.endpoint.id),
                       None)
        self.assertEqual('accepted', my_conn.status)

    def test_reject_service_connections(self):
        """Test rejecting a service connection."""
        my_conn = self._get_connection()
        self.assertIsNotNone(my_conn, "Connection not found")
        self.assertEqual('pendingAcceptance', my_conn.status)
        self.client.manage_service_connections(
            self.service.id, action='reject', endpoints=[self.endpoint.id])
        time.sleep(2)
        connections = list(self.client.service_connections(self.service.id))
        my_conn = next((c for c in connections if c.id == self.endpoint.id),
                       None)
        self.assertEqual('rejected', my_conn.status)
