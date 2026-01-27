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
import atexit
import time
import uuid

import openstack

from otcextensions.tests.functional import base

_logger = openstack._log.setup_logging('openstack')

# Module-level cache for shared ELB
_shared_load_balancer = None
_shared_vpc_id = None
_shared_subnet_id = None


def _cleanup_shared_elb():
    """Cleanup shared ELB at module exit."""
    global _shared_load_balancer
    if _shared_load_balancer:
        try:
            from openstack import connection
            from otcextensions import sdk
            conn = connection.Connection(config=base.TEST_CLOUD_REGION)
            sdk.register_otc_extensions(conn)
            conn.vlb.delete_load_balancer(_shared_load_balancer.id)
            conn.vlb.wait_for_delete_load_balancer(
                _shared_load_balancer.id, interval=5, wait=300)
            _logger.info('Deleted shared ELB')
        except Exception as e:
            _logger.warning(f'Error deleting shared ELB: {e}')
        finally:
            _shared_load_balancer = None


atexit.register(_cleanup_shared_elb)


class TestVpcepBase(base.BaseFunctionalTest):
    """Base class for VPCEP tests that don't need ELB
    (quota, public_service)."""

    def setUp(self):
        super(TestVpcepBase, self).setUp()
        self.client = self.conn.vpcep


class TestVpcep(base.NetworkBaseFunctionalTest):
    """Base class for VPCEP functional tests that need ELB.

    Uses lazy initialization with module-level caching to share ELB
    between tests. ELB is cleaned up at module exit via atexit.
    """

    def setUp(self):
        super(TestVpcep, self).setUp()
        self.client = self.conn.vpcep

        self._ensure_load_balancer()

        self.load_balancer = _shared_load_balancer
        self.vpc_id = _shared_vpc_id
        self.subnet_id = _shared_subnet_id

        if not self.load_balancer:
            self.skipTest('ELB not available')

    def _ensure_load_balancer(self):
        """Lazily create shared ELB if not exists."""
        global _shared_load_balancer, _shared_vpc_id, _shared_subnet_id

        if _shared_load_balancer:
            return

        self._find_existing_network()
        if not _shared_vpc_id or not _shared_subnet_id:
            return

        azs = list(self.conn.vlb.availability_zones())
        az = azs[0].code if azs else 'eu-de-01'

        lb_name = 'sdk-vpcep-elb-' + uuid.uuid4().hex[:8]

        attrs = {
            'name': lb_name,
            'description': 'ELB for VPCEP functional tests',
            'vip_subnet_cidr_id': _shared_subnet_id,
            'vpc_id': _shared_vpc_id,
            'availability_zone_list': [az],
            'guaranteed': True,
            'provider': 'vlb',
        }

        _logger.info(f'Creating ELB with attrs: {attrs}')
        _shared_load_balancer = self.conn.vlb.create_load_balancer(**attrs)
        _logger.info(f'Created ELB: {_shared_load_balancer.id}')

        self.conn.vlb.wait_for_load_balancer(
            _shared_load_balancer.id,
            status='ACTIVE',
            interval=5,
            wait=300
        )

        _shared_load_balancer = self.conn.vlb.get_load_balancer(
            _shared_load_balancer.id
        )
        _shared_vpc_id = _shared_load_balancer.vpc_id
        _logger.info(f'ELB active, port_id: {_shared_load_balancer.port_id}, '
                     f'vpc_id: {_shared_vpc_id}')

    def _find_existing_network(self):
        """Find existing VPC and subnet for ELB creation."""
        global _shared_vpc_id, _shared_subnet_id

        vpcs = list(self.conn.vpc.vpcs())
        if not vpcs:
            _logger.warning('No VPCs found')
            return

        for vpc in vpcs:
            subnets = list(self.conn.vpc.subnets(vpc_id=vpc.id))
            for subnet in subnets:
                if subnet.status == 'ACTIVE' and subnet.neutron_subnet_id:
                    _shared_vpc_id = vpc.id
                    _shared_subnet_id = subnet.neutron_subnet_id
                    _logger.info(
                        f'Using VPC {vpc.name} ({vpc.id}) '
                        f'subnet {subnet.name} ({subnet.neutron_subnet_id})'
                    )
                    return

        _logger.warning('No suitable VPC/subnet found')

    def create_service_helper(self, name=None, approval=False):
        """Create a VPCEP service using the shared ELB and wait for it."""
        if not name:
            name = 'svc' + uuid.uuid4().hex[:8]

        attrs = {
            'service_name': name,
            'port_id': self.load_balancer.port_id,
            'vpc_id': self.vpc_id,
            'server_type': 'LB',
            'ports': [{'client_port': 80, 'server_port': 80,
                       'protocol': 'TCP'}],
            'approval_enabled': approval,
            'service_type': 'interface'
        }

        service = self.client.create_service(**attrs)
        self.addCleanup(self._cleanup_service, service.id)

        for _ in range(40):
            service = self.client.get_service(service.id)
            if service.status == 'available':
                return service
            time.sleep(3)
        raise Exception(f'Service {service.id} not available')

    def _cleanup_service(self, service_id):
        """Delete service with retries (endpoints may still be deleting)."""
        for _ in range(10):
            try:
                self.client.delete_service(service_id, ignore_missing=True)
                return
            except Exception as e:
                if 'EndPoint.300' in str(e):
                    time.sleep(3)
                else:
                    _logger.warning(f'Error deleting service {service_id}:{e}')
                    return
