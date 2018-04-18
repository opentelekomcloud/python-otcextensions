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
import binascii
import hashlib

from openstack import resource

from otcextensions.sdk.kms.v1 import _base


def calculate_plain_message(plain_text):
    hash = hashlib.sha256()
    hex_data = binascii.unhexlify(plain_text)
    # hex_data = str(plain_text).decode(encoding='hex')
    hash.update(bytearray(hex_data))
    digest = hash.hexdigest()
    return (plain_text + digest, len(hex_data))


class DataKey(_base.Resource):

    create_path = '/kms/create-datakey'

    allow_create = True
    allow_update = True

    # Properties
    #: Secret key (CMK) ID
    #: *Type:str*
    key_id = resource.Body('key_id')
    #: Encryption context
    #: Dict (as string) describing resource context information
    #: *Type:str*
    encryption_context = resource.Body('encryption_context', type=dict)
    #: Datakey length
    #: *Type:int*
    datakey_length = resource.Body('datakey_length')
    #: Datakey plain length
    #: *Type:int*
    datakey_plain_length = resource.Body('datakey_plain_length')
    #: Datakey plain length
    #: *Type:int*
    datakey_cipher_length = resource.Body('datakey_cipher_length')
    #: Sequence
    #: *Type:str*
    sequence = resource.Body('sequence')
    #: Plain text of the data key
    #: *Type:str*
    plain_text = resource.Body('plain_text')
    #: Cipher text of the data key and encrypted_value
    #: *Type:str*
    cipher_text = resource.Body('cipher_text')

    def create_wo_plain(self, session, prepend_key=True, requires_id=True,
                        endpoint_override=None, headers=None):
        return super(DataKey, self).create(
            session, prepend_key=prepend_key, requires_id=requires_id,
            endpoint_override=endpoint_override, headers=headers,
            uri='/kms/create-datakey-without-plaintext')

    def encrypt(self, session):
        """Encrypt DEK

        Encrypt DEK with CMK. Requires plain_text to be set with the DEK's
            plain value. Populates encrypted_cipher_text attribute
            with the generated cipher in hex (2 chars per byte)
        """
        session = self._get_session(session)

        plain_text = self.plain_text
        if plain_text is None:
            raise ValueError('plain_text should be provided')
        (msg, size) = calculate_plain_message(plain_text)
        # params.update({'plain_text': msg})
        body = {
            'key_id': self.key_id,
            'plain_text': msg,
            'datakey_plain_length': size,
        }
        if self.sequence:
            body['sequence'] = self.sequence
        if self.encryption_context:
            body['encryption_context'] = self.encryption_context

        url = '/kms/encrypt-datakey'
        response = session.post(
            url,
            json=body)

        self._translate_response(response)

        self._update(
            datakey_cipher_length=self.datakey_length
        )

        return self

    def decrypt(self, session):
        """Decrypt Key

        Decrypts `cipher_text` into `plain_text` with the given CMK
        """
        session = self._get_session(session)
        body = {
            'key_id': self.key_id,
            'cipher_text': self.cipher_text,
            'datakey_cipher_length': self.datakey_cipher_length,
        }
        if self.sequence:
            body['sequence'] = self.sequence
        if self.encryption_context:
            body['encryption_context'] = self.encryption_context

        url = '/kms/decrypt-datakey'
        response = session.post(
            url,
            json=body)

        self._translate_response(response)
        data = response.json()
        self._update(
            plain_text=data['data_key']
        )

        return self
