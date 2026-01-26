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
    gateway = "4a5d39b75bc341e89033c65e97ad5bca"

    def setUp(self):
        super(TestVpcEndpoint, self).setUp()

    def test_01_list_vpc_endpoint(self):
        self.conn.vpcep.create_endpoint(
            subnet_id='1bc849dc-4426-455a-8207-fb5f726c6ff7',
            endpoint_service_id='b002616f-f386-4da1-8118-04d5e090200f',
            vpc_id='80a6ba4b-44d7-4c57-be40-5013a1e55273',

        )
        list(self.client.vpc_endpoints(
            gateway=TestVpcEndpoint.gateway,
        ))
