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

from otcextensions.osclient.vlb.v3 import listener
from otcextensions.tests.unit.osclient.vlb.v3 import fakes


class TestListener(fakes.TestVLB):

    def setUp(self):
        super(TestListener, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeListener.create_one()

        flat_data = listener._flatten_listener(obj)

        data = (
            flat_data['client_ca_tls_container_ref'],
            flat_data['connection_limit'],
            flat_data['created_at'],
            flat_data['default_pool_id'],
            flat_data['default_tls_container_ref'],
            flat_data['description'],
            flat_data['http2_enable'],
            flat_data['id'],
            flat_data['insert_headers'],
            flat_data['is_admin_state_up'],
            flat_data['name'],
            flat_data['project_id'],
            flat_data['security_policy_id'],
            flat_data['sni_match_algo'],
            flat_data['protocol'],
            flat_data['protocol_port'],
            flat_data['sni_container_refs'],
            flat_data['updated_at'],
            flat_data['tls_ciphers_policy'],
            flat_data['enable_member_retry'],
            flat_data['keepalive_timeout'],
            flat_data['client_timeout'],
            flat_data['member_timeout'],
            flat_data['ipgroup'],
            flat_data['transparent_client_ip_enable'],
            flat_data['enhance_l7policy_enable']
        )

        cmp_data = (
            obj.client_ca_tls_container_ref,
            obj.connection_limit,
            obj.created_at,
            obj.default_pool_id,
            obj.default_tls_container_ref,
            obj.description,
            obj.http2_enable,
            obj.id,
            obj.insert_headers,
            obj.is_admin_state_up,
            obj.name,
            obj.project_id,
            obj.security_policy_id,
            obj.sni_match_algo,
            obj.protocol,
            obj.protocol_port,
            obj.sni_container_refs,
            obj.updated_at,
            obj.tls_ciphers_policy,
            obj.enable_member_retry,
            obj.keepalive_timeout,
            obj.client_timeout,
            obj.member_timeout,
            obj.ipgroup,
            obj.transparent_client_ip_enable,
            obj.enhance_l7policy

        )

        self.assertEqual(data, cmp_data)

    def test_add_tags_to_listener_output(self):
        obj = fakes.FakeListener.create_one()

        column = ()
        data = ()
        verify_column = (
            'tags',
        )
        verify_data = (
            ('value=val-tags, key=key-tags',)
        )

        data, column = listener._add_tags_to_listener_obj(
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

        result = listener._normalize_tags(tags)

        self.assertEqual(result, verify_result)

    def test_add_loadbalancer_to_listener_output(self):
        obj = fakes.FakeListener.create_one()

        column = ()
        data = ()
        verify_column = (
            'loadbalancer_id_1',
            'loadbalancer_id_2',
        )
        verify_data = (
            'loadbalancer-id-1',
            'loadbalancer-id-2',
        )

        data, column = listener._add_loadbalancers_to_listener_obj(
            obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)
