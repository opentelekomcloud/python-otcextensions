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
from otcextensions.osclient.anti_ddos.v1 import floating_ip
from otcextensions.tests.unit.osclient.anti_ddos.v1 import fakes


class TestListFloatingIP(fakes.TestAntiDDoS):

    objects = fakes.FakeFloatingIP.create_multiple(3)

    columns = (
        'floating_ip_address', 'floating_ip_id', 'network_type', 'status'
    )

    data = []

    for s in objects:
        data.append((
            s.floating_ip_address,
            s.floating_ip_id,
            s.network_type,
            s.status
        ))

    def setUp(self):
        super(TestListFloatingIP, self).setUp()

        self.cmd = floating_ip.ListFloatingIP(self.app, None)

        self.client.floating_ips = mock.Mock()
        self.client.api_mock = self.client.floating_ips

    def test_list(self):
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

    def test_list_query(self):
        arglist = [
            '--ip', 'ip_pref',
            '--status', 'normal'
        ]

        verifylist = [
            ('ip', 'ip_pref'),
            ('status', 'normal')
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
            ip='ip_pref',
            status='normal'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShow(fakes.TestAntiDDoS):

    _data = fakes.FakeFloatingIP.create_one()

    columns = (
        'app_type_id', 'cleaning_access_pos_id', 'floating_ip_address',
        'floating_ip_id', 'http_request_pos_id', 'id', 'is_enable_l7',
        'network_type', 'status')

    data = (
        _data.app_type_id,
        _data.cleaning_access_pos_id,
        _data.floating_ip_address,
        _data.floating_ip_id,
        _data.http_request_pos_id,
        _data.id,
        _data.is_enable_l7,
        _data.network_type,
        _data.status
    )

    def setUp(self):
        super(TestShow, self).setUp()

        self.cmd = floating_ip.ShowFloatingIP(self.app, None)

        self.client.get_floating_ip_policies = mock.Mock()
        self.client.api_mock = self.client.get_floating_ip_policies

    def test_show_default(self):
        arglist = [
            'name_or_id',
        ]
        verifylist = [
            ('floating_ip_id', 'name_or_id'),
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
            'name_or_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestSetFloatingIP(fakes.TestAntiDDoS):

    _data = fakes.FakeFloatingIP.create_one()

    columns = (
        'app_type_id', 'cleaning_access_pos_id', 'floating_ip_address',
        'floating_ip_id', 'http_request_pos_id', 'id', 'is_enable_l7',
        'network_type', 'status')

    data = (
        _data.app_type_id,
        _data.cleaning_access_pos_id,
        _data.floating_ip_address,
        _data.floating_ip_id,
        _data.http_request_pos_id,
        _data.id,
        _data.is_enable_l7,
        _data.network_type,
        _data.status
    )

    def setUp(self):
        super(TestSetFloatingIP, self).setUp()

        self.cmd = floating_ip.SetFloatingIP(self.app, None)

        self.client.update_floating_ip_policies = mock.Mock()
        self.client.api_mock = self.client.update_floating_ip_policies

    def test_default(self):
        arglist = [
            'ip_id',
            '--enable_l7',
            '--traffic_pos_id', '1',
            '--http_request_pos_id', '2',
            '--cleaning_access_pos_id', '3',
            '--app_type_id', '0',
        ]
        verifylist = [
            ('floating_ip_id', 'ip_id'),
            ('enable_l7', True),
            ('traffic_pos_id', 1),
            ('http_request_pos_id', 2),
            ('cleaning_access_pos_id', 3),
            ('app_type_id', 0),
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
            floating_ip='ip_id',
            traffic_pos_id=1,
            http_request_pos_id=2,
            cleaning_access_pos_id=3,
            is_enable_l7=True,
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_enable_false(self):
        arglist = [
            'ip_id',
            '--disable_l7',
            '--traffic_pos_id', '1',
            '--http_request_pos_id', '2',
            '--cleaning_access_pos_id', '3',
            '--app_type_id', '0',
        ]
        verifylist = [
            ('floating_ip_id', 'ip_id'),
            ('disable_l7', True),
            ('traffic_pos_id', 1),
            ('http_request_pos_id', 2),
            ('cleaning_access_pos_id', 3),
            ('app_type_id', 0),
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
            floating_ip='ip_id',
            traffic_pos_id=1,
            http_request_pos_id=2,
            cleaning_access_pos_id=3,
            is_enable_l7=False,
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
