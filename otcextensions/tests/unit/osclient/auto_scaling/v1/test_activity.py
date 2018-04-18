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

from otcextensions.osclient.auto_scaling.v1 import activity
from otcextensions.tests.unit.osclient.auto_scaling.v1 import fakes


class TestAutoScalingActivity(fakes.TestAutoScaling):

    def setUp(self):
        super(TestAutoScalingActivity, self).setUp()
        self.client = self.app.client_manager.auto_scaling


class TestListAutoScalingActivity(TestAutoScalingActivity):

    _activities = fakes.FakeActivity.create_multiple(3)
    _group = fakes.FakeGroup.create_one()

    columns = (
        'ID', 'status', 'description',
        'instance_value', 'desire_value',
        'start_time', 'end_time')

    data = []

    for s in _activities:
        data.append((
            s.id,
            s.status,
            s.description,
            s.instance_value,
            s.desire_value,
            s.start_time,
            s.end_time
        ))

    def setUp(self):
        super(TestListAutoScalingActivity, self).setUp()

        self.cmd = activity.ListAutoScalingActivityLogs(self.app, None)

        self.client.find_group = mock.Mock()
        self.client.activities = mock.Mock()

    def test_list_default(self):
        arglist = [
            '--start_time', '2200-01-01T00:00:00Z',
            '--end_time', '2200-01-02T00:00:00Z',
            '--limit', '14',
            'group1'
        ]

        verifylist = [
            ('start_time', '2200-01-01T00:00:00Z'),
            ('end_time', '2200-01-02T00:00:00Z'),
            ('limit', 14),
            ('group', 'group1')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_group.side_effect = [
            self._group
        ]
        self.client.activities.side_effect = [
            self._activities
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_group.assert_called_once_with(
            'group1', ignore_missing=False)
        self.client.activities.assert_called_once_with(
            end_time='2200-01-02T00:00:00Z',
            start_time='2200-01-01T00:00:00Z',
            group=self._group.id,
            limit=14,
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
