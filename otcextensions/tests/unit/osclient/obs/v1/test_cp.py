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

from otcextensions.osclient.obs.v1 import cp
from otcextensions.tests.unit.osclient.obs.v1 import fakes as s3_fakes


class TestS3(s3_fakes.TestObs):

    def setUp(self):
        super(TestS3, self).setUp()


class TestS3Cp(TestS3):

    columns_buckets = ('Creation Date', 'Name')
    columns_objects = ('Modify Date', 'Name', 'Size')
    columns_objects_long = ('Modify Date', 'Name', 'Size',
                            'ETag', 'Storage Class')

    def setUp(self):
        super(TestS3Cp, self).setUp()

        self.cmd = cp.Copy(self.app, None)

        self.app.client_manager.obs.list_objects = mock.Mock()
        self.app.client_manager.obs.list_buckets = mock.Mock()
        self.app.client_manager.obs.download_file = mock.Mock()
        self.app.client_manager.obs.create_object = mock.Mock()

    def test_s3_cp_upload(self):
        arglist = [
            'tox.ini',
            's3://remote_dest'
        ]
        verifylist = [
            ('srcurl', ['tox.ini']),
            ('dsturl', ['s3://remote_dest']),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        # self.app.client_manager.obs.list_objects.assert_not_called()
        self.app.client_manager.obs.create_object.assert_called()
        # self.app.client_manager.obs.upload_file.assert_not_called()

    def test_s3_cp_upload_src_missing(self):
        arglist = [
            '___doesnotexist',
            's3://remote_dest'
        ]
        verifylist = [
            ('srcurl', ['___doesnotexist']),
            ('dsturl', ['s3://remote_dest']),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaises(
            exceptions.CommandError,
            self.cmd.take_action,
            parsed_args,
        )
