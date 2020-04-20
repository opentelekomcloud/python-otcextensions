#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
import random
import uuid

import mock

from openstack.network.v2 import health_monitor
from openstack.network.v2 import listener
from openstack.network.v2 import load_balancer
from openstack.network.v2 import pool
from openstack.network.v2 import pool_member

from otcextensions.tests.unit.osclient import test_base


class TestLoadBalancer(test_base.TestCommand):

    def setUp(self):
        super(TestLoadBalancer, self).setUp()

        self.app.client_manager.network = mock.Mock()
        self.client = self.app.client_manager.network


class FakeLoadBalancer(test_base.Fake):
    """Fake one or more LB"""

    @classmethod
    def generate(cls):
        object_info = {
            'admin_state_up': True,
            'description': 'descr-' + uuid.uuid4().hex,
            'id': 'id-' + uuid.uuid4().hex,
            'listeners': [{'id': 'id-' + uuid.uuid4().hex}],
            'name': 'name-' + uuid.uuid4().hex,
            'operating_status': 'op_stat-' + uuid.uuid4().hex,
            'provisioning_status': 'ps-' + uuid.uuid4().hex,
            'project_id': 'ten-' + uuid.uuid4().hex,
            'vip_address': 'vip_addr-' + uuid.uuid4().hex,
            'vip_subnet_id': 'vip_subn-' + uuid.uuid4().hex,
            'vip_port_id': 'vip_port-' + uuid.uuid4().hex,
            'provider': 'provider-' + uuid.uuid4().hex,
            'pools': [{'id': 'id-' + uuid.uuid4().hex}],
        }
        obj = load_balancer.LoadBalancer.existing(**object_info)
        return obj


class FakeListener(test_base.Fake):
    """Fake one or more LB Listener"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'admin_state_up': True,
            'description': 'descr-' + uuid.uuid4().hex,
            'loadbalancers': [{'id': 'id-' + uuid.uuid4().hex}],
            'protocol': 'proto-' + uuid.uuid4().hex,
            'protocol_port': random.randint(1, 65535),
            'default_pool_id': 'poolid-' + uuid.uuid4().hex,
            'connection_limit': random.randint(-1, 10),

        }
        obj = listener.Listener.existing(**object_info)
        return obj


class FakePool(test_base.Fake):
    """Fake one or more LB Pool"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'admin_state_up': True,
            'description': 'descr-' + uuid.uuid4().hex,
            'loadbalancers': [{'id': 'id-' + uuid.uuid4().hex}],
            'listeners': [{'id': 'id-' + uuid.uuid4().hex}],
            'protocol': 'proto-' + uuid.uuid4().hex,
            'session_persistence': True,
            'healthmonitor_id': 'hmid-' + uuid.uuid4().hex,
            # 'health_monitor_ids': [{'id': 'hmid-' + uuid.uuid4().hex}],
            'member_ids': [{'id': 'id-' + uuid.uuid4().hex}],
            'lb_algorithm': 'algo-' + uuid.uuid4().hex,
            'status': 'dummy'

        }
        obj = pool.Pool.existing(**object_info)
        return obj


class FakePoolMember(test_base.Fake):
    """Fake one or more LB Pool Member"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'admin_state_up': True,
            'address': 'addr-' + uuid.uuid4().hex,
            'operating_status': 'stat-' + uuid.uuid4().hex,
            'pool_id': 'pool_id-' + uuid.uuid4().hex,
            'protocol_port': random.randint(1, 65535),
            'weight': random.randint(1, 65535),
            'subnet_id': 'subnet-' + uuid.uuid4().hex,
        }
        obj = pool_member.PoolMember.existing(**object_info)
        return obj


class FakeHealthMonitor(test_base.Fake):
    """Fake one or more LB Health monitor"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'admin_state_up': True,
            'type': 'type-' + uuid.uuid4().hex,
            'http_method': 'method-' + uuid.uuid4().hex,
            'url_path': 'url_path-' + uuid.uuid4().hex,
            'pools': [{'id': 'id-' + uuid.uuid4().hex}],
            'max_retries': random.randint(1, 65535),
            'timeout': random.randint(1, 65535),
            'expected_codes': 'codes-' + uuid.uuid4().hex,

        }
        obj = health_monitor.HealthMonitor.existing(**object_info)
        return obj
