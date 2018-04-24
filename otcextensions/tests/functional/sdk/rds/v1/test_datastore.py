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


class TestDatastore(base.BaseFunctionalTest):

    def setUp(self):
        super(TestDatastore, self).setUp()

        sdk.register_otc_extensions(self.conn)

    def test_datastores_mysql(self):
        datastores = list(self.conn.rds.datastores('MySQL'))
        self.assertGreaterEqual(len(datastores), 1)
        self.assertIsNotNone(datastores[0].name)

    def test_datastores_pgsql(self):
        datastores = list(self.conn.rds.datastores('PostgreSQL'))
        self.assertGreaterEqual(len(datastores), 1)
        self.assertIsNotNone(datastores[0].name)

    def test_datastores_sqlserver(self):
        datastores = list(self.conn.rds.datastores('SQLServer'))
        self.assertGreaterEqual(len(datastores), 1)
        self.assertIsNotNone(datastores[0].name)
