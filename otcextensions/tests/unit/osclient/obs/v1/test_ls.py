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
from osc_lib import utils as common_utils

from otcextensions.osclient.obs.v1 import ls
from otcextensions.tests.unit.osclient.obs.v1 import fakes as s3_fakes


class TestS3(s3_fakes.TestObs):

    def setUp(self):
        super(TestS3, self).setUp()


class TestS3Ls(TestS3):

    columns_buckets = ('Creation Date', 'Name')
    columns_objects = ('Modify Date', 'Name', 'Size')
    columns_objects_long = ('Modify Date', 'Name', 'Size',
                            'ETag', 'Storage Class')

    def setUp(self):
        super(TestS3Ls, self).setUp()

        self.cmd = ls.List(self.app, None)

        self.app.client_manager.obs.list_objects = mock.Mock()
        self.app.client_manager.obs.list_buckets = mock.Mock()

        self.buckets = self.bucket_mock.create_buckets(3)
        self.buckets_data = []
        self.buckets_data_long = []

        self.objects = self.object_mock.create_objects(3)
        self.objects_data = []
        self.objects_data_hr = []
        self.objects_data_long = []

        for s in self.buckets:
            self.buckets_data.append((
                s.creationdate,
                s.name,
            ))

        for s in self.objects:
            self.objects_data.append((
                s.lastmodified,
                s.key,
                s.size,
            ))
            self.objects_data_hr.append((
                s.lastmodified,
                s.key,
                common_utils.format_size(s.size),
            ))
            self.objects_data_long.append((
                s.lastmodified,
                s.key,
                s.size,
                s.etag,
                s.storageclass
            ))
        # print(self.objects)

    # @mock.patch("otcextensions.obsclient.client.Client.list_buckets")
    def test_s3_ls_no_options(self):
        arglist = [
        ]
        verifylist = [
            ('human_readable', False),
            ('long', False)
            # ('disk_format', image.DEFAULT_DISK_FORMAT),
            # ('name', self.new_image.name),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.obs.buckets.side_effect = [
            self.buckets
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.obs.objects.assert_not_called()
        self.app.client_manager.obs.buckets.assert_called()

        self.assertEqual(self.columns_buckets, columns)
        self.assertEqual(tuple(self.buckets_data), tuple(data))

    def test_s3_ls_objects(self):
        bucket_url = 's3://test-bucket'
        arglist = [
            bucket_url
        ]

        verifylist = [
            ('human_readable', False),
            ('long', False),
            ('url', bucket_url)
            # ('disk_format', image.DEFAULT_DISK_FORMAT),
            # ('name', self.new_image.name),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.obs.objects.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.obs.objects.assert_called()
        self.app.client_manager.obs.buckets.assert_not_called()

        self.assertEqual(self.columns_objects, columns)
        self.assertEqual(tuple(self.objects_data), tuple(data))

    def test_s3_ls_objects_long(self):
        bucket_url = 's3://test-bucket'
        arglist = [
            bucket_url,
            '--long'
        ]

        verifylist = [
            ('human_readable', False),
            ('long', True),
            ('url', bucket_url)
            # ('disk_format', image.DEFAULT_DISK_FORMAT),
            # ('name', self.new_image.name),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.obs.objects = mock.Mock()
        self.app.client_manager.obs.objects.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.obs.objects.assert_called()
        self.app.client_manager.obs.buckets.assert_not_called()

        self.assertEqual(self.columns_objects_long, columns)
        self.assertEqual(tuple(self.objects_data_long), tuple(data))

    def test_s3_ls_objects_human_readable(self):
        bucket_url = 's3://test-bucket'
        arglist = [
            bucket_url,
            '--human-readable'
        ]

        verifylist = [
            ('human_readable', True),
            ('long', False),
            ('url', bucket_url)
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.obs.objects.side_effect = [
            self.objects
        ]
        self.app.client_manager.obs.get_bucket_by_name.side_effect = [
            self.buckets[0]
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.obs.objects.assert_called()
        self.app.client_manager.obs.buckets.assert_not_called()

        self.app.client_manager.obs.objects.assert_called_with(
            self.buckets[0]
        )

        self.assertEqual(self.columns_objects, columns)
        self.assertEqual(tuple(self.objects_data_hr), tuple(data))

    def test_s3_ls_some_params(self):
        bucket_url = 's3://test-bucket'
        arglist = [
            bucket_url,
            '--human-readable',
            '--marker=mrk',
            '--limit=3',
            '--prefix=prf'
        ]

        verifylist = [
            ('human_readable', True),
            ('long', False),
            ('url', bucket_url),
            ('limit', 3),
            ('marker', 'mrk'),
            ('prefix', 'prf')
        ]

        bucket = self.buckets[0]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        # Set the response
        self.app.client_manager.obs.get_bucket_by_name.side_effect = [
            bucket
        ]
        self.app.client_manager.obs.objects.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.obs.objects.assert_called_with(
            bucket,
            Marker='mrk',
            MaxKeys=3,
            Prefix='prf'
        )
