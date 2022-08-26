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

from openstack import _log

from otcextensions.tests.functional.sdk.auto_scaling.v1.base import TestAs

_logger = _log.setup_logging('openstack')


class TestInstance(TestAs):

    def setUp(self):
        super(TestInstance, self).setUp()
        self.create_network()
        self.initialize_as_group_with_instance()

    def test_01_find_as_group_by_name(self):
        as_group = self.client.find_group(
            name_or_id=TestAs.AS_GROUP_NAME)
        self.assertIsNotNone(as_group)
        self.assertEqual(as_group.name, self.AS_GROUP_NAME)

    def test_02_list_as_groups(self):
        as_group_list = list(self.client.groups())
        self.assertIsNotNone(as_group_list)

    def test_03_update_as_group(self):
        new_name = self.AS_GROUP_NAME
        as_group = self.client.update_group(
            group=TestAs.AS_GROUP, name=new_name,
            desire_instance_number=0)
        self.assertIsNotNone(as_group)
        self.assertEqual(as_group.name, new_name)

    def test_04_find_as_group_by_id(self):
        find_as_group = self.conn.auto_scaling.find_group(
            name_or_id=TestAs.AS_GROUP.id
        )
        self.assertEqual(TestAs.AS_GROUP.id, find_as_group.id)
        self.assertEqual(TestAs.AS_GROUP.name, find_as_group.name)

        self.deinitialize_as_group_with_instance()
        as_group = self.client.find_group(
            name_or_id=find_as_group.name)
        self.assertIsNone(as_group)

        self.destroy_network(TestAs.network, TestAs.KP_NAME)
        vpc = self.conn.vpc.find_vpc(
            TestAs.network.get('router_id'),
            ignore_missing=True)
        self.assertIsNone(vpc)
