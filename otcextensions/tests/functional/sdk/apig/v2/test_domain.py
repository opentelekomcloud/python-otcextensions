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
import uuid
import openstack

from otcextensions.tests.functional.sdk.apig import TestApiG
from otcextensions.tests.ssl import SelfSignedCertificateGenerator

_logger = openstack._log.setup_logging('openstack')


class TestDomain(TestApiG):

    def setUp(self):
        super(TestDomain, self).setUp()
        self.network_client = self.conn.dns
        self.suffix = uuid.uuid4().hex[:4]
        self.zone_name = self.suffix + 'dns.sdk-apig-zone-public.com.'
        self.create_gateway()
        self.gateway_id = TestDomain.gateway.id
        # self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"

        group_attrs = {
            "name": f"api_group_{self.suffix}",
            "remark": f"API group {self.suffix}"
        }
        self.group = self.client.create_api_group(
            gateway=self.gateway_id,
            **group_attrs
        )
        self.assertIsNotNone(self.group.id)

        self.zone = self.network_client.create_zone(
            name=self.zone_name
        )
        self.network_client.wait_for_zone(self.zone)

        attrs = {
            "url_domain": self.zone.name
        }
        self.domain = self.client.bind_domain_name(
            gateway=self.gateway_id,
            group=self.group.id,
            **attrs
        )
        self.assertIsNotNone(self.group.id)

        generator = SelfSignedCertificateGenerator(self.zone_name)
        generator.generate_private_key()
        generator.generate_certificate()
        attrs = {
            "name": f"cert_demo_{self.suffix}",
            "private_key": generator.get_private_key(),
            "cert_content": generator.get_certificate()
        }
        self.bind = self.client.create_certificate_for_domain_name(
            gateway=self.gateway_id,
            group=self.group.id,
            domain=self.domain.id,
            **attrs
        )
        self.assertEqual(self.bind.name, attrs["name"])

        self.addCleanup(self.delete_gateway())
        self.addCleanup(
            self.client.delete_api_group,
            gateway=self.gateway_id,
            api_group=self.group.id,
        )
        self.addCleanup(
            self.client.delete_certificate,
            certificate=self.bind.ssl_id,
        )
        self.addCleanup(
            self.client.unbind_domain_name,
            gateway=self.gateway_id,
            group=self.group.id,
            domain=self.domain.id,
        )

    def tearDown(self):
        if self.zone:
            try:
                self.network_client.delete_zone(self.zone)
                self.network_client.wait_for_delete_zone(self.zone)
            except openstack.exceptions.SDKException as e:
                _logger.warning('Got exception during clearing resources %s'
                                % e.message)
        super(TestDomain, self).tearDown()

    def test_update_domain_name_bound(self):
        attrs = {
            "min_ssl_version": "TLSv1.2"
        }
        updated = self.client.update_domain_name_bound(
            gateway=self.gateway_id,
            group=self.group.id,
            domain=self.domain.id,
            **attrs
        )
        self.assertEqual(updated.min_ssl_version, attrs["min_ssl_version"])

    # def test_unbind_certificate_from_domain(self):
    #     unbind = self.client.unbind_certificate_from_domain_name(
    #         gateway=self.gateway_id,
    #         group=self.group.id,
    #         domain=self.domain.id,
    #         certificate=self.bind.id,
    #     )
    #     self.assertIsNotNone(unbind)

    def test_disable_debug(self):
        debug = self.client.enable_debug_domain_name(
            gateway=self.gateway_id,
            group=self.group.id,
            domain=self.domain.id,
            enable=False,
        )
        self.assertEqual(
            debug.sl_domain_access_enabled,
            False
        )

    def test_get_bound_certificate(self):
        cert = self.client.get_bound_certificate(
            gateway=self.gateway_id,
            group=self.group.id,
            domain=self.domain.id,
            certificate=self.bind.ssl_id,
        )
        self.assertEqual(
            cert.id,
            self.bind.ssl_id
        )
