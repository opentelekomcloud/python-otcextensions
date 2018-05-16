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
import json
import os

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.volume_backup.v2 import backup_policy as _backup_policy

TESTDATA_DIR = os.path.join(os.path.dirname(__file__))

EXAMPLE = {
    "id": "XX",
    "name": "plan01",
    "scheduled_policy": {
        "remain_first_backup_of_curMonth": 'N',
        "rentention_num": 10,
        "frequency": 1,
        "start_time": "12:00",
        "status": "ON"
    },
    "policy_resource_count": 0
}


def _get_fixture(name):
    fixture = os.path.join(
        TESTDATA_DIR,
        'data_files/',
        name)
    with open(fixture, 'r') as data:
        return json.load(data)


class TestBackupPolicy(base.TestCase):

    def setUp(self):
        super(TestBackupPolicy, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.delete = mock.Mock()

        self.sot = _backup_policy.BackupPolicy.existing(**EXAMPLE)

    def test_basic(self):
        sot = _backup_policy.BackupPolicy()
        self.assertEqual('backup_policies', sot.resources_key)
        self.assertEqual('/backuppolicy', sot.base_path)
        self.assertEqual('vbs', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_update)

    def test_make_it(self):
        sot = _backup_policy.BackupPolicy.existing(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(
            EXAMPLE['policy_resource_count'],
            sot.policy_resource_count)
        self.assertEqual(
            EXAMPLE['policy_resource_count'],
            sot.policy_resource_count)
        sp = sot.scheduled_policy
        sp_compare = EXAMPLE['scheduled_policy']
        assert isinstance(sp, _backup_policy.SchedulePolicy)
        self.assertEqual(
            sp_compare['remain_first_backup_of_curMonth'],
            sp.remain_first_backup_of_curMonth)
        self.assertEqual(
            sp_compare['rentention_num'],
            sp.rentention_num)
        self.assertEqual(
            sp_compare['frequency'],
            sp.frequency)
        self.assertEqual(
            sp_compare['start_time'],
            sp.start_time)

    def test_list(self):
        response = _get_fixture('list_backup_policies.json')
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(response)

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess))

        self.sess.get.assert_called_once_with(
            '/backuppolicy',
            params={}
        )

        self.assertIsNotNone(result)

        for bp in result:
            assert isinstance(bp, _backup_policy.BackupPolicy)

    def test_create(self):
        sot = _backup_policy.BackupPolicy.new(**EXAMPLE)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {'backup_policy_id': 'some_id'}

        self.sess.post.return_value = mock_response

        result = sot.create(self.sess, prepend_key=True)

        call_args = self.sess.post.call_args_list[0]

        expected_json = {
            'backup_policy_id': 'XX',
            'policy_resource_count': 0,
            'scheduled_policy': {
                'remain_first_backup_of_curMonth': 'N',
                'rentention_num': 10,
                'frequency': 1,
                'start_time': '12:00',
                'status': 'ON'
            },
            'backup_policy_name': 'plan01'
        }

        self.assertEqual('/backuppolicy', call_args[0][0])
        self.assertDictEqual(expected_json, call_args[1]['json'])

        self.sess.post.assert_called_once()

        self.assertEqual('some_id', result.id)

    def test_delete(self):
        sot = _backup_policy.BackupPolicy.existing(id='some_id')

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.delete.return_value = mock_response

        sot.delete(self.sess)

        self.sess.delete.assert_called_once_with(
            'backuppolicy/%s' % 'some_id',
        )

    def test_update(self):
        sot = _backup_policy.BackupPolicy.existing(id='XX')

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {'backup_policy_id': 'XX'}

        self.sess.put.return_value = mock_response

        sot._update(**EXAMPLE)

        result = sot.update(self.sess)

        call_args = self.sess.put.call_args_list[0]

        expected_json = {
            'policy_resource_count': 0,
            'scheduled_policy': {
                'remain_first_backup_of_curMonth': 'N',
                'rentention_num': 10,
                'frequency': 1,
                'start_time': '12:00',
                'status': 'ON'
            },
            'backup_policy_name': 'plan01'
        }

        self.assertEqual('backuppolicy/XX', call_args[0][0])
        self.assertDictEqual(expected_json, call_args[1]['json'])

        self.sess.put.assert_called_once()

        self.assertDictEqual(
            _backup_policy.BackupPolicy.existing(**EXAMPLE).to_dict(),
            result.to_dict()
        )

    def mocked_requests_find(*args, **kwargs):

        class MockResponse(object):
            def __init__(self, json_data, status_code):
                self.json_data = copy.deepcopy(json_data)
                self.status_code = status_code
                self.headers = {}

            def json(self):
                return self.json_data

        if args[1] == '/backuppolicy/plan02':
            return MockResponse(None, 404)
        elif args[1] == '/backuppolicy':
            response = _get_fixture('list_backup_policies.json')
            return MockResponse(response, 200)

    def test_find(self):
        sot = _backup_policy.BackupPolicy()

        self.sess.get.side_effect = self.mocked_requests_find

        result = sot.find(self.sess, 'plan02')

        calls = [
            # if allow_get is False this will not be invoked
            # mock.call(
            #     '/backuppolicy/plan02',
            #     params={}
            #     ),
            mock.call(
                '/backuppolicy',
                params={}
            )
        ]

        self.sess.get.assert_has_calls(calls)

        print('res=%s' % result)

        expected_data = \
            _get_fixture('list_backup_policies.json')['backup_policies'][1]

        self.assertDictEqual(
            _backup_policy.BackupPolicy.existing(**expected_data).to_dict(),
            result.to_dict()
        )

    def test_execute_policy(self):
        sot = _backup_policy.BackupPolicy.existing(id='XX')

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot.execute(self.sess)

        self.sess.post.assert_called_once_with(
            'backuppolicy/XX/action',
            json=None
        )


class TestBackupPolicyResource(base.TestCase):

    def setUp(self):
        super(TestBackupPolicyResource, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

        self.sot = _backup_policy.BackupPolicyResource()

    def test_basic(self):
        sot = _backup_policy.BackupPolicyResource()
        self.assertEqual('/backuppolicyresources', sot.base_path)
        self.assertEqual('vbs', sot.service.service_type)
        self.assertFalse(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_update)

    def test_make_it(self):
        sot = _backup_policy.BackupPolicyResource()

        self.assertIsNotNone(sot)
        assert isinstance(sot, _backup_policy.BackupPolicyResource)

    def test_link(self):
        response = _get_fixture('link_resources.json')

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = response

        self.sess.post.return_value = mock_response

        result = self.sot.link(
            self.sess, 'pol_id', ["volume-id-1", "volume-id-2"])

        self.sess.post.assert_called_once_with(
            '/backuppolicyresources',
            json={
                'resources': [
                    {'resource_id': 'volume-id-1', 'resource_type': 'volume'},
                    {'resource_id': 'volume-id-2', 'resource_type': 'volume'}
                ],
                'backup_policy_id': 'pol_id'
            }
        )

        self.assertEqual(1, len(result.success_resources))
        self.assertEqual(1, len(result.fail_resources))

    def test_unlink(self):
        response = _get_fixture('unlink_resources.json')

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = response

        self.sess.post.return_value = mock_response

        result = self.sot.unlink(
            self.sess, 'pol_id', ["volume-id-1", "volume-id-2"])

        self.sess.post.assert_called_once_with(
            'backuppolicyresources/pol_id/deleted_resources',
            json={
                'resources': [
                    {'resource_id': 'volume-id-1', 'resource_type': 'volume'},
                    {'resource_id': 'volume-id-2', 'resource_type': 'volume'}
                ],
            }
        )

        self.assertEqual(1, len(result.success_resources))
        self.assertEqual(1, len(result.fail_resources))
