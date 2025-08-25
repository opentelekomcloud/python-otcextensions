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
from pathlib import Path
from otcextensions.tests.functional.sdk.apig import TestApiG


class TestSSLCert(TestApiG):
    gateway_id = "560de602c9f74969a05ff01d401a53ed"
    group_id = "ce973ff83ce54ef192c80bde884aa0ac"
    domain = None
    cert_id = ""

    def setUp(self):
        super(TestSSLCert, self).setUp()
        attrs = {
            "name": "cert_demo",
            "cert_content": Path("/mnt/c/Users/sand1/fullchain.pem")
            .read_text().replace('\r\n', '\n'),
            "private_key": Path("/mnt/c/Users/sand1/privkey.pem")
            .read_text().replace('\r\n', '\n'),
            "type": "instance",
            "instance_id": TestSSLCert.gateway_id
        }
        certificate = self.client.create_ssl_certificate(**attrs)
        self.assertIsNotNone(certificate.id)
        TestSSLCert.cert_id = certificate.id
        self.addCleanup(
            self.client.delete_ssl_certificate,
            ssl_certificate=certificate.id,
        )
        attrs = {
            "url_domain": "test-domain-ssl-cert.com"
        }
        domain = self.client.bind_domain_name(
            gateway=TestSSLCert.gateway_id,
            group=TestSSLCert.group_id,
            **attrs
        )
        TestSSLCert.domain = domain
        self.addCleanup(
            self.client.unbind_domain_name,
            gateway=TestSSLCert.gateway_id,
            group=TestSSLCert.group_id,
            domain=TestSSLCert.domain.id,
        )

    def test_get_ssl_certificate(self):
        found = self.client.get_ssl_certificate(
            ssl_certificate=TestSSLCert.cert_id)
        self.assertEqual(found.id, TestSSLCert.cert_id)

    def test_list_ssl_certificates(self):
        attrs = {
            "limit": 10,
            "offset": 0,
            "type": "instance",
            "instance_id": TestSSLCert.gateway
        }
        found = list(self.client.ssl_certificates(**attrs))
        self.assertGreater(len(found), 0)

    def test_update_ssl_certificate(self):
        attrs = {
            "name": "cert_demo",
            "cert_content": Path("/mnt/c/Users/sand1/fullchain.pem")
            .read_text().replace('\r\n', '\n'),
            "private_key": Path("/mnt/c/Users/sand1/privkey.pem")
            .read_text().replace('\r\n', '\n'),
        }
        result = self.client.update_ssl_certificate(
            ssl_certificate=TestSSLCert.cert_id,
            **attrs
        )
        self.assertEqual(result.name, attrs["name"])

    def test_bind_domain_to_cert(self):
        attrs = {
            "certificate_ids": [TestSSLCert.cert_id]
        }
        self.client.bind_domain_to_certificate(
            gateway=TestSSLCert.gateway_id,
            group=TestSSLCert.group_id,
            domain=TestSSLCert.domain.id,
            **attrs
        )

    def test_unbind_domain_from_cert(self):
        attrs = {
            "certificate_ids": [TestSSLCert.cert_id]
        }
        self.client.unbind_domain_from_certificate(
            gateway=TestSSLCert.gateway_id,
            group=TestSSLCert.group_id,
            domain=TestSSLCert.domain.id,
            **attrs
        )
