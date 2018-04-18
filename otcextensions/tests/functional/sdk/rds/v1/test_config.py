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
from otcextensions import sdk
from otcextensions.tests.functional import base


class TestConfig(base.BaseFunctionalTest):

    def setUp(self):
        super(TestConfig, self).setUp()

        sdk.register_otc_extensions(self.conn)

        self.config = []

    def test_list(self):
        self.config = list(self.conn.rds.configuration_groups())
        self.assertGreaterEqual(len(self.config), 1)
        self.assertIsNotNone(self.config[0].name)

    def test_get_group(self):
        if not self.config:
            self.config = list(self.conn.rds.configuration_groups())
        ref_obj = self.config[0]
        fetch_obj = self.conn.rds.get_configuration_group(ref_obj.id)

        self.assertEqual(fetch_obj.name, ref_obj.name)
        self.assertEqual(fetch_obj.id, ref_obj.id)
