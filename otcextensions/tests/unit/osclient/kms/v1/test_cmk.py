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

from osc_lib import exceptions

from otcextensions.osclient.kms.v1 import cmk
from otcextensions.tests.unit.osclient.kms.v1 import fakes


class TestCMK(fakes.TestKMS):

    def setUp(self):
        super(TestCMK, self).setUp()
        self.client = self.app.client_manager.kms


class TestListCMK(TestCMK):

    _objs = fakes.FakeCMK.create_multiple(3)

    columns = ('ID', 'key_alias', 'key_state')

    data = []

    for s in _objs:
        data.append((
            s.id,
            s.key_alias,
            s.key_state
        ))

    def setUp(self):
        super(TestListCMK, self).setUp()

        self.cmd = cmk.ListCMK(self.app, None)

        self.client.keys = mock.Mock()

    def test_list_default(self):
        arglist = [
            '--limit', '14',
            '--state', '2'
        ]

        verifylist = [
            ('limit', 14),
            ('state', 2)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.keys.side_effect = [
            self._objs
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.keys.assert_called_once_with(
            key_state=2,
            limit=14,
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowCMK(TestCMK):

    _obj = fakes.FakeCMK.create_one()

    columns = ['ID', 'key_alias', 'domain_id', 'realm',
               'key_description', 'creation_date', 'scheduled_deletion_date',
               'key_state', 'key_type']

    data = (
        _obj.id,
        _obj.key_alias,
        _obj.domain_id,
        _obj.realm,
        _obj.key_description,
        _obj.creation_date,
        _obj.scheduled_deletion_date,
        _obj.key_state,
        _obj.key_type,
    )

    def setUp(self):
        super(TestShowCMK, self).setUp()

        self.cmd = cmk.ShowCMK(self.app, None)

        self.client.find_key = mock.Mock()

    def test_show(self):
        arglist = [
            'key1'
        ]

        verifylist = [
            ('key', 'key1'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_key.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_key.assert_called_once_with(
            'key1',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestCreateCMK(TestCMK):

    _obj = fakes.FakeCMK.create_one()

    columns = ['ID', 'key_alias', 'domain_id', 'realm',
               'key_description', 'creation_date', 'scheduled_deletion_date',
               'key_state', 'key_type']

    data = (
        _obj.id,
        _obj.key_alias,
        _obj.domain_id,
        _obj.realm,
        _obj.key_description,
        _obj.creation_date,
        _obj.scheduled_deletion_date,
        _obj.key_state,
        _obj.key_type,
    )

    def setUp(self):
        super(TestCreateCMK, self).setUp()

        self.cmd = cmk.CreateCMK(self.app, None)

        self.client.create_key = mock.Mock()

    def test_create(self):
        arglist = [
            'key1',
            '--description', 'dscr',
            '--realm', 'rlm',
            '--key_policy', 'pol',
            '--key_usage', 'usg',
            '--type', 'typ'
        ]

        verifylist = [
            ('alias', 'key1'),
            ('description', 'dscr'),
            ('realm', 'rlm'),
            ('key_policy', 'pol'),
            ('key_usage', 'usg'),
            ('type', 'typ')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_key.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_key.assert_called_once_with(
            key_alias='key1',
            key_description='dscr',
            key_policy='pol',
            key_type='typ',
            key_usage='usg',
            realm='rlm'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestEnableCMK(TestCMK):

    _obj = fakes.FakeCMK.create_one()

    def setUp(self):
        super(TestEnableCMK, self).setUp()

        self.cmd = cmk.EnableCMK(self.app, None)

        self.client.enable_key = mock.Mock()
        self.client.find_key = mock.Mock()

    def test_enable(self):
        arglist = [
            'key1'
        ]

        verifylist = [
            ('key', 'key1'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_key.side_effect = [self._obj]
        self.client.enable_key.side_effect = [self._obj]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_key.assert_called_once_with('key1')
        self.client.enable_key.assert_called()


class TestDisableCMK(TestCMK):

    _obj = fakes.FakeCMK.create_one()

    def setUp(self):
        super(TestDisableCMK, self).setUp()

        self.cmd = cmk.DisableCMK(self.app, None)

        self.client.disable_key = mock.Mock()
        self.client.find_key = mock.Mock()

    def test_disable(self):
        arglist = [
            'key1'
        ]

        verifylist = [
            ('key', 'key1'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_key.side_effect = [self._obj]
        self.client.disable_key.side_effect = [self._obj]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_key.assert_called_once_with('key1')
        self.client.disable_key.assert_called_once()


class TestDeleteCMK(TestCMK):

    _obj = fakes.FakeCMK.create_one()

    def setUp(self):
        super(TestDeleteCMK, self).setUp()

        self.cmd = cmk.DeleteCMK(self.app, None)

        self.client.schedule_key_deletion = mock.Mock()
        self.client.find_key = mock.Mock()

    def test_delete(self):
        arglist = [
            'key1', '7'
        ]

        verifylist = [
            ('key', 'key1'),
            ('days', 7)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_key.side_effect = [self._obj]
        self.client.schedule_key_deletion.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_key.assert_called_once_with('key1')
        self.client.schedule_key_deletion.assert_called_once_with(
            key=self._obj,
            pending_days=7
        )

    def test_delete_out_of_range(self):
        arglist = [
            'key1', '3'
        ]

        verifylist = [
            ('key', 'key1'),
            ('days', 3)
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            exceptions.CommandError, self.cmd.take_action, parsed_args)


class TestCancelDeleteCMK(TestCMK):

    _obj = fakes.FakeCMK.create_one()

    def setUp(self):
        super(TestCancelDeleteCMK, self).setUp()

        self.cmd = cmk.CancelDeleteCMK(self.app, None)

        self.client.cancel_key_deletion = mock.Mock()
        self.client.find_key = mock.Mock()

    def test_delete(self):
        arglist = [
            'key1'
        ]

        verifylist = [
            ('key', 'key1'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_key.side_effect = [self._obj]
        self.client.cancel_key_deletion.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        self.client.find_key.assert_called_once_with('key1')
        self.client.cancel_key_deletion.assert_called_once_with(
            key=self._obj,
        )
