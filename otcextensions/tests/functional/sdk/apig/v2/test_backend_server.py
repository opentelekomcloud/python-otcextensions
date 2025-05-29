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


class TestBackendServer(TestApiG):
    gateway = "560de602c9f74969a05ff01d401a53ed"
    vpc = "80fc1bd30db94ef49468a27f536dd2cd"
    group = "vpc_member_group"
    server = None

    def setUp(self):
        super(TestBackendServer, self).setUp()
        attrs = {
            "members": [{
                "host": "192.168.2.25",
                "weight": 1,
                "member_group_name": "vpc_member_group"
            }]
        }
        result = self.client.add_or_update_backend_servers(
            gateway=TestBackendServer.gateway,
            vpc_channel=TestBackendServer.vpc,
            **attrs
        )
        TestBackendServer.server = result[0]
        self.assertIsNotNone(result[0].id)

    def tearDown(self):
        super(TestBackendServer, self).tearDown()
        self.client.remove_backend_server(
            gateway=TestBackendServer.gateway,
            vpc_channel=TestBackendServer.vpc,
            backend_server=TestBackendServer.server.id
        )

    def test_01_list_backend_servers(self):
        found = list(self.client.list_backend_servers(
            gateway=TestBackendServer.gateway,
            vpc_channel=TestBackendServer.vpc,
        ))
        self.assertEqual(1, len(found))

    def test_02_update_backend_server(self):
        attrs = {
            "member_group_name": "vpc_member_group",
            "members": [{
                "host": "192.168.2.25",
                "weight": 2,
                "is_backup": True,
                "member_group_name": "vpc_member_group"
            }]
        }
        updated = self.client.update_backend_server(
            gateway=TestBackendServer.gateway,
            vpc_channel=TestBackendServer.vpc,
            **attrs
        )
        self.assertEqual(updated[0].is_backup, True)

    def test_03_enable_backend_server(self):
        attrs = {
            "member_ids": [TestBackendServer.server.id]
        }
        self.client.enable_backend_server(
            gateway=TestBackendServer.gateway,
            vpc_channel=TestBackendServer.vpc,
            backend_server=TestBackendServer.server.id,
            **attrs
        )

    def test_04_disable_backend_server(self):
        attrs = {
            "member_ids": [TestBackendServer.server.id]
        }
        self.client.disable_backend_server(
            gateway=TestBackendServer.gateway,
            vpc_channel=TestBackendServer.vpc,
            backend_server=TestBackendServer.server.id,
            **attrs
        )
