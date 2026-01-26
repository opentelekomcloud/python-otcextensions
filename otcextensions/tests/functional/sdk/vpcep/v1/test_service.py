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
import time
import uuid

from otcextensions.tests.functional.sdk.vpcep import TestVpcep


class TestService(TestVpcep):

    def setUp(self):
        super(TestService, self).setUp()
        self.service_name = 'svc' + uuid.uuid4().hex[:8]

    def _create_service(self, remove=True, approval=False):
        """Create a test service using shared ELB."""
        attrs = {
            'service_name': self.service_name,
            'port_id': self.load_balancer.port_id,
            'vpc_id': self.vpc_id,
            'server_type': 'LB',
            'ports': [{'client_port': 80, 'server_port': 80,
                       'protocol': 'TCP'}],
            'is_approval_enabled': approval,
            'service_type': 'interface'
        }
        service = self.client.create_service(**attrs)
        self.assertIsNotNone(service)

        if remove:
            self.addCleanup(self._cleanup_service, service.id)
        self._wait_for_service_status(service.id, 'available')

        return service

    def _wait_for_service_status(self, service_id, status, timeout=60):
        """Wait for service to reach expected status."""
        start = time.time()
        while time.time() - start < timeout:
            svc = self.client.get_service(service_id)
            if svc.status == status:
                return svc
            time.sleep(2)
        raise Exception(f'Service {service_id} did not reach {status}')

    def test_create_service(self):
        """Test creating an Endpoint Service."""
        service = self._create_service()
        self.assertIn(self.service_name, service.service_name)
        self.assertEqual(self.load_balancer.port_id, service.port_id)

    def test_list_services(self):
        """Test listing Endpoint Services."""
        service = self._create_service()
        services = list(self.client.services())
        self.assertGreater(len(services), 0)

        found = any(s.id == service.id for s in services)
        self.assertTrue(found)

        filtered = list(self.client.services(id=service.id))
        self.assertEqual(1, len(filtered))
        self.assertEqual(service.id, filtered[0].id)

        filtered_name = list(self.client.services(name=service.service_name))
        self.assertEqual(1, len(filtered_name))
        self.assertEqual(service.service_name, filtered_name[0].service_name)

    def test_get_service(self):
        """Test retrieving a single Endpoint Service."""
        service = self._create_service()
        s = self.client.get_service(service.id)
        self.assertIsNotNone(s)
        self.assertEqual(service.id, s.id)

    def test_find_service(self):
        """Test finding an Endpoint Service."""
        service = self._create_service()
        s = self.client.find_service(service.service_name)
        self.assertIsNotNone(s)
        self.assertEqual(service.id, s.id)

    def test_update_service(self):
        """Test updating an Endpoint Service."""
        service = self._create_service()
        updated_name = self.service_name + '_upd'
        s = self.client.update_service(
            service.id,
            service_name=updated_name,
            is_approval_enabled=True
        )
        self.assertIn(updated_name, s.service_name)
        self.assertTrue(s.is_approval_enabled)

        fetched = self.client.get_service(service.id)
        self.assertIn(updated_name, fetched.service_name)
        self.assertTrue(fetched.is_approval_enabled)

    def test_delete_service(self):
        """Test deleting an Endpoint Service."""
        service = self._create_service(remove=False)
        self.client.delete_service(service.id)
        time.sleep(5)

        services = list(self.client.services(id=service.id))
        self.assertEqual(0, len(services))
