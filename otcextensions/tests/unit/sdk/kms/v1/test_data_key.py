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
import binascii
import hashlib

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.kms.v1 import data_key as _key

EXAMPLE = {
    'key_id': '0d0466b0-e727-4d9c-b35d-f84bb474a37f',
    'plain_text': '8151014275E426C72EE7D44267EF11590DCE0089E19',
    'cipher_text': '020098009EEAFCE122CAA5927D2E020086F9548BA167',
}


class TestKey(base.TestCase):

    def setUp(self):
        super(TestKey, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()
        self.sot = _key.DataKey()

    def test_basic(self):
        sot = _key.DataKey()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)
        self.assertEqual('/kms', sot.base_path)
        self.assertEqual('/kms/create-datakey', sot.create_path)
        self.assertFalse(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = _key.DataKey.existing(**EXAMPLE)
        self.assertEqual(EXAMPLE['key_id'], sot.key_id)
        self.assertEqual(EXAMPLE['plain_text'], sot.plain_text)
        self.assertEqual(EXAMPLE['cipher_text'], sot.cipher_text)

    def test_create(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = EXAMPLE.copy()

        self.sess.post.return_value = mock_response

        key = {
            'key_id': 'key',
            'encryption_context': {
                'a': 'b'
            },
            'datakey_length': 200,
            'sequence': 'seq',
        }

        sot = _key.DataKey(**key)
        result = sot.create(self.sess, prepend_key=False)

        call_args = self.sess.post.call_args_list[0]

        self.assertEqual('/kms/create-datakey', call_args[0][0])
        self.assertDictEqual(key, call_args[1]['json'])

        self.sess.post.assert_called_once()

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['key_id'], sot.key_id)
        self.assertEqual(EXAMPLE['plain_text'], sot.plain_text)
        self.assertEqual(EXAMPLE['cipher_text'], sot.cipher_text)

    def test_create_wo_plain(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'key_id': EXAMPLE['key_id'],
            'cipher_text': EXAMPLE['cipher_text'],
        }

        self.sess.post.return_value = mock_response

        key = {
            'key_id': 'key',
            'encryption_context': {
                'a': 'b'
            },
            'datakey_length': 200,
            'sequence': 'seq',
        }

        sot = _key.DataKey(**key)
        result = sot.create_wo_plain(self.sess, prepend_key=False)

        call_args = self.sess.post.call_args_list[0]

        self.assertEqual(
            '/kms/create-datakey-without-plaintext',
            call_args[0][0])
        self.assertDictEqual(key, call_args[1]['json'])

        self.sess.post.assert_called_once()

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['key_id'], sot.key_id)
        self.assertIsNone(sot.plain_text)
        self.assertEqual(EXAMPLE['cipher_text'], sot.cipher_text)

    def test_encrypt(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'key_id': EXAMPLE['key_id'],
            'cipher_text': EXAMPLE['cipher_text'],
            'datakey_length': 10
        }

        self.sess.post.return_value = mock_response

        plain_key = \
            '0000000000000000000000000000000000000000000000000000000000000000'
        hash = hashlib.sha256()
        hex_data = hex_data = binascii.unhexlify(plain_key)
        hash.update(bytearray(hex_data))
        digest = hash.hexdigest()
        encr_key = plain_key + digest

        key = {
            'key_id': EXAMPLE['key_id'],
            'encryption_context': {'a': 'b'},
            'plain_text': plain_key,
            'sequence': 'seq',
        }

        sot = _key.DataKey.existing(**key)
        result = sot.encrypt(self.sess)

        expected_json = {
            'key_id': EXAMPLE['key_id'],
            'encryption_context': {'a': 'b'},
            'plain_text': encr_key,
            'datakey_plain_length': len(hex_data),
            'sequence': 'seq'
        }

        call_args = self.sess.post.call_args_list[0]

        self.assertEqual('/kms/encrypt-datakey', call_args[0][0])
        self.assertDictEqual(expected_json, call_args[1]['json'])

        self.sess.post.assert_called_once()

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['key_id'], sot.key_id)
        self.assertEqual(10, sot.datakey_length)
        self.assertEqual(EXAMPLE['cipher_text'], sot.cipher_text)

    def test_decrypt(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'data_key': EXAMPLE['plain_text'],
            'datakey_length': 10
        }

        self.sess.post.return_value = mock_response

        key = {
            'key_id': EXAMPLE['key_id'],
            'encryption_context': {'a': 'b'},
            'cipher_text': EXAMPLE['cipher_text'],
            'datakey_cipher_length': 200,
            'sequence': 'seq',
        }

        sot = _key.DataKey.existing(**key)
        result = sot.decrypt(self.sess)

        expected_json = key

        call_args = self.sess.post.call_args_list[0]

        self.assertEqual('/kms/decrypt-datakey', call_args[0][0])
        self.assertDictEqual(expected_json, call_args[1]['json'])

        self.sess.post.assert_called_once()

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['key_id'], sot.key_id)
        self.assertEqual(EXAMPLE['plain_text'], sot.plain_text)
