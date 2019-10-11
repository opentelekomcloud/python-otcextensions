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
                'rds configuration show {id} '
                '-f json'.format(id=self.NAME)
            )
        )
        self.assertTrue(id, json_output['id'])

        self.openstack(
            'rds configuration set '
            '--value max_connections=15 '
            '{name}'.format(name=self.NAME)
        )

    def test_create(self):
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
        self.assertIsNotNone(json_output)
        id = json_output['id']
        self.addCleanup(self.openstack, 'rds configuration delete ' + id)

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
        self.assertIsNotNone(json_output)
        self.assertEqual(name, json_output['name'])
        id = json_output['id']
        self.addCleanup(self.openstack, 'rds configuration delete ' + id)

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
                '-f json'.format(cfg=json_output[0]['ID'])
            )
        )
        self.assertIsNotNone(json_output)

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
        self.assertIsNotNone(json_output)
        id = json_output['id']
        self.addCleanup(self.openstack, 'rds configuration delete ' + id)

        self.openstack(
            'rds configuration set '
            '{name} '
            '--value max_connections=10 '
            '--value autocommit=OFF'.format(name=name)
        )
        self.assertTrue(True)
