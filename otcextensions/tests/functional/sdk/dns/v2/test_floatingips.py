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
import openstack

from otcextensions.tests.functional.sdk.dns import TestDns

_logger = openstack._log.setup_logging('openstack')

class TestFloatingIps(TestDns):

    def setUp(self):
        super(TestFloatingIps, self).setUp()
        pub_net = self.conn.get_network('admin_external_net')
        self.floating_ip = self.conn.network.create_ip(
            floating_network_id=pub_net.id
        )
        self.floatingip = self.client.set_floating_ip(
            floating_ip=('eu-de:' + self.floating_ip.id),
            ptrdname='dns.ptr.test.com'
        )

    def tearDown(self):
        super(TestFloatingIps, self).tearDown()
        self.client.unset_floating_ip(
            floating_ip=self.floatingip,
        )
        self.conn.network.delete_ip(self.floating_ip)

    def test_list_floatingips(self):
        ips = self.client.floating_ips()
        self.assertIsNotNone(ips)

    def test_get_floatingip(self):
        ip = self.client.get_floating_ip(self.floatingip.id)
        self.assertEqual(ip['address'], self.floatingip['address'])

    # BUG
    # jira.tsi-dev.otc-service.com/servicedesk/customer/portal/4/OST-9283
    # def test_update_floatingip(self):
    #     ip = self.client.update_floating_ip(
    #         floating_ip=self.floatingip,
    #         ttl=500
    #     )
    #     self.assertEqual(ip['description'], 'updated')
