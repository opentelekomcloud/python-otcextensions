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

from otcextensions.sdk.waf.v1 import _proxy
from otcextensions.sdk.waf.v1 import certificate

from openstack.tests.unit import test_proxy_base


class TestWafProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestWafProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestWafCertificate(TestWafProxy):
    def test_certificate_create(self):
        self.verify_create(self.proxy.create_certificate,
                           certificate.Certificate,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id',
                                            'prepend_key': False})

    def test_certificate_delete(self):
        self.verify_delete(self.proxy.delete_certificate,
                           certificate.Certificate, True)

    def test_certificate_find(self):
        self.verify_find(self.proxy.find_certificate, certificate.Certificate)

    def test_certificate_get(self):
        self.verify_get(self.proxy.get_certificate, certificate.Certificate)

    def test_certificates(self):
        self.verify_list(self.proxy.certificates, certificate.Certificate)

    def test_certificate_update(self):
        self.verify_update(self.proxy.update_certificate,
                           certificate.Certificate)
