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

from otcextensions.osclient.dns.v2 import ptr
from otcextensions.tests.unit.osclient.dns.v2 import fakes


class TestListPTR(fakes.TestDNS):

    objects = fakes.FakePTR.create_multiple(3)

    columns = (
        'id', 'name', 'type', 'status', 'description'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListPTR, self).setUp()

        self.cmd = ptr.ListPTR(self.app, None)

        self.client.ptrs = mock.Mock()
        self.client.api_mock = self.client.ptrs

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


class TestShowPTR(fakes.TestDNS):

    _data = fakes.FakePTR.create_one()

    columns = (
        'address', 'description', 'floating_ip_id', 'id',
        'ptrdname', 'region', 'ttl'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowPTR, self).setUp()

        self.cmd = ptr.ShowPTR(self.app, None)

        self.client.get_ptr = mock.Mock()
        self.client.api_mock = self.client.get_ptr

    def test_default(self):
        arglist = [
            '--ptr', 'ptr_id',
            '--region', 'regio',
            '--floating_ip', 'fpid'
        ]

        verifylist = [
            ('ptr', 'ptr_id'),
            ('region', 'regio'),
            ('floating_ip', 'fpid')
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
            ptr='ptr_id'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_default_no_id(self):
        arglist = [
            '--region', 'regio',
            '--floating_ip', 'fpid'
        ]

        verifylist = [
            ('region', 'regio'),
            ('floating_ip', 'fpid')
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
            floating_ip_id='fpid',
            region='regio'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestSetPTR(fakes.TestDNS):

    _data = fakes.FakePTR.create_one()

    columns = (
        'address', 'description', 'floating_ip_id', 'id',
        'ptrdname', 'region', 'ttl'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestSetPTR, self).setUp()

        self.cmd = ptr.SetPTR(self.app, None)

        self.client.create_ptr = mock.Mock()
        self.client.api_mock = self.client.create_ptr

    def test_default(self):
        arglist = [
            '--region', 'regio',
            '--floating_ip', 'fpid',
            '--ptrdname', 'dname',
            '--description', 'descr',
            '--ttl', '350'
        ]

        verifylist = [
            ('region', 'regio'),
            ('floating_ip', 'fpid'),
            ('ptrdname', 'dname'),
            ('description', 'descr'),
            ('ttl', 350)
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
            floating_ip_id='fpid',
            ptrdname='dname',
            region='regio',
            ttl=350
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeletePTR(fakes.TestDNS):

    columns = (
        'address', 'description', 'floating_ip_id', 'id',
        'ptrdname', 'region', 'ttl'
    )

    def setUp(self):
        super(TestDeletePTR, self).setUp()

        self.cmd = ptr.DeletePTR(self.app, None)

        self.client.restore_ptr = mock.Mock()
        self.client.api_mock = self.client.restore_ptr

    def test_default(self):
        arglist = [
            '--ptr', 'ptr_id',
            '--region', 'regio',
            '--floating_ip', 'fpid'
        ]

        verifylist = [
            ('ptr', 'ptr_id'),
            ('region', 'regio'),
            ('floating_ip', 'fpid')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            ptr='ptr_id'
        )

    def test_default_no_id(self):
        arglist = [
            '--region', 'regio',
            '--floating_ip', 'fpid'
        ]

        verifylist = [
            ('region', 'regio'),
            ('floating_ip', 'fpid')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            floating_ip_id='fpid',
            region='regio'
        )
