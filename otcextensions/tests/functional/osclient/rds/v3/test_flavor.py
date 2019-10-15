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
import uuid

from openstackclient.tests.functional import base
from tempest.lib import exceptions

class TestRdsFlavor(base.TestCase):
    """Functional tests for RDS Flavor. """

    NAME = uuid.uuid4().hex
    OTHER_NAME = uuid.uuid4().hex

    def test_flavor_list(self):
        for datastore in ['mysql', 'postgresql', 'sqlserver']:
            json_output = json.loads(self.openstack(
                'rds datastore version list ' + datastore + ' -f json '
            ))

            for ds_ver in json_output:
                json_output = json.loads(self.openstack(
                    'rds flavor list {ds} {ver} -f json'.format(
                        ds=datastore,
                        ver=ds_ver['Name'])
                ))

                self.assertIsNotNone(json_output)
                self.assertEqual(
                    ['name', 'instance_mode', 'vcpus', 'ram'],
                    list(json_output[0].keys())
                )

    def test_invalid_datastore_flavor_list(self):
        self.assertRaises(
            exceptions.CommandFailed,
            self.openstack,
            'rds flavor list'
        )

        self.assertRaises(
            exceptions.CommandFailed,
            self.openstack,
            'rds flavor list invalid_ds 5.6'
        )

        for datastore in ['mysql', 'postgresql', 'sqlserver']:
            self.assertRaises(
                exceptions.CommandFailed,
                self.openstack,
                'rds flavor list {ds} {ver}'.format(
                    ds=datastore,
                    ver=0.0)
            )
