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

import mock
import random
import uuid

from otcextensions.sdk.vlb.v3 import load_balancer
from otcextensions.sdk.vlb.v3 import listener
from otcextensions.tests.unit.osclient import test_base


def generate_network_ids_list():
    """Generate random list of vault UUIDs"""
    network_ids = []
    random_int = random.randint(1, 10)
    while random_int > 0:
        network_ids.append(uuid.uuid4().hex)
        random_int -= 1
    return network_ids


class TestVLB(test_base.TestCommand):

    def setUp(self):
        super(TestVLB, self).setUp()

        self.app.client_manager.vlb = mock.Mock()
        self.client = self.app.client_manager.vlb


class FakeLoadBalancer(test_base.Fake):
    """Fake one or more VLB loadbalancers"""

    @classmethod
    def generate(cls):
        object_info = {
            "id": 'id-' + uuid.uuid4().hex,
            "name": 'name-' + uuid.uuid4().hex,
            "availability_zones": [random.choice(['eu-de-01',
                                                  'eu-de-02',
                                                  'eu-de-03'])],
            "created_at": uuid.uuid4().hex,
            "description": uuid.uuid4().hex,
            "eips": [{
                "eip_id": "eip-uuid",
                "eip_address": "eip-address",
                "ip_version": "ip-version"}],
            "flavor_id": uuid.uuid4().hex,
            "guaranteed": True,
            "l4_flavor_id": uuid.uuid4().hex,
            "l4_scale_flavor_id": uuid.uuid4().hex,
            "l7_flavor_id": uuid.uuid4().hex,
            "l7_scale_flavor_id": uuid.uuid4().hex,
            "listeners": [{"id": "listener-uuid"}],
            "operating_status": "ONLINE",
            "pools": [{"id": "pool-uuid"}],
            "project_id": uuid.uuid4().hex,
            "provider": 'vlb',
            "provisioning_status": 'ACTIVE',
            "tags": [{"key": "tag-key", "value": "tag-value"}],
            "updated_at": uuid.uuid4().hex,
            "vip_address": uuid.uuid4().hex,
            "vip_network_id": uuid.uuid4().hex,
            "vip_port_id": uuid.uuid4().hex,
            "vip_subnet_id": uuid.uuid4().hex,
            "vip_qos_policy_id": uuid.uuid4().hex,
            "floating_ips": [{"publicip_id": "publicip-uuid",
                              "publicip_address": "publicip-address",
                              "ip_version": "ip-version"}],
            "ip_target_enable": True,
            "ipv6_vip_address": uuid.uuid4().hex,
            "ipv6_vip_subnet_id": uuid.uuid4().hex,
            "ipv6_vip_port_id": uuid.uuid4().hex,
            "network_ids": generate_network_ids_list(),
            "vpc_id": uuid.uuid4().hex
        }

        obj = load_balancer.LoadBalancer.existing(**object_info)
        return obj


class TestVLB(test_base.TestCommand):

    def setUp(self):
        super(TestVLB, self).setUp()

        self.app.client_manager.vlb = mock.Mock()
        self.client = self.app.client_manager.vlb
