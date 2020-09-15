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

from unittest import mock

from otcextensions.sdk.identity.v3 import _proxy
from otcextensions.sdk.identity.v3 import credential

from openstack.tests.unit import test_proxy_base


class TestIdentityProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestIdentityProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestIdentityCredential(TestIdentityProxy):
    def test_credential_create(self):
        self.verify_create(self.proxy.create_credential, credential.Credential,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id',
                                            'prepend_key': True})

    def test_credential_delete(self):
        self.verify_delete(self.proxy.delete_credential,
                           credential.Credential, True)

    def test_credential_find(self):
        self.verify_find(self.proxy.find_credential, credential.Credential)

    def test_credential_get(self):
        self.verify_get(self.proxy.get_credential, credential.Credential)

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_credentials_endpoint')
    def test_credentials(self, epo_mock):
        epo_mock.return_value = 'fake'
        self.verify_list(
            self.proxy.credentials,
            credential.Credential,
        )
        epo_mock.assert_called_with()

    def test_credential_update(self):
        self.verify_update(self.proxy.update_credential, credential.Credential)
