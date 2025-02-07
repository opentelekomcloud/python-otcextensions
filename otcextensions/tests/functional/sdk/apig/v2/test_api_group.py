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


class TestApiGroup(TestApiG):
    api_group = None

    def setUp(self):
        super(TestApiGroup, self).setUp()
        self.create_gateway()

    def test_01_create_api_group(self):
        attrs = {
            "name": "api_group_001",
            "remark": "API group 1"
        }
        created = self.client.create_api_group(gateway=TestApiG.gateway,
                                               **attrs)
        self.assertIsNotNone(created.id)
        TestApiGroup.api_group = created

    def test_02_get_api_group(self):
        found = self.client.get_api_group(
            gateway=TestApiG.gateway,
            api_group=TestApiGroup.api_group.id)
        self.assertEqual(TestApiGroup.api_group.name, found.name)

    def test_03_update_api_group(self):
        new_remark = 'Brand new remark'
        attrs = {
            'name': TestApiGroup.api_group.name,
            'remark': new_remark
        }
        updated = self.client.update_api_group(
            gateway=TestApiG.gateway,
            api_group=TestApiGroup.api_group.id,
            **attrs)
        self.assertEqual(updated.remark, new_remark)

    def test_04_list_api_group(self):
        groups = list(self.client.api_groups(gateway=TestApiG.gateway))
        self.assertGreater(len(groups), 1)


    def test_05_verify_api_group(self):
        attrs = {
            "group_name" : "api_group_001"
        }
        result = self.client.verify_api_group_name(gateway=TestApiG.gateway)

    def test_06_delete_api_group(self):
        self.client.delete_api_group(gateway=TestApiG.gateway,
                                     api_group=TestApiGroup.api_group)
        self.delete_gateway()
