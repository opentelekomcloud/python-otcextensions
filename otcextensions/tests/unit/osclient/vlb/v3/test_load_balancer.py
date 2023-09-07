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

from otcextensions.osclient.vlb.v3 import load_balancer
from otcextensions.tests.unit.osclient.vlb.v3 import fakes


class TestLoadBalancer(fakes.TestVLB):

    def setUp(self):
        super(TestLoadBalancer, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeLoadBalancer.create_one()

        flat_data = load_balancer._flatten_loadbalancer(obj)

        data = (
            flat_data['availability_zone_list'],
            flat_data['created_at'],
            flat_data['description'],
            flat_data['deletion_protection_enable'],
            flat_data['is_guaranteed'],
            flat_data['is_admin_state_up'],
            flat_data['ip_target_enable'],
            flat_data['l4_flavor_id'],
            flat_data['l7_flavor_id'],
            flat_data['name'],
            flat_data['network_ids'],
            flat_data['subnet_type'],
            flat_data['operating_status'],
            flat_data['project_id'],
            flat_data['provider'],
            flat_data['provisioning_status'],
            flat_data['updated_at'],
            flat_data['ip_address'],
            flat_data['port_id'],
            flat_data['subnet_id'],
            flat_data['vpc_id']
        )

        cmp_data = (
            obj.availability_zones,
            obj.created_at,
            obj.description,
            obj.deletion_protection_enable,
            obj.is_guaranteed,
            obj.is_admin_state_up,
            obj.ip_target_enable,
            obj.l4_flavor_id,
            obj.l7_flavor_id,
            obj.name,
            obj.network_ids,
            obj.subnet_type,
            obj.operating_status,
            obj.project_id,
            obj.provider,
            obj.provisioning_status,
            obj.updated_at,
            obj.ip_address,
            obj.port_id,
            obj.subnet_id,
            obj.vpc_id
        )

        self.assertEqual(data, cmp_data)

    def test_add_tags_to_loadbalancer_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'tags',
        )
        verify_data = (
            ('value=val-tags, key=key-tags',)
        )

        data, column = load_balancer._add_tags_to_load_balancer_obj(
            obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_normalize_tags(self):
        tags = [
            'key1=value',
            'key2=',
            'key3'
        ]

        verify_result = [
            {'key': 'key1', 'value': 'value'},
            {'key': 'key2', 'value': ''},
            {'key': 'key3', 'value': ''}
        ]

        result = load_balancer._normalize_tags(tags)

        self.assertEqual(result, verify_result)

    def test_add_eips_to_loadbalancer_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'eip_id_1',
            'eip_address_1',
            'ip_version_1',
            'eip_id_2',
            'eip_address_2',
            'ip_version_2'
        )
        verify_data = (
            'eip-uuid-1',
            'eip-address-1',
            'ip-version-1',
            'eip-uuid-2',
            'eip-address-2',
            'ip-version-2'
        )

        data, column = load_balancer._add_eips_to_load_balancer_obj(
            obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_publicips_to_loadbalancer_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'publicip_id_1',
            'publicip_address_1',
            'publicip_ip_version_1',
            'publicip_id_2',
            'publicip_address_2',
            'publicip_ip_version_2',
        )
        verify_data = (
            'publicip-id-1',
            'publicip-address-1',
            'ip-version-1',
            'publicip-id-2',
            'publicip-address-2',
            'ip-version-2',
        )

        data, column = load_balancer._add_publicips_to_load_balancer_obj(
            obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_pools_to_loadbalancer_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'pool_id_1',
            'pool_id_2',
        )
        verify_data = (
            'pool-id-1',
            'pool-id-2',
        )

        data, column = load_balancer._add_pools_to_load_balancer_obj(
            obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_listeners_to_loadbalancer_output(self):
        obj = fakes.FakeLoadBalancer.create_one()

        column = ()
        data = ()
        verify_column = (
            'listener_id_1',
            'listener_id_2',
        )
        verify_data = (
            'listener-id-1',
            'listener-id-2',
        )

        data, column = load_balancer._add_listeners_to_load_balancer_obj(
            obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)
