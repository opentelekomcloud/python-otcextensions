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


class TestBackendServerGroup(TestApiG):
    gateway = "560de602c9f74969a05ff01d401a53ed"
    vpc = "80fc1bd30db94ef49468a27f536dd2cd"
    group = None

    def setUp(self):
        super(TestBackendServerGroup, self).setUp()
        attrs = {
            "member_groups": [{
                "member_group_name": "vpc_member_group",
                "member_group_weight": 10
            }]
        }
        result = self.client.add_or_update_backend_server_group(
            gateway=TestBackendServerGroup.gateway,
            vpc_channel=TestBackendServerGroup.vpc,
            **attrs
        )
        TestBackendServerGroup.group = result[0]
        self.assertEqual(TestBackendServerGroup.group.member_group_name,
                         "vpc_member_group")

    def tearDown(self):
        super(TestBackendServerGroup, self).tearDown()
        self.client.delete_backend_server_group(
            gateway=TestBackendServerGroup.gateway,
            vpc_channel=TestBackendServerGroup.vpc,
            backend_group=TestBackendServerGroup.group
        )

    def test_01_list_backend_server_groups(self):
        found = list(self.client.backend_server_groups(
            gateway=TestBackendServerGroup.gateway,
            vpc_channel=TestBackendServerGroup.vpc))
        self.assertEqual(len(found), 1)

    def test_02_update_backend_server_group(self):
        attrs = {
            "member_group_name": "vpc_member_group",
            "member_group_weight": 50
        }
        updated = self.client.update_backend_server_group(
            gateway=TestBackendServerGroup.gateway,
            vpc_channel=TestBackendServerGroup.vpc,
            backend_group=TestBackendServerGroup.group,
            **attrs
        )
        self.assertEqual(updated.member_group_weight,
                         attrs.get("member_group_weight"))

    def test_03_get_backend_server_group(self):
        found = self.client.get_backend_server_group(
            gateway=TestBackendServerGroup.gateway,
            vpc_channel=TestBackendServerGroup.vpc,
            backend_group=TestBackendServerGroup.group)
        self.assertEqual(found.member_group_id,
                         TestBackendServerGroup.group.member_group_id)
