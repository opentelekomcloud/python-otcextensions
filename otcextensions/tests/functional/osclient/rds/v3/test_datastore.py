#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

from openstackclient.tests.functional import base
from tempest.lib import exceptions

class TestRdsDatastore(base.TestCase):
    """Functional tests for RDS Datastore. """

    def test_datastore_list(self):
        json_output = json.loads(self.openstack(
            'rds datastore type list -f json '
        ))

        for datastore in ['MySQL', 'PostgreSQL', 'SQLServer']:
            self.assertIn(
                datastore,
                [ds['Name'] for ds in json_output]
            )

    def test_datastore_version_list(self):
        for datastore in ['MySQL', 'PostgreSQL', 'SQLServer']:
            json_output = json.loads(self.openstack(
                'rds datastore version list PostgreSQL -f json'
            ))
            self.assertIsNotNone(json_output)
            self.assertEqual(
                ['ID', 'Name'], 
                list(json_output[0].keys())
            )

    def test_invalid_datastore_version_list(self):
        self.assertRaises(
            exceptions.CommandFailed,
            self.openstack,
            'rds datastore version list invalid_ds'
        )
