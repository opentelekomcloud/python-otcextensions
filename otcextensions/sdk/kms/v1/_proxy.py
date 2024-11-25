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
from urllib import parse

from openstack import proxy

from otcextensions.common.utils import extract_url_parts
from otcextensions.sdk.kms.v1 import data_key as _data_key
from otcextensions.sdk.kms.v1 import key as _key
from otcextensions.sdk.kms.v1 import misc as _misc


class Proxy(proxy.Proxy):

    skip_discovery = True

    def _extract_name(self, url, service_type=None, project_id=None):
        return extract_url_parts(url, project_id)

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            'Content-Type': 'application/json',
            'X-Language': 'en-us'
        }

    # ======== CMK Keys ========
    def keys(self, **query):
        """List all master keys.

        :param dict query: Keyword arguments which will be used to list keys.
            limit, marker, sequence, key_state are allowed.
            Key state can be:
            * 1 indicates that the CMK is waiting to be activated.
            * 2 indicates that the CMK is enabled.
            * 3 indicates that the CMK is disabled.
            * 4 indicates that the CMK is scheduled for deletion.

        :returns: a generator of
            (:class:`~otcextensions.sdk.kms.v1.key.Key`) instances
        """
        return self._list(_key.Key, **query)

    def create_key(self, **attrs):
        """Create master key

        :param dict attrs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.kms.v1.key.Key`

        :returns: instance of :class:`~otcextensions.sdk.kms.v1.key.Key`
        """
        return self._create(
            _key.Key, prepend_key=False, **attrs
        )

    def get_key(self, key):
        """Describe a encrypt key by given key id or key object

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        :returns: instance of :class:`~otcextensions.sdk.kms.v1.key.Key`
        """
        return self._get(
            _key.Key, key,
        )

    def find_key(self, alias, ignore_missing=False):
        """Find a single key

        :param alias: The key alias
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent group.

        :returns: instance of :class:`~otcextensions.sdk.kms.v1.key.Key`
        """
        return self._find(
            _key.Key, alias,
            ignore_missing=ignore_missing,
        )

    def enable_key(self, key):
        """Enable a key

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`

        :returns: Updated instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        """
        key = self._get_resource(_key.Key, key)
        return key.enable(self)

    def disable_key(self, key):
        """Disable a key

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`

        :returns: Updated instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        """
        key = self._get_resource(_key.Key, key)
        return key.disable(self)

    def schedule_key_deletion(self, key, pending_days=7):
        """Schedule a key deletion

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        :param pending_days: Pending days before deletion, allow 7 to 1096
        :returns: Updated instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        """
        key = self._get_resource(_key.Key, key)
        return key.schedule_deletion(self, pending_days)

    def cancel_key_deletion(self, key):
        """Cancel a key deletion

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        :returns: Updated instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        """
        key = self._get_resource(_key.Key, key)
        return key.cancel_deletion(self)

    # ======== Data Keys ========
    def create_datakey(self, cmk, **attrs):
        """Create a data key

        :param cmk: key id or an instance of master key
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        :param dict attrs: Keyword arguments which will be used to create a
            Data key.
            encryption_context, sequence are optional parameters.
        :returns: instance of
            :class:`~otcextensions.sdk.kms.v1.data_key.DataKey`
        """
        key = self._get_resource(_key.Key, cmk)
        attrs['key_id'] = key.id
        return self._create(
            _data_key.DataKey, prepend_key=False, **attrs
        )

    def create_datakey_wo_plain(self, cmk, **attrs):
        """Create a data key without plain text

        :param cmk: key id or an instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        :param dict attrs: Keyword arguments which will be used to create a
            Data key. encryption_context, sequence are optional parameters.
        :returns: instance of
            :class:`~otcextensions.sdk.kms.v1.data_key.DataKey`
        """
        key = self._get_resource(_key.Key, cmk)
        attrs['key_id'] = key.id
        res = _data_key.DataKey.new(**attrs)
        persist = res.create_wo_plain(
            self,
            prepend_key=False,
        )
        return persist

    def encrypt_datakey(self, datakey):
        """Encrypt a data key

        Requires `plain_text` to be filled with the hex key value.
        Populates `cipher_text` with the encrypted value.

        :param datakey: key id or an instance of
            :class:`~otcextensions.sdk.kms.v1.data_key.DataKey`
        :returns: instance of
            :class:`~otcextensions.sdk.kms.v1.data_key.DataKey`
        """
        key = self._get_resource(_data_key.DataKey, datakey)
        key.encrypt(self)
        return key

    # def decrypt_datakey(self, datakey):
    #     """Decrypt a data key
    #
    #     Requires `cipher_text` to be filled with value retrieved from
    #     :func:`~otcextensions.sdk.kms.v1.data_key.DataKey.encrypt` call.
    #     Populates `plain_text` attribute.
    #
    #     :param datakey: key id or an instance of
    #         :class:`~otcextensions.sdk.kms.v1.data_key.DataKey`
    #     :returns: update key instance
    #         :class:`~otcextensions.sdk.kms.v1.data_key.DataKey`
    #     """
    #     key = self._get_resource(_data_key.DataKey, datakey)
    #     key.decrypt(self)
    #     return key

    def decrypt_datakey(self, cmk, cipher_text, datakey_cipher_length):
        """Decrypt a data key

        :param cmk: key id or an instance of
            :class:`~otcextensions.sdk.kms.v1.key.Key`
        :param cipher_text: encrypted value retrieved from
            :func:`~otcextensions.sdk.kms.v1.data_key.DataKey.encrypt` call.
        :param datakey_cipher_length: datakey_cipher_length (expected value 64)

        :returns: decrypted key instance of
            :class:`~otcextensions.sdk.kms.v1.data_key.DataKey` with plain_text
            populated
        """
        cmk_key = self._get_resource(_key.Key, cmk)
        key_attrs = {
            'key_id': cmk_key.id,
            'cipher_text': cipher_text,
            'datakey_cipher_length': datakey_cipher_length
        }
        key = self._get_resource(_data_key.DataKey, value=None, **key_attrs)
        key.decrypt(self)
        return key

    # ======== Misc ========
    def generate_random(self, random_data_length=512):
        """Generate random data

        :param random_data_length: random data size in bits [0..512]
        :returns: instance of :class:`~otcextensions.sdk.kms.v1.random.Random`
        """
        return self._create(
            _misc.Random, prepend_key=False,
            random_data_length=random_data_length
        )

    def get_instance_number(self):
        """Get encrypt key instance total number

        :returns: instance of
            :class:`~otcextensions.sdk.kms.v1.key.InstanceNumber`
        """
        instance_num_obj = _misc.InstanceNumber()
        return instance_num_obj.fetch(self)

    def quotas(self):
        """List quota resources for KMS service

        :returns: A generator of
            :class:`~otcextensions.sdk.kms.v1.key.Quota` objects
        """
        return _misc.Quota.list(self)
