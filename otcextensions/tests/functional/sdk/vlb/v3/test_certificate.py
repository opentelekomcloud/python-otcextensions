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

from otcextensions.tests.functional.sdk.vlb import TestVlb


class TestCertificate(TestVlb):
    def setUp(self):
        super(TestCertificate, self).setUp()
        self.create_certificate()

    def test_01_list_certificates(self):
        certs = list(self.client.certificates())
        self.assertGreaterEqual(len(certs), 0)

    def test_02_get_certificate(self):
        cert = self.client.get_certificate(TestVlb.certificate)
        self.assertEqual(TestVlb.certificate.name, cert.name)
        self.assertEqual(TestVlb.certificate.created_at, cert.created_at)
        self.assertEqual(TestVlb.certificate.expire_time, cert.expire_time)

    def test_03_find_certificate(self):
        cert = self.client.find_certificate(TestVlb.certificate.name)
        self.assertEqual(TestVlb.certificate.name, cert.name)
        self.assertEqual(TestVlb.certificate.created_at, cert.created_at)
        self.assertEqual(TestVlb.certificate.expire_time, cert.expire_time)

    def test_04_update_certificate(self):
        cert_updated = self.client.update_certificate(
            TestVlb.certificate,
            name=TestVlb.certificate.name + "_2_cp"
        )
        self.assertEqual(TestVlb.certificate.name, cert_updated.name)

        self.addCleanup(self.client.delete_certificate, TestVlb.certificate)