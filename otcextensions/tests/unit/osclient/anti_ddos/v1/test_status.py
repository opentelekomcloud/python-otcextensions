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

# from otcextensions.common import sdk_utils
from otcextensions.osclient.anti_ddos.v1 import status
from otcextensions.tests.unit.osclient.anti_ddos.v1 import fakes


class TestListFloatingIPEvents(fakes.TestAntiDDoS):

    objects = fakes.FakeFloatingIPEvent.create_multiple(3)

    columns = (
        'start_time', 'end_time', 'status', 'trigger_bps',
        'trigger_pps', 'trigger_http_pps'
    )

    data = []

    for s in objects:
        data.append((
            s.start_time,
            s.end_time,
            s.status,
            s.trigger_bps,
            s.trigger_pps,
            s.trigger_http_pps
        ))

    def setUp(self):
        super(TestListFloatingIPEvents, self).setUp()

        self.cmd = status.ListFloatingIPEvents(self.app, None)

        self.client.floating_ip_events = mock.Mock()
        self.client.api_mock = self.client.floating_ip_events

    def test_list(self):
        arglist = [
            'ip_id'
        ]

        verifylist = [
            ('floating_ip', 'ip_id')
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
            floating_ip_id='ip_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestListFloatingIPDayStat(fakes.TestAntiDDoS):

    objects = fakes.FakeFloatingIPStatDay.create_multiple(3)

    columns = (
        'period_start', 'bps_in', 'bps_attack', 'total_bps',
        'pps_in', 'pps_attack', 'total_pps'
    )

    data = []

    for s in objects:
        data.append((
            s.period_start,
            s.bps_in,
            s.bps_attack,
            s.total_bps,
            s.pps_in,
            s.pps_attack,
            s.total_pps
        ))

    def setUp(self):
        super(TestListFloatingIPDayStat, self).setUp()

        self.cmd = status.ListFloatingIPStatDay(self.app, None)

        self.client.floating_ip_stat_day = mock.Mock()
        self.client.api_mock = self.client.floating_ip_stat_day

    def test_list(self):
        arglist = [
            'ip_id'
        ]

        verifylist = [
            ('floating_ip', 'ip_id')
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
            floating_ip_id='ip_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestFloatingIPWeekStat(fakes.TestAntiDDoS):

    _data = fakes.FakeFloatingIPStatWeek.create_one()

    columns = (
        'period_start_date', 'ddos_intercept_times', 'ddos_blackhole_times',
        'max_attack_bps', 'max_attack_conns')

    data = []
    for wd in _data.weekdata:
        data.append((
            wd.period_start_date,
            wd.ddos_intercept_times,
            wd.ddos_blackhole_times,
            wd.max_attack_bps,
            wd.max_attack_conns
        ))

    def setUp(self):
        super(TestFloatingIPWeekStat, self).setUp()

        self.cmd = status.ListFloatingIPStatWeek(self.app, None)

        self.client.floating_ip_stat_week = mock.Mock()
        self.client.api_mock = self.client.floating_ip_stat_week

    def test_default(self):
        arglist = [
        ]
        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self._data
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
