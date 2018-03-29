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
import uuid

from openstack import _log
from openstack import exceptions

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestDataKey(base.BaseFunctionalTest):

    @classmethod
    def setUpClass(cls):
        super(TestDataKey, cls).setUpClass()
        cls.cmk = cls.conn.kms.create_key(
            key_alias=uuid.uuid4().hex
        )

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.cmk:
                key = cls.cmk
                if key.id:
                    cls.conn.kms.schedule_key_deletion(key, 7)
        except exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_dek(self):

        print(list(self.conn.kms.keys()))

        cmk = self.cmk

        dek = self.conn.kms.create_datakey(
            cmk=cmk,
            datakey_length=512,
            encryption_context={"a": "b", "c": "d"})
        self.assertIsNotNone(dek.plain_text)

        dek2 = self.conn.kms.create_datakey_wo_plain(
            cmk=cmk,
            datakey_length=512,
            encryption_context={"a": "b", "c": "d"})
        self.assertIsNone(dek2.plain_text)

        not_encrypted_value = dek.plain_text
        self.conn.kms.encrypt_datakey(dek)

        encrypted_value = dek.cipher_text

        self.assertIsNotNone(encrypted_value)
        self.assertNotEqual(not_encrypted_value, encrypted_value)
        _logger.debug('encrypted DEK = %s' % encrypted_value)

        self.conn.kms.decrypt_datakey(dek)
        decrypted_value = dek.plain_text
        self.assertEqual(not_encrypted_value, decrypted_value)
