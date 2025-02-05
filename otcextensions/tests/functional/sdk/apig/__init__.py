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

from otcextensions.tests.functional import base
import uuid


class TestApiG(base.BaseFunctionalTest):
    gateway = None

    def setUp(self):
        super(TestApiG, self).setUp()
        self.client = self.conn.apig

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
        if not TestApiG.gateway:
            attrs = self.get_attrs()
            TestApiG.gateway = self.client.create_gateway(**attrs)
            TestApiG.gateway = self.client.wait_for_gateway(
                TestApiG.gateway.instance_id)

    def delete_gateway(self):
        if TestApiG.gateway:
            self.client.delete_gateway(TestApiG.gateway)
