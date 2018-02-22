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


class TestBackup(base.BaseFunctionalTest):

    def setUp(self):
        super(TestBackup, self).setUp()

        sdk.register_otc_extensions(self.conn)

        self.backups = []

    def test_list(self):
        self.backups = list(self.conn.rds.backups())
        self.assertGreaterEqual(len(self.backups), 0)
        # self.assertIsNotNone(self.flavors[0].name)

    # def test_get_flavor(self):
    #     if not self.flavors:
    #         self.flavors = list(self.conn.rds.flavors())
    #     ref_flavor = self.flavors[0]
    #     flavor = self.conn.rds.get_flavor(ref_flavor.str_id)
    #
    #     self.assertEqual(flavor.name, ref_flavor.name)
    #     self.assertEqual(flavor.ram, ref_flavor.ram)
    #     self.assertEqual(flavor.str_id, ref_flavor.str_id)
