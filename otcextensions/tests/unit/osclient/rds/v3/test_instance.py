#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
import mock
# from osc_lib import utils as common_utils

from otcextensions.osclient.rds.v3 import instance
from otcextensions.tests.unit.osclient.rds.v3 import fakes as rds_fakes


class TestListDatabaseInstances(rds_fakes.TestRds):

    column_list_headers = [
        'ID', 'Name', 'Datastore Type', 'Datastore Version', 'Status',
        'Flavor_ref', 'Type', 'Size', 'Region'
    ]

    def setUp(self):
        super(TestListDatabaseInstances, self).setUp()

        self.cmd = instance.ListDatabaseInstances(self.app, None)

        self.app.client_manager.rds.instances = mock.Mock()

        self.objects = self.instance_mock.create_multiple(3)
        self.object_data = []
        for s in self.objects:
            self.object_data.append(
                (s.id, s.name, s.datastore['type'], s.datastore['version'],
                 s.status, s.flavor_ref, s.type, s.volume['size'], s.region))

    def test_list(self):
        arglist = []

        verifylist = []

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.instances.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.instances.assert_called()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(tuple(self.object_data), tuple(data))


class TestShowDatabaseInstance(rds_fakes.TestRds):

    column_list_headers = [
        'datastore', 'flavor_ref', 'id', 'name', 'region'
        'status', 'volume'
    ]

    def setUp(self):
        super(TestShowDatabaseInstance, self).setUp()

        self.cmd = instance.ShowDatabaseInstance(self.app, None)

        self.app.client_manager.rds.find_instance = mock.Mock()

        self.object = self.instance_mock.create_one()

        self.object_data = (
            self.object.datastore,
            self.object.flavor_ref,
            self.object.id,
            self.object.name,
            self.object.region,
            self.object.status,
            self.object.volume,
        )

    def test_show(self):
        arglist = [
            'test_instance',
        ]

        verifylist = [
            ('instance', 'test_instance'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.find_instance.side_effect = [self.object]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.app.client_manager.rds.find_instance.assert_called()

        # self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.object_data, data)


class TestDeleteDatabaseInstance(rds_fakes.TestRds):
    def setUp(self):
        super(TestDeleteDatabaseInstance, self).setUp()

        self.cmd = instance.DeleteDatabaseInstance(self.app, None)

        self.app.client_manager.rds.delete_instance = mock.Mock()

    def test_delete(self):
        arglist = [
            'test_obj',
        ]

        verifylist = [
            ('instance', 'test_obj'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.delete_instance.side_effect = [True]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.delete_instance.assert_called()


class TestCreateDatabaseInstance(rds_fakes.TestRds):
    def setUp(self):
        super(TestCreateDatabaseInstance, self).setUp()

        self.cmd = instance.CreateDatabaseInstance(self.app, None)

        self.app.client_manager.rds.find_flavor = mock.Mock()
        self.app.client_manager.rds.create_instance = mock.Mock()

        self.instance = self.instance_mock.create_one()
        self.flavor = self.flavor_mock.create_one()
        # self.instance.resize = mock.Mock()

        # self.instance._update(project_id='123')

    def test_action(self):
        arglist = [
            'inst_name', 'test-flavor', '--availability_zone', 'test-az-01',
            '--datastore', 'MySQL', '--datastore_version', '5.7',
            '--network_id', 'test-vpc-id', '--subnet_id', 'test-subnet-id',
            '--security_group', 'test-subnet-id', '--volume_type', 'ULTRAHIGH',
            '--size', '100', '--password', 'testtest', '--region',
            'test-region'
        ]

        verifylist = [('name', 'inst_name'), ('flavor_ref', 'test-flavor'),
                      ('availability_zone', 'test-az-01'),
                      ('datastore', 'MySQL'), ('datastore_version', '5.7'),
                      ('vpc_id', 'test-vpc-id'),
                      ('subnet_id', 'test-subnet-id'),
                      ('security_group_id', 'test-subnet-id'),
                      ('volume_type', 'ULTRAHIGH'), ('size', 100),
                      ('password', 'testtest'), ('region', 'test-region')]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.create_instance.side_effect = [
            self.instance
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.create_instance.assert_called()
