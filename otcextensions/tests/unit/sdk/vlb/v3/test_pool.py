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

from otcextensions.sdk.vlb.v3 import pool

EXAMPLE = {
    'description': 'description',
    'created_at': 'created-at',
    'healthmonitor_id': 'healthmonitor-id',
    'admin_state_up': True,
    'ip_version': 'ip-version',
    'lb_algorithm': 'lb-algorithm',
    'listener_id': 'listener-id',
    'listeners': [{'id': 'uuid1'}, {'id': 'uuid2'}],
    'loadbalancer_id': 'loadbalancer-id',
    'loadbalancers': [{'id': 'uuid1'}, {'id': 'uuid2'}],
    'members': [{'id': 'uuid1'}, {'id': 'uuid2'}],
    'member_deletion_protection_enable': True,
    'name': 'name',
    'project_id': 'project-id',
    'protocol': 'protocol',
    'session_persistence': {'cookie_name': 'cookie-name',
                            'type': 'type',
                            'persistence_timeout': 1},
    'slow_start': {'enable': True,
                   'duration': 1},
    'updated_at': 'updated-at',
    'vpc_id': 'vpc-id',
    'type': 'type',
}


class TestLoadBalancer(base.TestCase):

    def test_basic(self):
        sot = pool.Pool()
        path = '/elb/pools'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = pool.Pool(**EXAMPLE)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['healthmonitor_id'], sot.healthmonitor_id)
        self.assertEqual(EXAMPLE['admin_state_up'], sot.is_admin_state_up)
        self.assertEqual(EXAMPLE['ip_version'], sot.ip_version)
        self.assertEqual(EXAMPLE['lb_algorithm'], sot.lb_algorithm)
        self.assertEqual(EXAMPLE['listener_id'], sot.listener_id)
        self.assertEqual(EXAMPLE['listeners'], sot.listeners)
        self.assertEqual(EXAMPLE['loadbalancer_id'], sot.loadbalancer_id)
        self.assertEqual(EXAMPLE['loadbalancers'], sot.loadbalancers)
        self.assertEqual(EXAMPLE['members'], sot.members)
        self.assertEqual(EXAMPLE['member_deletion_protection_enable'],
                         sot.member_deletion_protection_enable)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['protocol'], sot.protocol)
        self.assertEqual(EXAMPLE['session_persistence'],
                         sot.session_persistence)
        self.assertEqual(EXAMPLE['slow_start'], sot.slow_start)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
        self.assertEqual(EXAMPLE['vpc_id'], sot.vpc_id)
        self.assertEqual(EXAMPLE['type'], sot.type)
