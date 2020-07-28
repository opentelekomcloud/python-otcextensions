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
import random

from otcextensions.osclient.dcs.v1 import config
from otcextensions.tests.unit.osclient.dcs.v1 import fakes


class TestListParam(fakes.TestDCS):

    objects = fakes.FakeConfig.create_multiple(3)
    inst = fakes.FakeInstance.create_one()

    columns = ('id', 'name', 'value', 'default_value')

    data = []

    for s in objects:
        data.append((
            s.id,
            s.name,
            s.value,
            s.default_value
        ))

    def setUp(self):
        super(TestListParam, self).setUp()

        self.cmd = config.ListInstanceParam(self.app, None)

        self.client.instance_params = mock.Mock()
        self.client.find_instance = mock.Mock()

    def test_list(self):
        arglist = [
            'inst'
        ]

        verifylist = [
            ('instance', 'inst')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.instance_params.side_effect = [
            self.objects
        ]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.instance_params.assert_called_once_with(
            instance={'id': self.inst.id},
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowParam(fakes.TestDCS):

    objects = fakes.FakeConfig.create_multiple(3)
    inst = fakes.FakeInstance.create_one()

    columns = (
        'default_value', 'description', 'id', 'name',
        'value', 'value_range', 'value_type')

    search = objects[random.randint(0, 2)]

    data = (
        search.default_value,
        search.description,
        search.id,
        search.name,
        search.value,
        search.value_range,
        search.value_type,
    )

    def setUp(self):
        super(TestShowParam, self).setUp()

        self.cmd = config.ShowInstanceParam(self.app, None)

        self.client.instance_params = mock.Mock()
        self.client.find_instance = mock.Mock()

    def test_list(self):
        criteria = self.search.name

        arglist = [
            'inst',
            '--param', criteria
        ]

        verifylist = [
            ('instance', 'inst'),
            ('param', criteria)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.instance_params.side_effect = [
            self.objects
        ]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.instance_params.assert_called_once_with(
            instance={'id': self.inst.id},
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdateParam(fakes.TestDCS):

    inst = fakes.FakeInstance.create_one()

    def setUp(self):
        super(TestUpdateParam, self).setUp()

        self.cmd = config.UpdateInstanceParam(self.app, None)

        self.client.update_instance_params = mock.Mock()
        self.client.find_instance = mock.Mock()

    def test_update(self):

        arglist = [
            'inst',
            '--param', 'id1:name1:value1',
            '--param', 'id2:name2:value2',
        ]

        verifylist = [
            ('instance', 'inst'),
            ('param', ['id1:name1:value1', 'id2:name2:value2'])
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_instance_params.side_effect = [{}]
        self.client.find_instance.side_effect = [
            self.inst
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.update_instance_params.assert_called_once_with(
            instance={'id': self.inst.id},
            params=[
                {
                    'param_id': 'id1',
                    'param_name': 'name1',
                    'param_value': 'value1'
                }, {
                    'param_id': 'id2',
                    'param_name': 'name2',
                    'param_value': 'value2'
                }
            ]
        )
