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
from otcextensions.sdk.kms.v1 import key as _key
from otcextensions.sdk.kms.v1 import data_key as _data_key
from otcextensions.sdk.kms.v1 import misc as _misc
from otcextensions.sdk import sdk_proxy


class Proxy(sdk_proxy.Proxy):

    # ======== CMK Keys ========
    def keys(self, **query):
        """List all keys.

        :param dict kwargs: Keyword arguments which will be used to list keys.
                            limit, marker, sequence are allowed.

        """
        return self._list(_key.Key, paginated=True, **query)

    def create_key(self, **attrs):
        """Create a encrypt key for encrypt a data key

        :param dict kwargs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.v1.key.Key`

        :returns: Updated key instance
        :rtype: :class:`~otcextensions.sdk.v1.key.Key`
        """
        return self._create(
            _key.Key, prepend_key=False, **attrs
        )

    def get_key(self, key):
        """Describe a encrypt key by given key id or key object

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.v1.key.Key`
        :param dict kwargs: Keyword arguments which will be used to describe
            the key. e.g. sequence
        :rtype: :class:`~otcextensions.sdk.v1.key.Key`
        """
        return self._get(
            _key.Key, key,
        )

    def find_key(self, alias, ignore_missing=True):
        """Find a single group

        :param alias: The key alias
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent group.

        :returns: ``None``
        """
        return self._find(
            _key.Key, alias,
            ignore_missing=ignore_missing,
        )

    def enable_key(self, key):
        """Enable a key

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.v1.key.Key`

        :returns: Updated instance of :class:`~otcextensions.sdk.v1.key.Key`
        """
        key = self._get_resource(_key.Key, key)
        return key.enable(self)

    def disable_key(self, key):
        """Disable a key

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.v1.key.Key`
        :returns: Updated instance of :class:`~otcextensions.sdk.v1.key.Key`
        """
        key = self._get_resource(_key.Key, key)
        return key.disable(self)

    def schedule_key_deletion(self, key, pending_days):
        """Schedule a key deletion

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.v1.key.Key`
        :param pending_days: Pending days before deletion, allow 7 to 1096
        :returns: Updated instance of :class:`~otcextensions.sdk.v1.key.Key`
        """
        key = self._get_resource(_key.Key, key)
        return key.schedule_deletion(self, pending_days)

    def cancel_key_deletion(self, key, **params):
        """Cancel a key deletion

        :param key: key id or an instance of
            :class:`~otcextensions.sdk.v1.key.Key`
        :returns: Updated instance of :class:`~otcextensions.sdk.v1.key.Key`
        """
        key = self._get_resource(_key.Key, key)
        return key.cancel_deletion(self)

    # ======== Data Keys ========
    def create_datakey(self, cmk, **attrs):
        """Create a data key

        :param cmk: key id or an instance of
            :class:`~otcextensions.sdk.v1.key.Key`
        :param dict attrs: Keyword arguments which will be used to create a
            Data key, datakey_length is required,
            encryption_context, sequence are optional.
        :rtype: :class:`~otcextensions.sdk.v1.key.DataKey`
        """
        key = self._get_resource(_key.Key, cmk)
        attrs['key_id'] = key.id
        return self._create(
            _data_key.DataKey, prepend_key=False, **attrs
        )

    def create_datakey_wo_plain(self, cmk, **attrs):
        """Create a data key without plain text

        :param cmk: key id or an instance of
            :class:`~otcextensions.sdk.v1.key.Key`
        :param dict attrs: Keyword arguments which will be used to create a
            Data key, datakey_length is required,
            encryption_context, sequence are optional.
        :rtype: :class:`~otcextensions.sdk.v1.key.DataKey`
        """
        key = self._get_resource(_key.Key, cmk)
        attrs['key_id'] = key.id
        res = _data_key.DataKey.new(**attrs)
        persist = res.create_wo_plain(
            self,
            prepend_key=False,
        )
        return persist

    def encrypt_datakey(self, datakey, **params):
        """Encrypt a data key

        :param datakey: key id or an instance of
            :class:`~otcextensions.sdk.v1.key.DataKey`
        :param dict kwargs: Keyword arguments which will be used to encrypt a
            Data key, encryption_context, plain_text,
            datakey_plain_length are required,
            encryption_context, sequence are optional.
        :rtype: :class:`~otcextensions.sdk.v1.key.DataKey`
        """
        key = self._get_resource(_data_key.DataKey, datakey)
        key.encrypt(self)
        return key

    def decrypt_datakey(self, datakey, **params):
        """Decrypt a data key

        :param datakey: key id or an instance of
            :class:`~otcextensions.sdk.v1.key.DataKey`
        :param dict kwargs: Keyword arguments which will be used to decrypt a
            Data key, cipher_text, datakey_cipher_length are
            required, encryption_context, sequence are
            optional.
        :rtype: :class:`~otcextensions.sdk.v1.key.DataKey`
        """
        key = self._get_resource(_data_key.DataKey, datakey)
        key.decrypt(self)
        return key

    # ======== Misc ========
    def generate_random(self, random_data_length=512):
        """Generate random data

        :param random_data_length: random data size in bits [0..512]
        :rtype: :class:`~otcextensions.sdk.v1.random.Random`
        """
        return self._create(
            _misc.Random, prepend_key=False,
            random_data_length=random_data_length
        )

    def get_instance_number(self):
        """Get encrpt key instance total number

        :rtype: :class:`~otcextensions.sdk.v1.key.InstanceNumber`
        """
        instance_num_obj = _misc.InstanceNumber()
        return instance_num_obj.get(self)

    def quotas(self):
        """List quota resources for KMS service

        :returns: A generator of Quota object
        :rtype: :class:`~otcextensions.sdk.v1.key.Quota`
        """
        return _misc.Quota.list(self)
