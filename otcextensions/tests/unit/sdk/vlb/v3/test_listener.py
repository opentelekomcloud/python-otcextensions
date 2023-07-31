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

from openstack.tests.unit import base

from otcextensions.sdk.vlb.v3 import listener

EXAMPLE = {
    'admin_state_up': True,
    'client_ca_tls_container_ref': 'client-ca-tls-container-ref',
    'client_timeout': 80,
    'created_at': 'created-at',
    'connection_timeout': 80,
    'description': 'description',
    'default_pool_id': 'default-pool-id',
    'default_tls_container_ref': 'default-tls-container-ref',
    'enable_member_retry': True,
    'enhance_l7policy_enable': True,
    'http2_enable': True,
    'insert_headers': {'X-Forwarded-ELB-IP': True},
    'loadbalancers': [{'id': 'lb-uuid1'}, {'id': 'lb-uuid2'}],
    'loadbalancer_id': 'loadbalancer_id',
    'ipgroup': {'ipgroup_id': 'ipgroup-id',
                'enable_ipgroup': True,
                'type': 'type'},
    'name': 'name',
    'keepalive_timeout': 5,
    'member_timeout': 5,
    'protocol': 'protocol',
    'protocol_port': 5,
    'project_id': 'project-id',
    'security_policy_id': 'security-policy-id',
    'sni_container_refs': [],
    'sni_match_algo': 'sni-match-algo',
    'transparent_client_ip_enable': True,
    'tls_ciphers_policy': 'tls-ciphers-policy',
    'updated_at': 'updated-at',
    'tags': [{
        "key": "test",
        "value": "api"
    }]
}


class TestListener(base.TestCase):

    def test_basic(self):
        sot = listener.Listener()
        path = '/elb/listeners'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = listener.Listener(**EXAMPLE)
        self.assertEqual(EXAMPLE['admin_state_up'],
                         sot.is_admin_state_up)
        self.assertEqual(EXAMPLE['client_ca_tls_container_ref'],
                         sot.client_ca_tls_container_ref)
        self.assertEqual(EXAMPLE['client_timeout'], sot.client_timeout)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['connection_timeout'], sot.connection_timeout)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['default_pool_id'], sot.default_pool_id)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['default_tls_container_ref'],
                         sot.default_tls_container_ref)
        self.assertEqual(EXAMPLE['enable_member_retry'],
                         sot.enable_member_retry)
        self.assertEqual(EXAMPLE['enhance_l7policy_enable'],
                         sot.enhance_l7policy)
        self.assertEqual(EXAMPLE['http2_enable'], sot.http2_enable)
        self.assertEqual(EXAMPLE['insert_headers'], sot.insert_headers)
        self.assertEqual(EXAMPLE['loadbalancer_id'], sot.loadbalancer_id)
        self.assertEqual(EXAMPLE['loadbalancers'], sot.load_balancers)
        self.assertEqual(EXAMPLE['ipgroup'], sot.ipgroup)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['keepalive_timeout'], sot.keepalive_timeout)
        self.assertEqual(EXAMPLE['member_timeout'], sot.member_timeout)
        self.assertEqual(EXAMPLE['protocol'], sot.protocol)
        self.assertEqual(EXAMPLE['protocol_port'], sot.protocol_port)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['security_policy_id'], sot.security_policy_id)
        self.assertEqual(EXAMPLE['sni_container_refs'], sot.sni_container_refs)
        self.assertEqual(EXAMPLE['sni_match_algo'], sot.sni_match_algo)
        self.assertEqual(EXAMPLE['tags'], sot.tags)
        self.assertEqual(EXAMPLE['transparent_client_ip_enable'],
                         sot.transparent_client_ip_enable)
        self.assertEqual(EXAMPLE['tls_ciphers_policy'], sot.tls_ciphers_policy)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
