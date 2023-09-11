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

from otcextensions.sdk.vlb.v3 import load_balancer, listener
from otcextensions.tests.unit.osclient import test_base


def generate_eips_list():
    """Generate random list of vault UUIDs"""
    eips = [{"eip_id": 'eip-uuid-1',
             "eip_address": 'eip-address-1',
             "ip_version": 'ip-version-1'},
            {"eip_id": 'eip-uuid-2',
             "eip_address": 'eip-address-2',
             "ip_version": 'ip-version-2'}
            ]
    return eips


def generate_floating_ips_list():
    """Generate random list of vault UUIDs"""
    floating_ips = [{"publicip_id": "publicip-id-1",
                     "publicip_address": "publicip-address-1",
                     "ip_version": "ip-version-1"},
                    {"publicip_id": "publicip-id-2",
                     "publicip_address": "publicip-address-2",
                     "ip_version": "ip-version-2"}
                    ]
    return floating_ips


def generate_listeners_list():
    """Generate random list of vault UUIDs"""
    listeners = [{"id": 'listener-id-1'},
                 {"id": 'listener-id-2'}]
    return listeners


def generate_pools_list():
    """Generate random list of vault UUIDs"""
    pools = [{"id": 'pool-id-1'},
             {"id": 'pool-id-2'}]
    return pools


def generate_network_ids_list():
    """Generate random list of vault UUIDs"""
    network_ids = []
    random_int = random.randint(1, 10)
    while random_int > 0:
        network_ids.append(uuid.uuid4().hex)
        random_int -= 1
    return network_ids


def generate_tags_list():
    """Generate random list of lb UUIDs"""
    tags = [{'key': 'key-tags', 'value': 'val-tags'}]
    return tags


class TestVLB(test_base.TestCommand):

    def setUp(self):
        super(TestVLB, self).setUp()

        self.app.client_manager.vlb = mock.Mock()
        self.client = self.app.client_manager.vlb


class FakeLoadBalancer(test_base.Fake):
    """Fake one or more loadbalancer"""

    @classmethod
    def generate(cls):
        object_info = {
            "availability_zones": ['eu-de-01'],
            "created_at": uuid.uuid4().hex,
            "description": uuid.uuid4().hex,
            "deletion_protection_enable": True,
            "eips": generate_eips_list(),
            "floating_ip": generate_floating_ips_list()[0],
            "floating_ips": generate_floating_ips_list(),
            "is_guaranteed": True,
            "is_admin_state_up": True,
            "ip_target_enable": True,
            "l4_flavor_id": uuid.uuid4().hex,
            "l7_flavor_id": uuid.uuid4().hex,
            "listeners": generate_listeners_list(),
            "name": uuid.uuid4().hex,
            "network_ids": generate_network_ids_list(),
            "subnet_type": uuid.uuid4().hex,
            "operating_status": uuid.uuid4().hex,
            "pools": generate_pools_list(),
            "project_id": uuid.uuid4().hex,
            "provider": "vlb",
            "provisioning_status": uuid.uuid4().hex,
            "tags": generate_tags_list(),
            "updated_at": uuid.uuid4().hex,
            "ip_address": uuid.uuid4().hex,
            "port_id": uuid.uuid4().hex,
            "subnet_id": uuid.uuid4().hex,
            "vpc_id": uuid.uuid4().hex,
        }

        obj = load_balancer.LoadBalancer.existing(**object_info)
        return obj


def generate_ipgroup():
    """Generate random list of vault UUIDs"""
    ipgroup = {"ipgroup_id": "ipgroup-uuid",
               "enable_ipgroup": True,
               "type":  "ipgroup-type"}
    return ipgroup


def generate_loadbalancers_list():
    """Generate random list of loadbalancers UUIDs"""
    loadbalancers = [{"id": 'loadbalancer-id-1'},
             {"id": 'loadbalancer-id-2'}]
    return loadbalancers


class FakeListener(test_base.Fake):
    """Fake one or more listener"""

    @classmethod
    def generate(cls):
        object_info = {
            "client_ca_tls_container_ref": uuid.uuid4().hex,
            "client_timeout": uuid.uuid4().hex,
            "created_at": uuid.uuid4().hex,
            "connection_limit": 10,
            "default_pool_id": uuid.uuid4().hex,
            "default_tls_container_ref": uuid.uuid4().hex,
            "enable_member_retry": True,
            "enhance_l7policy": True,
            "http2_enable": True,
            "insert_headers": {},
            "is_admin_state_up": True,
            "load_balancers": generate_loadbalancers_list(),
            "ipgroup": generate_ipgroup(),
            "name": uuid.uuid4().hex,
            "keepalive_timeout": 10,
            "member_timeout": 10,
            "protocol": uuid.uuid4().hex,
            "protocol_port": uuid.uuid4().hex,
            "project_id": uuid.uuid4().hex,
            "security_policy_id": uuid.uuid4().hex,
            "sni_container_refs": [],
            "sni_match_algo": uuid.uuid4().hex,
            "tags": generate_tags_list(),
            "transparent_client_ip_enable": True,
            "tls_ciphers_policy": uuid.uuid4().hex,
            "updated_at": uuid.uuid4().hex,
        }

        obj = listener.Listener.existing(**object_info)
        return obj
