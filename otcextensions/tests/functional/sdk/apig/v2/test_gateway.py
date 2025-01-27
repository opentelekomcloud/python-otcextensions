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
from otcextensions.sdk.apig.v2 import gateway
import uuid


class TestGateway(TestApiG):
    gateway = None

    def setUp(self):
        super(TestGateway, self).setUp()
        self.create_gateway()

    def tearDown(self):
        super(TestGateway, self).tearDown()

    def get_attrs(self):
        all_vpc = list(self.conn.vpc.vpcs())
        vpc = all_vpc[0]
        all_subnets = list(self.conn.vpc.subnets(vpc_id = vpc.id))
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

    def test_05_delete_gateway(self):
        self.client.delete_gateway(TestGateway.gateway)
