# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
import mock

from otcextensions.osclient.dcaas.v2 import virtual_gateway
from otcextensions.tests.unit.osclient.dcaas.v2 import fakes

from osc_lib import exceptions

from openstackclient.tests.unit import utils as tests_utils


class TestListVirtualGateway(fakes.TestDcaas):

    objects = fakes.FakeVirtualGateway.create_multiple(3)

    column_list_headers = (
        'id',
        'name',
        'vpc id',
        'local ep group id',
        'type',
        'status'
    )
    columns = (
        'id',
        'name',
        'vpc id',
        'local ep group id',
        'type',
        'status'
    )
    data = []
    for s in objects:
        data.append((
            s.id,
            s.name,
            s.vpc_id,
            s.local_ep_group_id,
            s.type,
            s.status
        ))

    def setUp(self):
        super(TestListVirtualGateway, self).setUp()
        self.cmd = virtual_gateway.ListVirtualGateways(self.app, None)
        self.client.virtual_gateways = mock.Mock()
        self.client.api_mock = self.client.virtual_gateways

    def test_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.client.api_mock.side_effect = [self.objects]
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()
        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            '--id', '1',
            '--name', 'test',
            '--vpc_id', 'vpc_id1',
            '--local_ep_group_id', 'lepg_id1',
            '--type', 'double ipsec',
            '--status', 'ACTIVE'
        ]
        verifylist = [
            ('id', '1'),
            ('name', 'test'),
            ('vpc_id', 'vpc_id1'),
            ('local_ep_group_id', 'lepg_id1'),
            ('type', 'double ipsec'),
            ('status', 'ACTIVE')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.client.api_mock.side_effect = [self.objects]
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            id='1',
            name='test',
            vpc_id='vpc_id1',
            local_ep_group_id='lepg_id1',
            type='double ipsec',
            status='ACTIVE'
        )


class TestCreateVirtualGateway(fakes.TestDcaas):
    _data = fakes.FakeVirtualGateway.create_one()

    columns = (
        'admin_state_up',
        'bgp_asn',
        'description',
        'device_id',
        'id',
        'ipsec_bandwidth',
        'local_ep_group_id',
        'name',
        'redundant_device_id',
        'status',
        'type',
        'vpc_id'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateVirtualGateway, self).setUp()
        self.cmd = virtual_gateway.CreateVirtualGateway(self.app, None)
        self.client.create_virtual_gateway = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            'vpc_id1',
            'lepg_id1',
            '--name', 'test',
            '--description', 'test description',
            '--device_id', 'device_id1',
            '--redundant_device_id', 'red_dev_id1',
            '--type', 'default',
            '--ipsec_bandwidth', '50',
            '--bgp_asn', '10',
            '--admin_state_up', 'True'
        ]
        verifylist = [
            ('vpc_id', 'vpc_id1'),
            ('local_ep_group_id', 'lepg_id1'),
            ('name', 'test'),
            ('description', 'test description'),
            ('device_id', 'device_id1'),
            ('redundant_device_id', 'red_dev_id1'),
            ('type', 'default'),
            ('ipsec_bandwidth', 50),
            ('bgp_asn', 10),
            ('admin_state_up', True)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.client.create_virtual_gateway.assert_called_with(
            name='test',
            vpc_id='vpc_id1',
            local_ep_group_id='lepg_id1',
            description='test description',
            device_id='device_id1',
            redundant_device_id='red_dev_id1',
            type='default',
            ipsec_bandwidth=50,
            bgp_asn=10,
            admin_state_up=True
        )
        self.assertEqual(self.columns, columns)


class TestShowVirtualGateway(fakes.TestDcaas):

    _data = fakes.FakeVirtualGateway.create_one()

    columns = (
        'admin_state_up',
        'bgp_asn',
        'description',
        'device_id',
        'id',
        'ipsec_bandwidth',
        'local_ep_group_id',
        'name',
        'redundant_device_id',
        'status',
        'type',
        'vpc_id'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowVirtualGateway, self).setUp()
        self.cmd = virtual_gateway.ShowVirtualGateway(self.app, None)
        self.client.find_virtual_gateway = mock.Mock(return_value=self._data)

    def test_show_no_option(self):
        arglist = []
        verifylist = []
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.id,
        ]
        verifylist = [
            ('virtual_gateway', self._data.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)
        self.client.find_virtual_gateway.assert_called_with(self._data.id)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existing(self):
        arglist = [
            'unexisting_virtual_gateway'
        ]
        verifylist = [
            ('virtual_gateway', 'unexisting_virtual_gateway')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        find_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_virtual_gateway = (
            mock.Mock(side_effect=find_mock_result)
        )
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.find_virtual_gateway.assert_called_with(
            'unexisting_virtual_gateway'
        )


class TestUpdateVirtualGateway(fakes.TestDcaas):

    _data = fakes.FakeVirtualGateway.create_one()

    columns = (
        'admin_state_up',
        'bgp_asn',
        'description',
        'device_id',
        'id',
        'ipsec_bandwidth',
        'local_ep_group_id',
        'name',
        'redundant_device_id',
        'status',
        'type',
        'vpc_id'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestUpdateVirtualGateway, self).setUp()
        self.cmd = virtual_gateway.UpdateVirtualGateway(self.app, None)
        self.client.find_virtual_gateway = mock.Mock(return_value=self._data)
        self.client.update_virtual_gateway = mock.Mock(return_value=self._data)
        self.client.api_mock = self.client.update_virtual_gateway

    def test_update(self):
        arglist = [
            self._data.id,
            '--name', 'updated_name',
            '--description', 'updated description',
            '--local_ep_group_id', 'lepg_id2'
        ]
        verifylist = [
            ('virtual_gateway', self._data.id),
            ('name', 'updated_name'),
            ('description', 'updated description'),
            ('local_ep_group_id', 'lepg_id2')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.side_effect = [
            self._data
        ]

        self.client.api_mock.assert_called_with(
            self._data.id,
            name='updated_name',
            description='updated description',
            local_ep_group_id='lepg_id2'
        )
        self.assertEqual(self.columns, columns)


class TestDeleteVirtualGateway(fakes.TestDcaas):
    _data = fakes.FakeVirtualGateway.create_one()

    def setUp(self):
        super(TestDeleteVirtualGateway, self).setUp()
        self.client.delete_virtual_gateway = mock.Mock(return_value=None)
        self.cmd = virtual_gateway.DeleteVirtualGateway(self.app, None)

    def test_delete(self):
        arglist = [
            self._data.name,
        ]
        verifylist = [
            ('virtual_gateway', self._data.name)
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.client.find_virtual_gateway = (
            mock.Mock(return_value=self._data)
        )
        result = self.cmd.take_action(parsed_args)
        self.client.delete_virtual_gateway.assert_called_with(self._data.id)
        self.assertIsNone(result)
