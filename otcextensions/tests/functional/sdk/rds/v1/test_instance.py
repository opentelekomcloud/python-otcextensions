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

from otcextensions import sdk


class TestInstance(base.BaseFunctionalTest):

    def setUp(self):
        super(TestInstance, self).setUp()

        sdk.register_otc_extensions(self.conn)

        self.instances = []

    def test_list(self):
        self.instances = list(self.conn.rds.instances())
        self.assertGreaterEqual(len(self.instances), 1)
        self.assertIsNotNone(self.instances[0].name)
        print(self.instances)

    def test_get_instance(self):
        if not self.instances:
            self.instances = list(self.conn.rds.instances())
        ref_instance = self.instances[0]
        instance = self.conn.rds.get_instance(ref_instance.id)

        self.assertEqual(instance.name, ref_instance.name)
        self.assertEqual(instance.id, ref_instance.id)
