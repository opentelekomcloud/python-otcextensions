# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy

from keystoneauth1 import adapter
import mock

from openstack.tests.unit import base

from otcextensions.sdk.auto_scaling.v1 import policy

PROJECT_ID = '123'

EXAMPLE = {
    'scaling_policy_id': 'fd7d63ce-8f5c-443e-b9a0-bef9386b23b3',
    'scaling_group_id': 'e5d27f5c-dd76-4a61-b4bc-a67c5686719a',
    'scaling_policy_name': 'schedule1',
    'scaling_policy_type': 'SCHEDULED',
    'scheduled_policy': {
        'launch_time': '2015-07-24T01:21Z'
    },
    'cool_down_time': 300,
    'scaling_policy_action': {
        'operation': 'REMOVE',
        'instance_number': 1
    },
    'policy_status': 'INSERVICE',
    'create_time': '2015-07-24T01:09:30Z'
}

EXAMPLE_LIST = {
    'limit': 20,
    'total_number': 1,
    'start_number': 0,
    'scaling_policies': [
        {
            'scaling_policy_id': 'fd7d63ce-8f5c-443e-b9a0-bef9386b23b3',
            'scaling_group_id': 'e5d27f5c-dd76-4a61-b4bc-a67c5686719a',
            'scaling_policy_name': 'schedule1',
            'scaling_policy_type': 'SCHEDULED',
            'scheduled_policy': {
                'launch_time': '2015-07-24T01:21Z'
            },
            'cool_down_time': 300,
            'scaling_policy_action': {
            'operation': 'REMOVE',
            'instance_number': 1
        },
        'policy_status': 'INSERVICE',
        'create_time': '2015-07-24T01:09:30Z'
        }
    ]
}


class TestPolicy(base.TestCase):

    def setUp(self):
        super(TestPolicy, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        # self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)
        self.sot = policy.Policy(**EXAMPLE)

    def test_basic(self):
        sot = policy.Policy()
        self.assertEqual('scaling_policy', sot.resource_key)
        self.assertEqual('scaling_policies', sot.resources_key)
        self.assertEqual('/scaling_policy', sot.base_path)
        self.assertEqual(
            '/scaling_policy/%(scaling_group_id)s/list', sot.list_path)
        self.assertEqual('as', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = policy.Policy.existing(**EXAMPLE)
        self.assertEqual(EXAMPLE['scaling_policy_id'], sot.id)
        self.assertEqual(EXAMPLE['scaling_policy_name'], sot.name)
        self.assertEqual(EXAMPLE['scaling_policy_type'], sot.type)
        self.assertEqual(EXAMPLE['scaling_group_id'], sot.scaling_group_id)
        self.assertEqual(EXAMPLE['cool_down_time'], sot.cool_down_time)
        self.assertEqual(EXAMPLE['policy_status'], sot.status)
        self.assertEqual(EXAMPLE['create_time'], sot.create_time)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST)

        self.sess.get.return_value = mock_response

        result = list(
            self.sot.list(
                self.sess,
                scaling_group_id='grp_id',
                limit=3,
                marker=4
            )
        )

        self.sess.get.assert_called_once_with(
            '/scaling_policy/grp_id/list',
            params={
                'limit': 3,
                'start_number': 4,
            },
        )

        expected_list = [
            policy.Policy.existing(
                **EXAMPLE_LIST['scaling_policies'][0]),
        ]

        self.assertEqual(expected_list, result)

    def test_get(self):
        sot = policy.Policy.existing(
            id=EXAMPLE['scaling_policy_id'])
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'scaling_policy': EXAMPLE.copy()}

        self.sess.get.return_value = mock_response

        result = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            'scaling_policy/%s' %
            EXAMPLE['scaling_policy_id'],
        )

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['scaling_policy_id'], result.id)
        self.assertEqual(EXAMPLE['scaling_policy_name'], result.name)

    def test_create(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'scaling_policy': {
                'scaling_policy_id': EXAMPLE['scaling_policy_id']
            }}

        self.sess.post.return_value = mock_response

        sot = policy.Policy.new(**EXAMPLE)
        result = sot.create(self.sess, prepend_key=False)

        call_args = self.sess.post.call_args_list[0]

        expected_json = copy.deepcopy(EXAMPLE)
        expected_json.pop('scaling_group_id')

        self.assertEquals('/scaling_policy', call_args[0][0])
        self.assertDictEqual(expected_json, call_args[1]['json'])

        self.sess.post.assert_called_once()

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['scaling_policy_id'], result.id)
        self.assertEqual(EXAMPLE['scaling_policy_name'], result.name)

    def test_delete(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.delete.return_value = mock_response

        sot = policy.Policy.existing(id=EXAMPLE['scaling_policy_id'])

        result = sot.delete(self.sess)

        self.sess.delete.assert_called_once()

    def test_update(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'scaling_policy': {
                'scaling_policy_id': EXAMPLE['scaling_policy_id']
        }}

        self.sess.put.return_value = mock_response

        sot = policy.Policy.existing(id=EXAMPLE['scaling_policy_id'])

        sot._update(**EXAMPLE)

        result = sot.update(self.sess, prepend_key=False)

        call_args = self.sess.put.call_args_list[0]

        expected_json = copy.deepcopy(EXAMPLE)
        expected_json.pop('scaling_policy_id')
        expected_json.pop('scaling_group_id')

        self.assertEquals(
            'scaling_policy/%s' % EXAMPLE['scaling_policy_id'],
            call_args[0][0])
        self.assertDictEqual(expected_json, call_args[1]['json'])

        self.sess.put.assert_called_once()

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['scaling_policy_id'], result.id)
        self.assertEqual(EXAMPLE['scaling_policy_name'], result.name)

    def test_execute(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = policy.Policy.existing(id=EXAMPLE['scaling_policy_id'])

        result = sot.execute(self.sess)

        self.sess.post.assert_called_once_with(
            'scaling_policy/%s/action' % EXAMPLE['scaling_policy_id'],
            json={'action':'execute'}
        )

    def test_pause(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = policy.Policy.existing(id=EXAMPLE['scaling_policy_id'])

        result = sot.pause(self.sess)

        self.sess.post.assert_called_once_with(
            'scaling_policy/%s/action' % EXAMPLE['scaling_policy_id'],
            json={'action':'pause'}
        )

    def test_resume(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = policy.Policy.existing(id=EXAMPLE['scaling_policy_id'])

        result = sot.resume(self.sess)

        self.sess.post.assert_called_once_with(
            'scaling_policy/%s/action' % EXAMPLE['scaling_policy_id'],
            json={'action':'resume'}
        )
