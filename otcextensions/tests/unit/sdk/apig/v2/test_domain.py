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
from openstack.tests.unit import base
from otcextensions.sdk.apig.v2 import domain_name

EXAMPLE = {
    "url_domain": "www.company.com",
    "id": "c5e0d5ba62a34d26ad5c709ae22c1a17",
    "status": 3,
    "min_ssl_version": "TLSv1.1",
    "is_http_redirect_to_https": False,
    "verified_client_certificate_enabled": False
}


class TestDomainName(base.TestCase):

    def test_basic(self):
        sot = domain_name.DomainName()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/'
            'api-groups/%(group_id)s/domains',
            sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = domain_name.DomainName(**EXAMPLE)
        self.assertEqual(EXAMPLE['url_domain'], sot.url_domain)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['min_ssl_version'], sot.min_ssl_version)


EXAMPLE_CERTIFICATE = {
    "ssl_name": "cert_demo",
    "url_domain": "www.example.com",
    "ssl_id": "a27be832f2e9441c8127fe48e3b5ac67",
    "id": " f6bb84ccf1c34035878aa51b7253b21c",
    "status": 3
}


class TestCertificate(base.TestCase):

    def test_basic(self):
        sot = domain_name.Certificate()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/'
            'api-groups/%(group_id)s/domains/'
            '%(domain_id)s/certificate',
            sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = domain_name.Certificate(**EXAMPLE_CERTIFICATE)
        self.assertEqual(EXAMPLE_CERTIFICATE['ssl_name'], sot.ssl_name)
        self.assertEqual(EXAMPLE_CERTIFICATE['url_domain'], sot.url_domain)
        self.assertEqual(EXAMPLE_CERTIFICATE['ssl_id'], sot.ssl_id)
        self.assertEqual(EXAMPLE_CERTIFICATE['id'], sot.id)
        self.assertEqual(EXAMPLE_CERTIFICATE['status'], sot.status)


EXAMPLE_DEBUG = {
    "sl_domain_access_enabled": True
}


class TestDomainDebug(base.TestCase):

    def test_basic(self):
        sot = domain_name.DomainDebug()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/api-groups/'
            '%(group_id)s/sl-domain-access-settings',
            sot.base_path)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = domain_name.DomainDebug(**EXAMPLE_DEBUG)
        self.assertEqual(
            EXAMPLE_DEBUG['sl_domain_access_enabled'],
            sot.sl_domain_access_enabled
        )
