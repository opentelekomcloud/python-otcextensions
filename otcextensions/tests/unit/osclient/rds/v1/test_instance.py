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

from otcextensions.osclient.rds.v1 import instance
from otcextensions.tests.unit.osclient.rds.v1 import fakes as rds_fakes


class TestListDatabaseInstances(rds_fakes.TestRds):

    column_list_headers = [
        'ID', 'Name', 'Datastore Type',
        'Datastore Version', 'Status',
        'Flavor ID', 'Size', 'Region']

    def setUp(self):
        super(TestListDatabaseInstances, self).setUp()

        self.cmd = instance.ListDatabaseInstances(self.app, None)

        self.app.client_manager.rds.instances = mock.Mock()

        self.objects = self.instance_mock.create_multiple(3)
        self.object_data = []
        for s in self.objects:
            self.object_data.append((
                s.id,
                s.name,
                s.datastore['type'],
                s.datastore['version'],
                s.status,
                s.flavor['id'],
                s.volume['size'],
                s.region
                # s.flavor_detail,
            ))

    def test_list(self):
        arglist = [
        ]

        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.instances.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.instances.assert_called()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(tuple(self.object_data), tuple(data))


class TestShowDatabaseInstance(rds_fakes.TestRds):

    column_list_headers = [
        'datastore', 'flavor', 'id', 'name', 'region'
        'status', 'volume']

    def setUp(self):
        super(TestShowDatabaseInstance, self).setUp()

        self.cmd = instance.ShowDatabaseInstance(self.app, None)

        self.app.client_manager.rds.find_instance = mock.Mock()

        self.object = self.instance_mock.create_one()

        self.object_data = (
            self.object.datastore,
            self.object.flavor,
            self.object.id,
            self.object.name,
            self.object.region,
            self.object.status,
            self.object.volume,
        )

    def test_show(self):
        arglist = [
            'test_obj',
        ]

        verifylist = [
            ('instance', 'test_obj'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.find_instance.side_effect = [
            self.object
        ]

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
        self.app.client_manager.rds.delete_instance.side_effect = [
            True
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.delete_instance.assert_called()


class TestResizeDatabaseInstanceFlavor(rds_fakes.TestRds):

    def setUp(self):
        super(TestResizeDatabaseInstanceFlavor, self).setUp()

        self.cmd = instance.ResizeDatabaseInstanceFlavor(self.app, None)

        self.app.client_manager.rds.find_instance = mock.Mock()
        self.app.client_manager.rds.find_flavor = mock.Mock()

        self.instance = self.instance_mock.create_one()
        self.flavor = self.flavor_mock.create_one()
        self.instance.resize = mock.Mock()

        self.instance._update(project_id='123')

    def test_delete(self):
        arglist = [
            'curr_inst',
            'new_flavor',
        ]

        verifylist = [
            ('instance', 'curr_inst'),
            ('flavor_id', 'new_flavor')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.find_instance.side_effect = [
            self.instance
        ]
        self.app.client_manager.rds.find_flavor.side_effect = [
            self.flavor
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.find_instance.assert_called()
        self.app.client_manager.rds.find_flavor.assert_called()
        self.instance.resize.assert_called()


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
            '--users',
            'a:b',
            '--size',
            '15',
            'inst_name',
            'flavor',
        ]

        verifylist = [
            ('users', ['a:b']),
            ('size', 15),
            ('name', 'inst_name'),
            ('flavor', 'flavor'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.create_instance.side_effect = [
            self.instance
        ]
        self.app.client_manager.rds.find_flavor.side_effect = [
            self.flavor
        ]

        # Trigger the action
        res = self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.find_flavor.assert_called()
        self.app.client_manager.rds.create_instance.assert_called()


class TestResetDatabaseInstanceStatus(rds_fakes.TestRds):

    def setUp(self):
        super(TestResetDatabaseInstanceStatus, self).setUp()

        self.cmd = instance.ResetDatabaseInstanceStatus(self.app, None)

    def test_delete(self):
        arglist = [
            'curr_inst',
        ]

        verifylist = [
            ('instance', 'curr_inst'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            NotImplementedError, self.cmd.take_action, parsed_args)


class TestUpgradeDatabaseInstance(rds_fakes.TestRds):

    def setUp(self):
        super(TestUpgradeDatabaseInstance, self).setUp()

        self.cmd = instance.UpgradeDatabaseInstance(self.app, None)

    def test_delete(self):
        arglist = [
            'curr_inst',
            'dv'
        ]

        verifylist = [
            ('instance', 'curr_inst'),
            ('datastore_version', 'dv'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            NotImplementedError, self.cmd.take_action, parsed_args)


class TestEnableDatabaseInstanceLog(rds_fakes.TestRds):

    def setUp(self):
        super(TestEnableDatabaseInstanceLog, self).setUp()

        self.cmd = instance.EnableDatabaseInstanceLog(self.app, None)

    def test_delete(self):
        arglist = [
            'curr_inst',
            'dv'
        ]

        verifylist = [
            ('instance', 'curr_inst'),
            ('log_name', 'dv'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            NotImplementedError, self.cmd.take_action, parsed_args)


class TestResizeDatabaseInstanceVolume(rds_fakes.TestRds):

    def setUp(self):
        super(TestResizeDatabaseInstanceVolume, self).setUp()

        self.cmd = instance.ResizeDatabaseInstanceVolume(self.app, None)

    def test_delete(self):
        arglist = [
            'curr_inst',
            '15'
        ]

        verifylist = [
            ('instance', 'curr_inst'),
            ('size', 15),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            NotImplementedError, self.cmd.take_action, parsed_args)


class TestForceDeleteDatabaseInstance(rds_fakes.TestRds):

    def setUp(self):
        super(TestForceDeleteDatabaseInstance, self).setUp()

        self.cmd = instance.ForceDeleteDatabaseInstance(self.app, None)

    def test_delete(self):
        arglist = [
            'curr_inst',
        ]

        verifylist = [
            ('instance', 'curr_inst'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            NotImplementedError, self.cmd.take_action, parsed_args)


class TestRestartDatabaseInstance(rds_fakes.TestRds):

    def setUp(self):
        super(TestRestartDatabaseInstance, self).setUp()

        self.cmd = instance.RestartDatabaseInstance(self.app, None)

    def test_delete(self):
        arglist = [
            'curr_inst',
        ]

        verifylist = [
            ('instance', 'curr_inst'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            NotImplementedError, self.cmd.take_action, parsed_args)


class TestUpdateDatabaseInstance(rds_fakes.TestRds):

    def setUp(self):
        super(TestUpdateDatabaseInstance, self).setUp()

        self.cmd = instance.UpdateDatabaseInstance(self.app, None)

    def test_delete(self):
        arglist = [
            'curr_inst',
        ]

        verifylist = [
            ('instance', 'curr_inst'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            NotImplementedError, self.cmd.take_action, parsed_args)
