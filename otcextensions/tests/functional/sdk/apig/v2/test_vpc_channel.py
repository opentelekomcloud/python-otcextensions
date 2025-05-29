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


class TestVpcChannel(TestApiG):
    lb_channel = None
    gateway = "560de602c9f74969a05ff01d401a53ed"

    def setUp(self):
        super(TestVpcChannel, self).setUp()
        attrs = {
            "balance_strategy": 1,
            "member_type": "ip",
            "name": "VPC_demo",
            "port": 22,
        }
        vpc = self.client.create_vpc_channel(
            gateway=TestVpcChannel.gateway,
            **attrs)
        self.assertIsNotNone(vpc.id)
        TestVpcChannel.lb_channel = vpc

    def tearDown(self):
        super(TestVpcChannel, self).tearDown()
        self.client.delete_vpc_channel(
            gateway=TestVpcChannel.gateway,
            vpc_channel=TestVpcChannel.lb_channel.id)

    def test_01_get_vpc_channel(self):
        found = self.client.get_vpc_channel(
            gateway=TestVpcChannel.gateway,
            vpc_channel=TestVpcChannel.lb_channel['id']
        )
        self.assertIsNotNone(found.name)

    def test_02_vpc_channels(self):
        found = list(self.client.vpc_channels(gateway=TestVpcChannel.gateway))
        self.assertEqual(len(found), 1)

    def test_03_update_vpc_channel(self):
        attrs = {
            "balance_strategy": 1,
            "member_type": "ip",
            "name": "VPC_demo",
            "port": 222,
        }
        updated = self.client.update_vpc_channel(
            gateway=TestVpcChannel.gateway,
            vpc_channel=TestVpcChannel.lb_channel['id'],
            **attrs)
        self.assertEqual(updated.port, attrs["port"])

    def test_04_update_vpc_channel_healthcheck(self):
        attrs = {
            "http_code": "200",
            "path": "/vpc/demo",
            "port": 22,
            "method": "GET",
            "protocol": "http",
            "threshold_abnormal": 5,
            "threshold_normal": 2,
            "time_interval": 10,
            "timeout": 5,
            "enable_client_ssl": False
        }
        self.client.modify_vpc_channel_healthcheck(
            gateway=TestVpcChannel.gateway,
            vpc_channel=TestVpcChannel.lb_channel['id'],
            **attrs
        )
