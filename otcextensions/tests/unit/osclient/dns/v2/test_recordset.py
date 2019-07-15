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
import mock

from otcextensions.osclient.dns.v2 import recordset
from otcextensions.tests.unit.osclient.dns.v2 import fakes


class TestListRS(fakes.TestDNS):

    objects = fakes.FakeRecordset.create_multiple(3)
    _zone = fakes.FakeZone.create_one()

    columns = (
        'id', 'name', 'type', 'status', 'description', 'records'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListRS, self).setUp()

        self.cmd = recordset.ListRS(self.app, None)

        self.client.recordsets = mock.Mock()
        self.client.find_zone = mock.Mock()
        self.client.api_mock = self.client.recordsets

    def test_default_zone(self):
        arglist = [
            'zn'
        ]

        verifylist = [
            ('zone', 'zn')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]
        self.client.find_zone.side_effect = [
            self._zone
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_zone.assert_called_once_with(
            'zn',
            ignore_missing=False,
        )
        self.client.api_mock.assert_called_once_with(
            zone=self._zone
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowRS(fakes.TestDNS):

    _data = fakes.FakeRecordset.create_one()
    _zone = fakes.FakeZone.create_one()

    columns = (
        'description', 'name', 'records', 'status', 'ttl', 'type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowRS, self).setUp()

        self.cmd = recordset.ShowRS(self.app, None)

        self.client.find_zone = mock.Mock()
        self.client.get_recordset = mock.Mock()
        self.client.api_mock = self.client.get_recordset

    def test_default(self):
        arglist = [
            'zone',
            'rs'
        ]

        verifylist = [
            ('zone', 'zone'),
            ('recordset', 'rs')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_zone.side_effect = [
            self._zone
        ]
        self.client.api_mock.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            zone=self._zone,
            recordset='rs'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateRS(fakes.TestDNS):

    _data = fakes.FakeRecordset.create_one()
    _zone = fakes.FakeZone.create_one()

    columns = (
        'description', 'name', 'records', 'status', 'ttl', 'type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateRS, self).setUp()

        self.cmd = recordset.CreateRS(self.app, None)

        self.client.create_recordset = mock.Mock()
        self.client.find_zone = mock.Mock()
        self.client.api_mock = self.client.create_recordset

    def test_create(self):
        arglist = [
            'zn',
            '--name', 'rs',
            '--description', 'descr',
            '--type', 'A',
            '--ttl', '500',
            '--record', 'a=b',
            '--record', 'c=d',
        ]

        verifylist = [
            ('zone', 'zn'),
            ('name', 'rs'),
            ('description', 'descr'),
            ('type', 'A'),
            ('ttl', 500),
            ('record', ['a=b', 'c=d']),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_zone.side_effect = [
            self._zone
        ]
        self.client.api_mock.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            zone=self._zone,
            description='descr',
            name='rs',
            type='A',
            ttl=500,
            records=['a=b', 'c=d']
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestSetRS(fakes.TestDNS):

    _data = fakes.FakeRecordset.create_one()
    _zone = fakes.FakeZone.create_one()

    columns = (
        'description', 'name', 'records', 'status', 'ttl', 'type'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestSetRS, self).setUp()

        self.cmd = recordset.SetRS(self.app, None)

        self.client.update_recordset = mock.Mock()
        self.client.find_zone = mock.Mock()
        self.client.get_recordset = mock.Mock()
        self.client.api_mock = self.client.update_recordset

    def test_create(self):
        arglist = [
            'zn',
            'rs',
            '--description', 'descr',
            '--ttl', '500',
            '--record', 'a=b',
            '--record', 'c=d',
        ]

        verifylist = [
            ('zone', 'zn'),
            ('recordset', 'rs'),
            ('description', 'descr'),
            ('ttl', 500),
            ('record', ['a=b', 'c=d']),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_zone.side_effect = [
            self._zone
        ]
        self.client.api_mock.side_effect = [
            self._data
        ]
        self.client.get_recordset.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            recordset=self._data,
            description='descr',
            records=['a=b', 'c=d'],
            ttl=500,
            zone_id=self._zone.id
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteRS(fakes.TestDNS):
    _zone = fakes.FakeZone.create_one()

    def setUp(self):
        super(TestDeleteRS, self).setUp()

        self.cmd = recordset.DeleteRS(self.app, None)

        self.client.delete_recordset = mock.Mock()
        self.client.find_zone = mock.Mock()
        self.client.api_mock = self.client.delete_recordset

    def test_delete_multiple(self):
        arglist = [
            'zn',
            't1',
            't2',
        ]
        verifylist = [
            ('zone', 'zn'),
            ('recordset', ['t1', 't2'])
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_zone.side_effect = [
            self._zone
        ]
        self.client.api_mock.side_effect = [{}, {}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        calls = [
            mock.call(zone=self._zone, recordset='t1', ignore_missing=False),
            mock.call(zone=self._zone, recordset='t2', ignore_missing=False)
        ]

        self.client.api_mock.assert_has_calls(calls)
        self.assertEqual(2, self.client.api_mock.call_count)
