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
from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.kms.v1 import _proxy
from otcextensions.sdk.kms.v1 import data_key as _data_key
from otcextensions.sdk.kms.v1 import key as _key
from otcextensions.sdk.kms.v1 import misc as _misc


class TestKmsProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestKmsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestKmsKeys(TestKmsProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.keys, _key.Key,
            # mock_method='openstack.proxy.Proxy._list',
            method_kwargs={
                'some_arg': 'arg_value',
            },
            expected_kwargs={
                'some_arg': 'arg_value',
            }
        )

    def test_get(self):
        self.verify_get(
            self.proxy.get_key,
            _key.Key,
            # mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={
            }
        )

    def test_create(self):
        self.verify_create(
            self.proxy.create_key, _key.Key,
            mock_method='openstack.proxy.Proxy._create',
            method_kwargs={
                'instance': 'test',
                'name': 'some_name'
            },
            expected_kwargs={
                'prepend_key': False,
                'instance': 'test',
                'name': 'some_name'
            }
        )

    def test_enable(self):
        self._verify(
            'otcextensions.sdk.kms.v1.key.Key.enable',
            self.proxy.enable_key,
            method_args=['INSTANCE'],
            expected_args=[self.proxy]
        )

    def test_disable(self):
        self._verify(
            'otcextensions.sdk.kms.v1.key.Key.disable',
            self.proxy.disable_key,
            method_args=['INSTANCE'],
            expected_args=[self.proxy]
        )

    def test_schedule_deletion(self):
        self._verify(
            'otcextensions.sdk.kms.v1.key.Key.schedule_deletion',
            self.proxy.schedule_key_deletion,
            method_args=['INSTANCE', 3],
            expected_args=[self.proxy, 3]
        )

    def test_cancel_deletion(self):
        self._verify(
            'otcextensions.sdk.kms.v1.key.Key.cancel_deletion',
            self.proxy.cancel_key_deletion,
            method_args=['INSTANCE'],
            expected_args=[self.proxy]
        )


class TestKmsDataKeys(TestKmsProxy):

    def test_create(self):
        self.verify_create(
            self.proxy.create_datakey, _data_key.DataKey,
            mock_method='openstack.proxy.Proxy._create',
            method_args=['CMK'],
            method_kwargs={
                'name': 'some_name'
            },
            expected_kwargs={
                'prepend_key': False,
                'name': 'some_name',
                'key_id': 'CMK'
            }
        )

    def test_create_no_plain(self):
        self._verify(
            'otcextensions.sdk.kms.v1.data_key.DataKey.create_wo_plain',
            self.proxy.create_datakey_wo_plain,
            method_args=['INSTANCE'],
            expected_args=[self.proxy],
            expected_kwargs={
                'prepend_key': False,
            }
        )

    # def test_encrypt(self):
    #     self._verify(
    #         'otcextensions.sdk.kms.v1.data_key.DataKey.encrypt',
    #         self.proxy.encrypt_datakey,
    #         method_args=['INSTANCE'],
    #         expected_args=[self.proxy],
    #     )
    #
    # def test_decrypt(self):
    #     self._verify(
    #         'otcextensions.sdk.kms.v1.data_key.DataKey.decrypt',
    #         self.proxy.decrypt_datakey,
    #         method_args=['INSTANCE'],
    #         expected_args=[self.proxy],
    #     )


class TestKmsRandom(TestKmsProxy):

    def test_create(self):
        self.verify_create(
            self.proxy.generate_random, _misc.Random,
            mock_method='openstack.proxy.Proxy._create',
            method_kwargs={
                'random_data_length': 100
            },
            expected_kwargs={
                'prepend_key': False,
                'random_data_length': 100
            }
        )


class TestKmsInstanceNum(TestKmsProxy):

    def test_get(self):
        self._verify(
            'otcextensions.sdk.kms.v1.misc.InstanceNumber.fetch',
            self.proxy.get_instance_number,
            method_args=[],
            expected_args=[self.proxy],
        )


class TestKmsQuota(TestKmsProxy):

    def test_quotas(self):
        self._verify(
            'otcextensions.sdk.kms.v1.misc.Quota.list',
            self.proxy.quotas,
            method_args=[],
            expected_args=[self.proxy],
        )
