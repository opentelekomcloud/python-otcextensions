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

from otcextensions.tests.functional.sdk.apig import TestApiG
import uuid


class TestGateway(TestApiG):
    gateway = None
    eip = None
    admin_external_net = None

    def setUp(self):
        super(TestGateway, self).setUp()
        self.create_gateway()

    def tearDown(self):
        super(TestGateway, self).tearDown()

    def get_attrs(self):
        all_vpc = list(self.conn.vpc.vpcs())
        vpc = all_vpc[0]
        all_subnets = list(self.conn.vpc.subnets(vpc_id=vpc.id))
        subnet = all_subnets[0]
        security_groups = list(self.conn.network.security_groups())
        security_group = security_groups[0]
        available_zone_ids = ["eu-de-01"]
        nmb = uuid.uuid4().hex[:8]
        return {
            'instance_name': 'test_gateway_{}'.format(nmb),
            'spec_id': 'BASIC',
            'vpc_id': vpc.id,
            'subnet_id': subnet.id,
            'security_group_id': security_group.id,
            'available_zone_ids': available_zone_ids,
        }

    def create_gateway(self):
        if not TestGateway.gateway:
            attrs = self.get_attrs()
            TestGateway.gateway = self.client.create_gateway(**attrs)

    def test_01_list_gateways(self):
        attrs = {
            'limit': 2
        }
        gateways = list(self.client.gateways(**attrs))
        self.assertGreater(len(gateways), 0)

    def test_02_creation_progress(self):
        found = self.client.get_gateway_progress(TestGateway.gateway)
        self.assertIsNotNone(found.progress)

    def test_03_get_gateway(self):
        found = self.client.get_gateway(TestGateway.gateway.instance_id)
        self.assertEqual(found.id, TestGateway.gateway.instance_id)
        TestGateway.gateway = found

    def test_04_update_gateway(self):
        self.client.wait_for_gateway(TestGateway.gateway)
        test_nmb = uuid.uuid4().hex[:8]
        attrs = {
            "description": test_nmb
        }
        found = self.client.update_gateway(TestGateway.gateway, **attrs)
        self.assertEqual(found.description, attrs['description'])

    def test_05_get_constraints(self):
        found = self.client.get_constraints(TestGateway.gateway.id)
        self.assertIsNotNone(found.resource_subnet_cidr)

    def test_06_enable_public_access(self):
        self.client.wait_for_gateway(TestGateway.gateway)
        attrs = {
            "bandwidth_size": "5",
            "bandwidth_charging_mode": "bandwidth"
        }
        found = self.client.enable_public_access(TestGateway.gateway.id,
                                                 **attrs)
        self.assertIsNotNone(found.bandwidth_name)

    def test_07_update_public_access(self):
        self.client.wait_for_gateway(TestGateway.gateway)
        attrs = {
            "bandwidth_size": "7",
            "bandwidth_charging_mode": "bandwidth"
        }
        found = self.client.update_public_access(TestGateway.gateway.id,
                                                 **attrs)
        self.assertIsNotNone(found.bandwidth_name)

    def test_08_disable_public_access(self):
        self.client.wait_for_gateway(TestGateway.gateway)
        self.client.disable_public_access(TestGateway.gateway.id)

    # def test_09_modify_spec(self):
    #     self.client.wait_for_gateway(TestGateway.gateway)
    #     attrs = {
    #         "spec_id" : "PROFESSIONAL"
    #     }
    #     found = self.client.modify_gateway_spec(TestGateway.gateway, **attrs)
    #     self.assertIsNotNone(found.job_id)

    # def test_10_enable_ingress(self):
    #     self.client.wait_for_gateway(TestGateway.gateway)
    #     attrs = {
    #         "bandwidth_size" : "5",
    #         "bandwidth_charging_mode" : "bandwidth"
    #     }
    #     found = self.client.enable_ingress(TestGateway.gateway.id, **attrs)
    #     self.assertIsNotNone(found.job_id)
    #
    # def test_11_update_ingress(self):
    #     self.client.wait_for_gateway(TestGateway.gateway)
    #     attrs = {
    #         "bandwidth_size" : "7",
    #         "bandwidth_charging_mode" : "bandwidth"
    #     }
    #     found = self.client.update_ingress(TestGateway.gateway.id, **attrs)
    #     self.assertIsNotNone(found.job_id)
    #
    # def test_12_disable_ingress(self):
    #     self.client.wait_for_gateway(TestGateway.gateway)
    #     self.client.disable_ingress(TestGateway.gateway.id)

    # def test_13_bind_eip(self):
    #     admin_external_net = self.conn.network.find_network(
    #         name_or_id='admin_external_net')
    #     self.assertIsNotNone(admin_external_net)
    #     floating_ip = self.conn.network.create_ip(
    #         floating_network_id=admin_external_net.id)
    #     self.client.wait_for_gateway(TestGateway.gateway)
    #     attrs = {
    #         "eip_id": floating_ip.id
    #     }
    #     TestGateway.eip = floating_ip
    #     TestGateway.admin_external_net = admin_external_net
    #     self.client.bind_eip(TestGateway.gateway, **attrs)
    #
    # def test_14_unbind_eip(self):
    #     self.client.unbind_eip(TestGateway.gateway)
    #     self.conn.network.delete_ip(TestGateway.eip)

    def test_15_delete_gateway(self):
        self.client.delete_gateway(TestGateway.gateway)
