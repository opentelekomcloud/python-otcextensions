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
from otcextensions.sdk.apig.v2 import ssl_certificate

EXAMPLE_CERT = {
    'id': 'cert-001',
    'name': 'my-cert',
    'cert_content': '---CERT---',
    'private_key': '---KEY---',
    'type': 'server',
    'instance_id': 'gw-001',
    'trusted_root_ca': '---CA---',
    'project_id': 'proj-001',
    'common_name': 'example.com',
    'san': ['www.example.com', 'api.example.com'],
    'not_after': '2030-01-01T00:00:00Z',
    'signature_algorithm': 'RSA-SHA256',
    'create_time': '2024-01-01T00:00:00Z',
    'update_time': '2024-06-01T00:00:00Z',
    'is_has_trusted_root_ca': True,
    'version': 3,
    'organization': ['Example Org'],
    'organizational_unit': ['IT'],
    'locality': ['City'],
    'state': ['State'],
    'country': ['US'],
    'not_before': '2023-01-01T00:00:00Z',
    'serial_number': '00:AB:CD',
    'issuer': ['CA Org', 'Root CA']
}


class TestSslCertificate(base.TestCase):

    def test_basic(self):
        sot = ssl_certificate.SslCertificate()
        self.assertEqual('/apigw/certificates', sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_commit)
        self.assertEqual('certs', sot.resources_key)

    def test_make_it(self):
        sot = ssl_certificate.SslCertificate(**EXAMPLE_CERT)
        self.assertEqual('cert-001', sot.id)
        self.assertEqual('my-cert', sot.name)
        self.assertEqual('---CERT---', sot.cert_content)
        self.assertEqual('---KEY---', sot.private_key)
        self.assertEqual('server', sot.type)
        self.assertEqual('gw-001', sot.instance_id)
        self.assertEqual('---CA---', sot.trusted_root_ca)
        self.assertEqual('proj-001', sot.project_id)
        self.assertEqual('example.com', sot.common_name)
        self.assertEqual(['www.example.com', 'api.example.com'], sot.san)
        self.assertEqual('2030-01-01T00:00:00Z', sot.not_after)
        self.assertEqual('RSA-SHA256', sot.signature_algorithm)
        self.assertEqual('2024-01-01T00:00:00Z', sot.create_time)
        self.assertEqual('2024-06-01T00:00:00Z', sot.update_time)
        self.assertTrue(sot.is_has_trusted_root_ca)
        self.assertEqual(3, sot.version)
        self.assertEqual(['Example Org'], sot.organization)
        self.assertEqual(['IT'], sot.organizational_unit)
        self.assertEqual(['City'], sot.locality)
        self.assertEqual(['State'], sot.state)
        self.assertEqual(['US'], sot.country)
        self.assertEqual('2023-01-01T00:00:00Z', sot.not_before)
        self.assertEqual('00:AB:CD', sot.serial_number)
        self.assertEqual(['CA Org', 'Root CA'], sot.issuer)
