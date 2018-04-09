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
import mock
import copy

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.kms.v1 import key as _key

EXAMPLE = {
    'key_id': '0d0466b0-e727-4d9c-b35d-f84bb474a37f',
    'domain_id': '00074811d5c27c4f8d48bb91e4a1dcfd',
    'key_alias': 'caseuirpr',
    'realm': 'cn-north-1',
    'key_description': '123',
    'creation_date': '1502799822000',
    'scheduled_deletion_date': '',
    'key_state': '2',
    'default_key_flag': '0',
    'key_type': '1',
    'expiration_time': '1501578672000',
    'origin': 'kms'
}

EXAMPLE_LIST_P1 = {
    'keys': [
        '0d0466b0-e727-4d9c-b35d-f84bb474a37f',
    ],
    'key_details': [{
        'key_id': '0d0466b0-e727-4d9c-b35d-f84bb474a37f',
        'domain_id': '00074811d5c27c4f8d48bb91e4a1dcfd',
        'key_alias': 'caseuirpr',
        'realm': 'cn-north-1',
        'key_description': '123',
        'creation_date': '1502799822000',
        'scheduled_deletion_date': '',
        'key_state': '2',
        'default_key_flag': '0',
        'key_type': '1',
        'expiration_time': '1501578672000',
        'origin': 'kms'
    }],
    'next_marker': '1',
    'truncated': 'true'
}
EXAMPLE_LIST_P2 = {
    'keys': [
        '2e258389-bb1e-4568-a1d5-e1f50adf70ea',
    ],
    'key_details': [{
        'key_id': '2e258389-bb1e-4568-a1d5-e1f50adf70ea',
        'domain_id': '00074811d5c27c4f8d48bb91e4a1dcfd',
        'key_alias': 'casehvniz',
        'realm': 'cn-north-1',
        'key_description': '234',
        'creation_date': '1502799820000',
        'scheduled_deletion_date': '',
        'key_state': '2',
        'default_key_flag': '0',
        'key_type': '1',
        'expiration_time': '1501578673000',
        'origin': 'kms'
    }],
    'next_marker': '',
    'truncated': 'false'
}


class TestKey(base.TestCase):

    def setUp(self):
        super(TestKey, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()
        self.sot = _key.Key()

    def test_basic(self):
        sot = _key.Key()
        self.assertEqual('key_info', sot.resource_key)
        self.assertEqual('key_details', sot.resources_key)
        self.assertEqual('/kms', sot.base_path)
        self.assertEqual('/kms/list-keys', sot.list_path)
        self.assertEqual('kms', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = _key.Key.existing(**EXAMPLE)
        self.assertEqual(EXAMPLE['key_id'], sot.id)
        self.assertEqual(EXAMPLE['domain_id'], sot.domain_id)
        self.assertEqual(EXAMPLE['domain_id'], sot.domain_id)
        self.assertEqual(EXAMPLE['key_alias'], sot.key_alias)
        self.assertEqual(EXAMPLE['realm'], sot.realm)
        self.assertEqual(EXAMPLE['key_description'], sot.key_description)
        self.assertEqual(EXAMPLE['creation_date'], sot.creation_date)
        self.assertEqual(EXAMPLE['scheduled_deletion_date'],
                         sot.scheduled_deletion_date)
        self.assertEqual(EXAMPLE['key_state'], sot.key_state)
        self.assertEqual(EXAMPLE['default_key_flag'], sot.default_key_flag)
        self.assertEqual(EXAMPLE['key_type'], sot.key_type)
        # self.assertEqual(EXAMPLE['error_code'], sot.error_code)
        # self.assertEqual(EXAMPLE['error_msg'], sot.error_msg)

    def mocked_requests_list(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = copy.deepcopy(json_data)
                self.status_code = status_code

            def json(self):
                return self.json_data

        marker = kwargs['json']['marker']
        if marker == '0':
            return MockResponse(EXAMPLE_LIST_P1, 200)
        elif marker == '1':
            return MockResponse(EXAMPLE_LIST_P2, 200)

        return MockResponse(None, 404)

    def test_list(self):
        self.sess.post.side_effect = self.mocked_requests_list

        result = list(
            self.sot.list(
                self.sess,
                limit=1,
                marker='0',
                key_state='state',
                sequence='seq'
            )
        )

        calls = [
            mock.call('/kms/list-keys', json={
                'limit': 1, 'marker': '1',
                'key_state': 'state', 'sequence': 'seq'}),
            mock.call('/kms/list-keys', json={
                'limit': 1, 'marker': '1',
                'key_state': 'state', 'sequence': 'seq'}),
        ]

        self.sess.post.assert_has_calls(calls)

        expected_list = [
            _key.Key.existing(**EXAMPLE_LIST_P1['key_details'][0]),
            _key.Key.existing(**EXAMPLE_LIST_P2['key_details'][0])
        ]

        self.assertEqual(expected_list, result)

    def test_get(self):
        sot = _key.Key.existing(
            id=EXAMPLE['key_id'])
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'key_info': EXAMPLE.copy()}

        self.sess.post.return_value = mock_response

        result = sot.get(self.sess)

        self.sess.post.assert_called_once_with(
            '/kms/describe-key',
            json={
                'key_id': EXAMPLE['key_id']
            }
        )

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['key_id'], sot.id)
        self.assertEqual(EXAMPLE['domain_id'], sot.domain_id)
        self.assertEqual(EXAMPLE['domain_id'], sot.domain_id)
        self.assertEqual(EXAMPLE['key_alias'], sot.key_alias)
        self.assertEqual(EXAMPLE['realm'], sot.realm)
        self.assertEqual(EXAMPLE['key_description'], sot.key_description)
        self.assertEqual(EXAMPLE['creation_date'], sot.creation_date)
        self.assertEqual(EXAMPLE['scheduled_deletion_date'],
                         sot.scheduled_deletion_date)
        self.assertEqual(EXAMPLE['key_state'], sot.key_state)
        self.assertEqual(EXAMPLE['default_key_flag'], sot.default_key_flag)
        self.assertEqual(EXAMPLE['key_type'], sot.key_type)

    def test_create(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'key_info': {
                'key_id': EXAMPLE['key_id'],
                'domain_id': EXAMPLE['domain_id']
            }
        }

        self.sess.post.return_value = mock_response

        key = {
            'key_alias': EXAMPLE['key_alias'],
            'key_description': EXAMPLE['key_description'],
            'realm': EXAMPLE['realm'],
            'key_type': EXAMPLE['key_type'],
            # 'key_policy': 'policy',
            # 'key_usage': 'usage',
            # 'sequence': 'sequence'
        }

        sot = _key.Key.new(**key)
        result = sot.create(self.sess, prepend_key=False)

        call_args = self.sess.post.call_args_list[0]

        expected_json = copy.deepcopy(key)
        # expected_json.pop('scaling_group_id')
        #
        self.assertEquals('/kms/create-key', call_args[0][0])
        self.assertDictEqual(expected_json, call_args[1]['json'])

        self.sess.post.assert_called_once(
            # '/kms/create-key',
            # json=key
        )

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['key_id'], sot.id)
        self.assertEqual(EXAMPLE['domain_id'], sot.domain_id)
        self.assertEqual(EXAMPLE['key_alias'], sot.key_alias)
        self.assertEqual(EXAMPLE['realm'], sot.realm)
        self.assertEqual(EXAMPLE['key_description'], sot.key_description)

    def test_enable(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = _key.Key.existing(id=EXAMPLE['key_id'])

        sot.enable(self.sess)

        self.sess.post.assert_called_once_with(
            'kms/enable-key',
            json={'key_id': EXAMPLE['key_id']}
        )

    def test_disable(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = _key.Key.existing(id=EXAMPLE['key_id'])

        sot.disable(self.sess)

        self.sess.post.assert_called_once_with(
            'kms/disable-key',
            json={'key_id': EXAMPLE['key_id']}
        )

    def test_schedule_deletion(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = _key.Key.existing(id=EXAMPLE['key_id'])

        sot.schedule_deletion(self.sess, 10)

        self.sess.post.assert_called_once_with(
            'kms/schedule-key-deletion',
            json={'key_id': EXAMPLE['key_id'], 'pending_days': 10}
        )

    def test_cancel_deletion(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = _key.Key.existing(id=EXAMPLE['key_id'])

        sot.cancel_deletion(self.sess)

        self.sess.post.assert_called_once_with(
            'kms/cancel-key-deletion',
            json={'key_id': EXAMPLE['key_id']}
        )
