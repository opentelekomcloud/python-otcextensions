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
from tempest.lib.exceptions import CommandFailed

class TestRdsConfiguration(base.TestCase):
    """Functional tests for RDS Configurations. """

    NAME = uuid.uuid4().hex

    def test_list(self):
        json_output = json.loads(
            self.openstack('rds configuration list -f json '))
        self.assertIsNotNone(json_output)

    def test_show(self):
        json_output = json.loads(
            self.openstack('rds configuration list -f json'))

        json_output = json.loads(
            self.openstack(
                'rds configuration show {cfg} '
                '-f json'.format(
                    cfg=json_output[0]['ID']
                )

            )
        )

        self.assertIsNotNone(json_output['id'])

    def test_show_with_invalid_cfg(self):
        self.assertRaises(
            CommandFailed,
            self.openstack,
            'rds configuration show'
        )

        self.assertRaises(
            CommandFailed,
            self.openstack,
            'rds configuration show invalid_cfg_id'
        )

    def test_long(self):
        json_output = json.loads(
            self.openstack(
                'rds configuration create '
                '--datastore-type postgresql '
                '--datastore-version 9.6 '
                '--value max_connections=10 '
                '{name} -f json'.format(name=self.NAME)
            )
        )
        id = json_output['id']
        self.addCleanup(self.openstack, 'rds configuration delete ' + id)

        json_output = json.loads(
            self.openstack(
                'rds configuration show {id} '
                '-f json'.format(id=id)
            )
        )
        self.assertTrue(self.NAME, json_output['name'])

        json_output = json.loads(
            self.openstack(
                'rds configuration show {name} '
                '-f json'.format(name=self.NAME)
            )
        )
        self.assertTrue(id, json_output['id'])

        self.openstack(
            'rds configuration set '
            '--value max_connections=15 '
            '{name}'.format(name=self.NAME)
        )

    def test_create(self):
        for datastore in ['MySQL', 'PostgreSQL', 'SQLServer']:
            json_output = json.loads(self.openstack(
                'rds datastore version list ' + datastore + ' -f json '
            ))

            for ds_ver in json_output:
                json_output = self._create_configuration(datastore, ds_ver['Name'])
                id = json_output['id']
                self.addCleanup(self.openstack, 'rds configuration delete ' + id)
                self.assertIsNotNone(json_output)

    def test_delete(self):
        for datastore in ['MySQL', 'PostgreSQL', 'SQLServer']:
            json_output = json.loads(self.openstack(
                'rds datastore version list ' + datastore + ' -f json '
            ))

            for ds_ver in json_output:
                json_output = self._create_configuration(datastore, ds_ver['Name'])
                id = json_output['id']
                self.openstack('rds configuration delete ' + id)

                self.assertRaises(
                    CommandFailed,
                    self.openstack, 
                    'rds configuration show ' + id)


    def test_create_with_value(self):
        name = uuid.uuid4().hex
        json_output = json.loads(
            self.openstack(
                'rds configuration create '
                '{name} '
                '--datastore-type MySQL '
                '--datastore-version 5.7 '
                '--value max_connections=10 '
                '--value autocommit=OFF '
                '-f json'.format(name=name)

            )
        )
        id = json_output['id']
        self.addCleanup(self.openstack, 'rds configuration delete ' + id)
        self.assertIsNotNone(json_output)
        self.assertEqual(name, json_output['name'])

    def test_create_with_invalid_values(self):
        self.assertRaises(
            CommandFailed,
            self.openstack,
            'rds configuration create '
            '--datastore-type MySQL '
            '--datastore-version 5.7 '
        )

        self.assertRaises(
            CommandFailed,
            self.openstack,
            'rds configuration create '
            'test-cfg '
            '--datastore-type YourSQL '
            '--datastore-version 5.7 '
        )

        self.assertRaises(
            CommandFailed,
            self.openstack,
            'test-cfg '
            'rds configuration create '
            '--datastore-type MySQL '
            '--datastore-version 0.0 '
        )

        self.assertRaises(
            CommandFailed,
            self.openstack,
            'rds configuration create '
            'test-cfg '
            '--datastore-typee MySQL '
            '--datastore-version 5.7 '
        )

    def test_config_param_list(self):
        json_output = json.loads(
            self.openstack(
                'rds configuration list -f json'
            )
        )
        json_output = json.loads(
            self.openstack(
                'rds configuration parameter list '
                '{cfg} '
                '-f json'.format(
                    cfg=json_output[0]['ID'])
            )
        )
        self.assertIsNotNone(json_output)

    def test_invalid_config_param_list(self):
        self.assertRaises(
            CommandFailed,
            self.openstack,
            'rds configuration parameter list'
        )

        self.assertRaises(
            CommandFailed,
            self.openstack,
            'rds configuration parameter list '
            'invalid_cfg_id'
        )


    def test_config_set(self):
        name = uuid.uuid4().hex
        json_output = json.loads(
            self.openstack(
                'rds configuration create '
                '{name} '
                '--datastore-type MySQL '
                '--datastore-version 5.7 '
                '-f json'.format(name=name)
            )
        )
        id = json_output['id']
        self.addCleanup(self.openstack, 'rds configuration delete ' + id)
        self.assertIsNotNone(json_output)

        self.openstack(
            'rds configuration set '
            '{name} '
            '--value max_connections=10 '
            '--value autocommit=OFF'.format(name=name)
        )
        self.assertTrue(True)

    def _create_configuration(self, datastore, version, cfg_param_cmd=None):
        name = uuid.uuid4().hex
        cmd = ('rds configuration create '
                '--datastore-type {ds} '
                '--datastore-version {ver} '
                '{name} '.format(
                    name=name,
                    ds=datastore,
                    ver=version)
            )
        if cfg_param_cmd:
            cmd = '{} {}'.format(cmd, cfg_param_cmd)
                
        json_output = json.loads(
            self.openstack(cmd + ' -f json'))
        return json_output
