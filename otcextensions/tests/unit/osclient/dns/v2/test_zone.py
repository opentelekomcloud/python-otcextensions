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
import argparse
import mock

from otcextensions.osclient.dns.v2 import zone
from otcextensions.tests.unit.osclient.dns.v2 import fakes


class TestListZone(fakes.TestDNS):

    objects = fakes.FakeZone.create_multiple(3)

    columns = (
        'id', 'name', 'zone_type', 'serial', 'status', 'action'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListZone, self).setUp()

        self.cmd = zone.ListZone(self.app, None)

        self.client.zones = mock.Mock()
        self.client.api_mock = self.client.zones

    def test_default(self):
        arglist = [
        ]

        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_default_query(self):
        arglist = [
            '--type', 'private'
        ]

        verifylist = [
            ('type', 'private')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            type='private'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowZone(fakes.TestDNS):

    _data = fakes.FakeZone.create_one()

    columns = (
        'action', 'created_at', 'description', 'email', 'id', 'name',
        'pool_id', 'record_num', 'router', 'serial', 'status', 'ttl',
        'updated_at', 'zone_type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowZone, self).setUp()

        self.cmd = zone.ShowZone(self.app, None)

        self.client.find_zone = mock.Mock()
        self.client.api_mock = self.client.find_zone

    def test_default(self):
        arglist = [
            'zone'
        ]

        verifylist = [
            ('zone', 'zone')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            'zone'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateZone(fakes.TestDNS):

    _data = fakes.FakeZone.create_one()

    columns = (
        'action', 'created_at', 'description', 'email', 'id', 'name',
        'pool_id', 'record_num', 'router', 'serial', 'status', 'ttl',
        'updated_at', 'zone_type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateZone, self).setUp()

        self.cmd = zone.CreateZone(self.app, None)

        self.client.create_zone = mock.Mock()
        self.client.api_mock = self.client.create_zone

    def test_create(self):
        arglist = [
            '--name', 'zn',
            '--email', 'eml',
            '--description', 'descr',
            '--type', 'public',
            '--ttl', '500',
            '--router_id', 'rid',
            '--router_region', 'regio',
        ]

        verifylist = [
            ('name', 'zn'),
            ('email', 'eml'),
            ('description', 'descr'),
            ('type', 'public'),
            ('ttl', 500),
            ('router_id', 'rid'),
            ('router_region', 'regio'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            description='descr',
            email='eml',
            name='zn',
            ttl=500,
            zone_type='public'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_create_private(self):
        arglist = [
            '--name', 'zn',
            '--email', 'eml',
            '--description', 'descr',
            '--type', 'private',
            '--ttl', '500',
            '--router_id', 'rid',
            '--router_region', 'regio',
        ]

        verifylist = [
            ('name', 'zn'),
            ('email', 'eml'),
            ('description', 'descr'),
            ('type', 'private'),
            ('ttl', 500),
            ('router_id', 'rid'),
            ('router_region', 'regio'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            description='descr',
            email='eml',
            name='zn',
            ttl=500,
            zone_type='private',
            router={'router_id': 'rid', 'router_region': 'regio'}
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_create_private_raise_no_rid(self):
        arglist = [
            '--name', 'zn',
            '--email', 'eml',
            '--description', 'descr',
            '--type', 'private',
            '--ttl', '500',
            '--router_region', 'regio',
        ]

        verifylist = [
            ('name', 'zn'),
            ('email', 'eml'),
            ('description', 'descr'),
            ('type', 'private'),
            ('ttl', 500),
            ('router_region', 'regio'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]

        # Trigger the action
        self.assertRaises(argparse.ArgumentTypeError,
                          self.cmd.take_action, parsed_args)

        self.client.api_mock.assert_not_called()


class TestSetZone(fakes.TestDNS):

    _data = fakes.FakeZone.create_one()

    columns = (
        'action', 'created_at', 'description', 'email', 'id', 'name',
        'pool_id', 'record_num', 'router', 'serial', 'status', 'ttl',
        'updated_at', 'zone_type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestSetZone, self).setUp()

        self.cmd = zone.SetZone(self.app, None)

        self.client.update_zone = mock.Mock()
        self.client.find_zone = mock.Mock()
        self.client.api_mock = self.client.update_zone

    def test_update(self):
        arglist = [
            'zn',
            '--email', 'eml',
            '--description', 'descr',
            '--ttl', '500',
        ]

        verifylist = [
            ('zone', 'zn'),
            ('email', 'eml'),
            ('description', 'descr'),
            ('ttl', 500),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]
        self.client.find_zone.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_zone.assert_called_once_with(
            'zn',
            ignore_missing=False
        )

        self.client.api_mock.assert_called_once_with(
            zone=self._data,
            description='descr',
            email='eml',
            ttl=500
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteZone(fakes.TestDNS):

    def setUp(self):
        super(TestDeleteZone, self).setUp()

        self.cmd = zone.DeleteZone(self.app, None)

        self.client.delete_zone = mock.Mock()
        self.client.api_mock = self.client.delete_zone

    def test_delete_multiple(self):
        arglist = [
            't1',
            't2',
        ]
        verifylist = [
            ('zone', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [
            mock.call(zone='t1', ignore_missing=False),
            mock.call(zone='t2', ignore_missing=False)
        ]

        self.client.api_mock.assert_has_calls(calls)
        self.assertEqual(2, self.client.api_mock.call_count)


class TestAssociateRouter(fakes.TestDNS):

    _data = fakes.FakeZone.create_one()

    columns = (
        'action', 'created_at', 'description', 'email', 'id', 'name',
        'pool_id', 'record_num', 'router', 'serial', 'status', 'ttl',
        'updated_at', 'zone_type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestAssociateRouter, self).setUp()

        self.cmd = zone.AssociateRouterToZone(self.app, None)

        self.client.add_router_to_zone = mock.Mock()
        self.client.find_zone = mock.Mock()
        self.client.api_mock = self.client.add_router_to_zone

    def test_update(self):
        arglist = [
            'zn',
            '--router_id', 'rid',
            '--router_region', 'regio',
        ]

        verifylist = [
            ('zone', 'zn'),
            ('router_id', 'rid'),
            ('router_region', 'regio'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]
        self.client.find_zone.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_zone.assert_called_once_with(
            'zn',
            ignore_missing=False
        )

        self.client.api_mock.assert_called_once_with(
            zone=self._data,
            router_id='rid',
            router_region='regio'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDisassociateRouter(fakes.TestDNS):

    _data = fakes.FakeZone.create_one()

    columns = (
        'action', 'created_at', 'description', 'email', 'id', 'name',
        'pool_id', 'record_num', 'router', 'serial', 'status', 'ttl',
        'updated_at', 'zone_type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestDisassociateRouter, self).setUp()

        self.cmd = zone.DisassociateRouterToZone(self.app, None)

        self.client.remove_router_from_zone = mock.Mock()
        self.client.find_zone = mock.Mock()
        self.client.api_mock = self.client.remove_router_from_zone

    def test_update(self):
        arglist = [
            'zn',
            '--router_id', 'rid',
            '--router_region', 'regio',
        ]

        verifylist = [
            ('zone', 'zn'),
            ('router_id', 'rid'),
            ('router_region', 'regio'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]
        self.client.find_zone.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_zone.assert_called_once_with(
            'zn',
            ignore_missing=False
        )

        self.client.api_mock.assert_called_once_with(
            zone=self._data,
            router_id='rid',
            router_region='regio'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
