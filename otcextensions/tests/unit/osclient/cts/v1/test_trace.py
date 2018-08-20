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

from otcextensions.osclient.cts.v1 import trace
from otcextensions.tests.unit.osclient.cts.v1 import fakes


class TestListTrace(fakes.TestCTS):

    objects = fakes.FakeTrace.create_multiple(3)

    columns = (
        'id', 'name', 'user', 'service_type', 'type',
        'resource_type', 'resource_name', 'resource_id',
        'source_ip', 'level', 'time'
    )

    columns_long = (
        'id', 'name', 'type', 'user', 'service_type',
        'resource_type', 'resource_name', 'resource_id',
        'source_ip', 'level', 'time', 'request', 'response'
    )

    data = []
    data_long = []

    for s in objects:
        data.append((
            s.id,
            s.name,
            s.user,
            s.service_type,
            s.type,
            s.resource_type,
            s.resource_name,
            s.resource_id,
            s.source_ip,
            s.level,
            s.time
        ))
        data_long.append((
            s.id,
            s.name,
            s.type,
            s.user,
            s.service_type,
            s.resource_type,
            s.resource_name,
            s.resource_id,
            s.source_ip,
            s.level,
            s.time,
            s.request,
            s.response
        ))

    def setUp(self):
        super(TestListTrace, self).setUp()

        self.cmd = trace.ListTrace(self.app, None)

        self.client.traces = mock.Mock()

    def test_list(self):
        arglist = [
        ]

        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.traces.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.traces.assert_called_once_with(
            tracker='system'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

    def test_list_long(self):
        arglist = [
            '--long'
        ]

        verifylist = [
            ('long', True)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.traces.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.traces.assert_called_once_with(
            tracker='system'
        )

        self.assertEqual(self.columns_long, columns)
        self.assertEqual(self.data_long, list(data))

    def test_list_query(self):
        arglist = [
            '--tracker', 'trck',
            '--limit', '1',
            '--next', '2',
            '--service_type', '3',
            '--resource_type', '4',
            '--resource_id', '5',
            '--resource_name', '6',
            '--trace_name', '7',
            '--trace_id', '8',
            '--level', 'NORMAL',
            '--user', '9',
            '--start_time', '1970-01-01T00:00:00',
            '--end_time', '1970-01-01T00:00:00',
        ]

        verifylist = [
            ('tracker', 'trck'),
            ('limit', 1),
            ('next', 2),
            ('service_type', '3'),
            ('resource_type', '4'),
            ('resource_id', '5'),
            ('resource_name', '6'),
            ('trace_name', '7'),
            ('trace_id', '8'),
            ('level', 'NORMAL'),
            ('user', '9'),
            ('start_time', '1970-01-01T00:00:00'),
            ('end_time', '1970-01-01T00:00:00'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.traces.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.traces.assert_called_once_with(
            level='NORMAL',
            limit=1,
            next=2,
            res_id='5',
            res_name='6',
            res_type='4',
            service_type='3',
            to=0,
            trace_id='8',
            trace_name='7',
            tracker='trck',
            user='9',
            **{
                'from': 0,
            }
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
