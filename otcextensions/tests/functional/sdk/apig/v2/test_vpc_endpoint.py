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


class TestVpcEndpoint(TestApiG):
    gateway = ""

    def setUp(self):
        super(TestVpcEndpoint, self).setUp()

    def test_01_list_vpc_endpoint(self):
        self.conn.vpcep.create_endpoint(
            subnet_id='',
            endpoint_service_id='',
            vpc_id='',
        )
        list(self.client.vpc_endpoints(
            gateway=TestVpcEndpoint.gateway,
        ))
