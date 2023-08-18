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

from otcextensions.sdk.vlb.v3 import l7_policy

EXAMPLE = {
    'action': 'action',
    'created_at': 'created-at',
    'description': 'description',
    'admin_state_up': True,
    'listener_id': 'listener-id',
    'name': 'name',
    'priority': 1,
    'project_id': 'project-id',
    'provisioning_status': 'provisioning-status',
    'redirect_pool_id': 'redirect-pool-id',
    'position': 1,
    'redirect_listener_id': 'redirect-listener-id',
    'redirect_url': 'redirect-url',
    'rules': [],
    'redirect_url_config': {},
    'fixed_response_config': {},
    'updated_at': 'updated-at',
}


class TestLoadBalancer(base.TestCase):

    def test_basic(self):
        sot = l7_policy.L7Policy()
        path = '/elb/l7policies'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = l7_policy.L7Policy(**EXAMPLE)
        self.assertEqual(EXAMPLE['action'], sot.action)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(
            EXAMPLE['description'],
            sot.description)
        self.assertEqual(EXAMPLE['admin_state_up'], sot.is_admin_state_up)
        self.assertEqual(EXAMPLE['listener_id'], sot.listener_id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['priority'], sot.priority)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(
            EXAMPLE['provisioning_status'],
            sot.provisioning_status)
        self.assertEqual(EXAMPLE['redirect_pool_id'], sot.redirect_pool_id)
        self.assertEqual(EXAMPLE['position'], sot.position)
        self.assertEqual(EXAMPLE['redirect_listener_id'],
                         sot.redirect_listener_id)
        self.assertEqual(EXAMPLE['redirect_url'], sot.redirect_url)
        self.assertEqual(EXAMPLE['rules'], sot.rules)
        self.assertEqual(EXAMPLE['redirect_url_config'],
                         sot.redirect_url_config)
        self.assertEqual(EXAMPLE['fixed_response_config'],
                         sot.fixed_response_config)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
