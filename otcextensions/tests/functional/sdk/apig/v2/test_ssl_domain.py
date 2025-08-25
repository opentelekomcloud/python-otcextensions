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


class TestSSLDomain(TestApiG):
    gateway_id = "560de602c9f74969a05ff01d401a53ed"
    cert_id = ""
    domain = None
    group_id = "ce973ff83ce54ef192c80bde884aa0ac"

    def setUp(self):
        super(TestSSLDomain, self).setUp()
        attrs = {
            "name": "cert_demo",
            "cert_content": Path("/mnt/c/Users/sand1/fullchain.pem")
            .read_text().replace('\r\n', '\n'),
            "private_key": Path("/mnt/c/Users/sand1/privkey.pem")
            .read_text().replace('\r\n', '\n'),
            "type": "instance",
            "instance_id": TestSSLDomain.gateway_id
        }
        certificate = self.client.create_ssl_certificate(**attrs)
        self.assertIsNotNone(certificate.id)
        TestSSLDomain.cert_id = certificate.id
        self.addCleanup(
            self.client.delete_ssl_certificate,
            ssl_certificate=certificate.id,
        )
        attrs = {
            "url_domain": "test-domain-ssl-cert.com"
        }
        domain = self.client.bind_domain_name(
            gateway=TestSSLDomain.gateway_id,
            group=TestSSLDomain.group_id,
            **attrs
        )
        TestSSLDomain.domain = domain
        self.addCleanup(
            self.client.unbind_domain_name,
            gateway=TestSSLDomain.gateway_id,
            group=TestSSLDomain.group_id,
            domain=TestSSLDomain.domain.id,
        )

    def test_list_domain_for_cert(self):
        result = list(self.client.domains_for_certificate(
            ssl_certificate=TestSSLDomain.cert_id
        ))
        self.assertEqual(len(result), 0)

    def test_bind_certificates_for_domain(self):
        attrs = {
            "domains": [{
                "domain": "test-domain-ssl-cert.com",
                "instance_ids": [TestSSLDomain.gateway_id]
            }]
        }
        self.client.bind_ssl_certificates_for_domain(
            ssl_certificate=TestSSLDomain.cert_id,
            **attrs
        )

    def test_unbind_certificates_for_domain(self):
        attrs = {
            "domains": [{
                "domain": "test-domain-ssl-cert.com",
                "instance_ids": [TestSSLDomain.gateway_id]
            }]
        }
        self.client.unbind_ssl_certificates_for_domain(
            ssl_certificate=TestSSLDomain.cert_id,
            **attrs
        )
