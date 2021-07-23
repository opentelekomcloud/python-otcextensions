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

from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.vlb.v3 import _proxy
from otcextensions.sdk.vlb.v3 import availability_zone
from otcextensions.sdk.vlb.v3 import certificate
from otcextensions.sdk.vlb.v3 import flavor
from otcextensions.sdk.vlb.v3 import health_monitor
from otcextensions.sdk.vlb.v3 import l7_policy
from otcextensions.sdk.vlb.v3 import l7_rule
from otcextensions.sdk.vlb.v3 import listener
from otcextensions.sdk.vlb.v3 import load_balancer
from otcextensions.sdk.vlb.v3 import member
from otcextensions.sdk.vlb.v3 import pool


class TestVlbProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestVlbProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestVlbLoadBalancer(TestVlbProxy):
    def test_load_balancer_create(self):
        self.verify_create(
            self.proxy.create_load_balancer,
            load_balancer.LoadBalancer,
            method_kwargs={
                'az_list': ['az'],
                'name': 'name',
                'description': 'description',
                'guaranteed': True,
                'provider': 'vlb',
                'ip_target_enable': True
            },
            expected_kwargs={
                'az_list': ['az'],
                'name': 'name',
                'description': 'description',
                'guaranteed': True,
                'provider': 'vlb',
                'ip_target_enable': True
            }
        )

    def test_load_balancer_delete(self):
        self.verify_delete(self.proxy.delete_load_balancer,
                           load_balancer.LoadBalancer, True)

    def test_load_balancer_get(self):
        self.verify_get(
            self.proxy.get_load_balancer,
            load_balancer.LoadBalancer
        )

    def test_load_balancers(self):
        self.verify_list(
            self.proxy.load_balancers,
            load_balancer.LoadBalancer
        )

    def test_load_balancer_find(self):
        self.verify_find(
            self.proxy.find_load_balancer,
            load_balancer.LoadBalancer
        )

    def test_load_balancer_update(self):
        self.verify_update(
            self.proxy.update_load_balancer,
            load_balancer.LoadBalancer
        )


class TestVlbListener(TestVlbProxy):
    def test_listener_create(self):
        self.verify_create(
            self.proxy.create_listener,
            listener.Listener,
            method_kwargs={
                'name': 'name',
                'protocol_port': 80,
                'protocol': 'TCP',
            },
            expected_kwargs={
                'name': 'name',
                'protocol_port': 80,
                'protocol': 'TCP',
            }
        )

    def test_listener_delete(self):
        self.verify_delete(self.proxy.delete_listener,
                           listener.Listener, True)

    def test_listener_get(self):
        self.verify_get(
            self.proxy.get_listener,
            listener.Listener
        )

    def test_listeners(self):
        self.verify_list(
            self.proxy.listeners,
            listener.Listener
        )

    def test_listener_find(self):
        self.verify_find(
            self.proxy.find_listener,
            listener.Listener
        )

    def test_listener_update(self):
        self.verify_update(
            self.proxy.update_listener,
            listener.Listener
        )


class TestVlbCertificate(TestVlbProxy):
    def test_certificate_create(self):
        self.verify_create(
            self.proxy.create_certificate,
            certificate.Certificate,
            method_kwargs={
                'private_key': '_private_key',
                'certificate': '_certificate',
                'name': 'name'
            },
            expected_kwargs={
                'private_key': '_private_key',
                'certificate': '_certificate',
                'name': 'name'
            }
        )

    def test_certificate_delete(self):
        self.verify_delete(self.proxy.delete_certificate,
                           certificate.Certificate, True)

    def test_certificate_get(self):
        self.verify_get(
            self.proxy.get_certificate,
            certificate.Certificate
        )

    def test_certificates(self):
        self.verify_list(
            self.proxy.certificates,
            certificate.Certificate
        )

    def test_certificate_find(self):
        self.verify_find(
            self.proxy.find_certificate,
            certificate.Certificate
        )

    def test_certificate_update(self):
        self.verify_update(
            self.proxy.update_certificate,
            certificate.Certificate
        )


class TestVlbAvailabilityZone(TestVlbProxy):
    def test_availability_zones(self):
        self.verify_list(
            self.proxy.availability_zones,
            availability_zone.AvailabilityZone
        )


class TestVlbFlavor(TestVlbProxy):
    def test_flavors(self):
        self.verify_list(
            self.proxy.flavors,
            flavor.Flavor
        )

    def test_flavor_get(self):
        self.verify_get(
            self.proxy.get_flavor,
            flavor.Flavor
        )

    def test_flavor_find(self):
        self.verify_find(
            self.proxy.find_flavor,
            flavor.Flavor
        )


class TestVlbPool(TestVlbProxy):
    def test_pool_create(self):
        self.verify_create(
            self.proxy.create_pool,
            pool.Pool,
            method_kwargs={
                'lb_algorithm': 'ROUND_ROBIN',
                'name': 'name',
                'protocol': 'TCP',
            },
            expected_kwargs={
                'lb_algorithm': 'ROUND_ROBIN',
                'name': 'name',
                'protocol': 'TCP',
            }
        )

    def test_pool_delete(self):
        self.verify_delete(self.proxy.delete_pool,
                           pool.Pool, True)

    def test_pool_get(self):
        self.verify_get(
            self.proxy.get_pool,
            pool.Pool
        )

    def test_pools(self):
        self.verify_list(
            self.proxy.pools,
            pool.Pool
        )

    def test_pool_find(self):
        self.verify_find(
            self.proxy.find_pool,
            pool.Pool
        )

    def test_pool_update(self):
        self.verify_update(
            self.proxy.update_pool,
            pool.Pool
        )


class TestVlbMember(TestVlbProxy):
    def test_member_create(self):
        self.verify_create(
            self.proxy.create_member,
            member.Member,
            method_kwargs={
                'pool': 'pool',
                'name': 'name',
                'protocol_port': 8080,
            },
            expected_kwargs={
                'pool_id': 'pool',
                'name': 'name',
                'protocol_port': 8080,
            }
        )

    def test_member_delete(self):
        self.verify_delete(
            self.proxy.delete_member,
            member.Member,
            True,
            method_kwargs={
                'pool': 'pool'
            },
            expected_kwargs={
                'pool_id': 'pool',
                'ignore_missing': True
            }
        )

    def test_member_get(self):
        self.verify_get(
            self.proxy.get_member,
            member.Member,
            method_kwargs={
                'pool': 'pool'
            },
            expected_kwargs={
                'pool_id': 'pool',
            }
        )

    def test_members(self):
        self.verify_list(
            self.proxy.members,
            member.Member,
            method_kwargs={
                'pool': 'pool'
            },
            expected_kwargs={
                'pool_id': 'pool',
            }
        )

    def test_member_find(self):
        self.verify_find(
            self.proxy.find_member,
            member.Member,
            method_kwargs={
                'pool': 'pool'
            },
            expected_kwargs={
                'pool_id': 'pool',
            }
        )

    def test_member_update(self):
        self.verify_update(
            self.proxy.update_member,
            member.Member,
            method_kwargs={
                'pool': 'pool'
            },
            expected_kwargs={
                'pool_id': 'pool',
            }
        )


class TestVlbHealthMonitor(TestVlbProxy):
    def test_health_monitor_create(self):
        self.verify_create(
            self.proxy.create_health_monitor,
            health_monitor.HealthMonitor,
            method_kwargs={
                'type': 'TCP',
                'timeout': 3,
                'delay': 5,
                'max_retries': 3,
                'admin_state_up': True,
                'monitor_port': 8080,
            },
            expected_kwargs={
                'type': 'TCP',
                'timeout': 3,
                'delay': 5,
                'max_retries': 3,
                'admin_state_up': True,
                'monitor_port': 8080,
            }
        )

    def test_health_monitor_delete(self):
        self.verify_delete(self.proxy.delete_health_monitor,
                           health_monitor.HealthMonitor, True)

    def test_health_monitor_get(self):
        self.verify_get(
            self.proxy.get_health_monitor,
            health_monitor.HealthMonitor
        )

    def test_health_monitors(self):
        self.verify_list(
            self.proxy.health_monitors,
            health_monitor.HealthMonitor
        )

    def test_health_monitor_find(self):
        self.verify_find(
            self.proxy.find_health_monitor,
            health_monitor.HealthMonitor
        )

    def test_health_monitor_update(self):
        self.verify_update(
            self.proxy.update_health_monitor,
            health_monitor.HealthMonitor
        )


class TestVlbL7Policy(TestVlbProxy):
    def test_l7_policy_create(self):
        self.verify_create(
            self.proxy.create_l7_policy,
            l7_policy.L7Policy,
            method_kwargs={
                'action': 'action',
                'name': 'name',
                'redirect_listener_id': 'id',
            },
            expected_kwargs={
                'action': 'action',
                'name': 'name',
                'redirect_listener_id': 'id',
            }
        )

    def test_l7_policy_delete(self):
        self.verify_delete(self.proxy.delete_l7_policy,
                           l7_policy.L7Policy, True)

    def test_l7_policy_get(self):
        self.verify_get(
            self.proxy.get_l7_policy,
            l7_policy.L7Policy
        )

    def test_l7_policies(self):
        self.verify_list(
            self.proxy.l7_policies,
            l7_policy.L7Policy
        )

    def test_l7_policy_find(self):
        self.verify_find(
            self.proxy.find_l7_policy,
            l7_policy.L7Policy
        )

    def test_l7_policy_update(self):
        self.verify_update(
            self.proxy.update_l7_policy,
            l7_policy.L7Policy
        )


class TestVlbL7Rule(TestVlbProxy):
    def test_l7_rule_create(self):
        self.verify_create(
            self.proxy.create_l7_rule,
            l7_rule.L7Rule,
            method_kwargs={
                'l7_policy': 'l7_policy',
            },
            expected_kwargs={
                'l7policy_id': 'l7_policy',
            }
        )

    def test_l7_rule_delete(self):
        self.verify_delete(
            self.proxy.delete_l7_rule,
            l7_rule.L7Rule,
            True,
            method_kwargs={
                'l7_policy': 'l7_policy'
            },
            expected_kwargs={
                'l7policy_id': 'l7_policy',
            }
        )

    def test_l7_rule_get(self):
        self.verify_get(
            self.proxy.get_l7_rule,
            l7_rule.L7Rule,
            method_kwargs={
                'l7_policy': 'l7_policy'
            },
            expected_kwargs={
                'l7policy_id': 'l7_policy',
            }
        )

    def test_l7_rules(self):
        self.verify_list(
            self.proxy.l7_rules,
            l7_rule.L7Rule,
            method_kwargs={
                'l7_policy': 'l7_policy'
            },
            expected_kwargs={
                'l7policy_id': 'l7_policy',
            }
        )

    def test_l7_rule_find(self):
        self.verify_find(
            self.proxy.find_l7_rule,
            l7_rule.L7Rule,
            method_kwargs={
                'l7_policy': 'l7_policy'
            },
            expected_kwargs={
                'l7policy_id': 'l7_policy',
            }
        )

    def test_l7_rule_update(self):
        self.verify_update(
            self.proxy.update_l7_rule,
            l7_rule.L7Rule,
            method_kwargs={
                'l7_policy': 'l7_policy'
            },
            expected_kwargs={
                'l7policy_id': 'l7_policy',
            }
        )
