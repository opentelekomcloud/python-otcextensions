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
# import uuid
# from datetime import datetime
import mock

from osc_lib import utils as _osc_lib_utils

from openstackclient.tests.unit import utils

from otcextensions.tests.unit.osclient import test_base
from otcextensions.sdk.dis.v2 import stream
from otcextensions.sdk.dis.v2 import app
from otcextensions.sdk.dis.v2 import checkpoint
from otcextensions.sdk.dis.v2 import dump_task


def gen_data(obj, columns, formatters=None):
    """Fill expected data tuple based on columns list
    """
    return _osc_lib_utils.get_item_properties(
        obj, columns, formatters=formatters
    )


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestDis(utils.TestCommand):
    def setUp(self):
        super(TestDis, self).setUp()

        self.app.client_manager.dis = mock.Mock()

        self.client = self.app.client_manager.dis


class FakeStream(test_base.Fake):
    """Fake one or more Dis Streams."""
    @classmethod
    def generate(cls):
        """Create a fake DIS Stream.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "auto_scale_enabled": True,
            "auto_scale_max_partition_count": 1,
            "auto_scale_min_partition_count": 1,
            "compression_format": "gzip",
            "create_time": 1687671774706,
            "data_type": "BLOB",
            "has_more_partitions": False,
            "last_modified_time": 1687671775413,
            "partitions": [
                {
                    "hash_range": "[0 : 461168601842738]",
                    "partition_id": "shardId-0000000000",
                    "sequence_number_range": "[0 : 0]",
                    "status": "ACTIVE"
                },
                {
                    "hash_range": "[461168601842738 : 922337203685477]",
                    "partition_id": "shardId-0000000001",
                    "sequence_number_range": "[0 : 0]",
                    "status": "ACTIVE"
                }
            ],
            "readable_partition_count": 2,
            "retention_period": 24,
            "status": "RUNNING",
            "stream_id": "VeamOHP5TNBWpprzcTi",
            "stream_name": "test-dis3",
            "stream_type": "COMMON",
            "writable_partition_count": 2
        }

        return stream.Stream(**object_info)


class FakeApp(test_base.Fake):
    """Fake one or more Dis Apps."""
    @classmethod
    def generate(cls):
        """Create a fake DIS App.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "app_id": "bd6IPpvgiIflQPMpi9M",
            "app_name": "newstream",
            "create_time": 1593569685875,
            "commit_checkpoint_stream_names": ["newstream"]
        }

        return app.App(**object_info)


class FakeCheckpoint(test_base.Fake):
    """Fake one or more Dis Checkpoints."""
    @classmethod
    def generate(cls):
        """Create a fake DIS Checkpoint.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "sequence_number": "newstram",
            "metadata": ""
        }
        return checkpoint.Checkpoint(**object_info)


class FakeDumpTask(test_base.Fake):
    """Fake one or more Dis Apps."""
    @classmethod
    def generate(cls):
        """Create a fake DIS App.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "create_time": 1689377676849,
            "destination_type": "OBS",
            "exception_strategy": "ignoreAndBackup",
            "last_transfer_timestamp": 1689377695587,
            "obs_destination_description": {
                "agency_name": "dis_admin_agency",
                "consumer_strategy": "LATEST",
                "deliver_time_interval": 300,
                "destination_file_type": "text",
                "obs_bucket_path": "test-bucket-abcdef",
                "record_delimiter": "\n",
                "retry_duration": 0
            },
            "partitions": [
                {
                    "discard": 0,
                    "last_transfer_offset": 0,
                    "last_transfer_timestamp": 1689377695587,
                    "partitionId": "shardId-0000000000",
                    "state": "RUNNING"
                },
                {
                    "discard": 0,
                    "last_transfer_offset": 0,
                    "last_transfer_timestamp": 1689377695587,
                    "partitionId": "shardId-0000000001",
                    "state": "RUNNING"
                }
            ],
            "state": "RUNNING",
            "streamId": "bxdSOIEYPwJdSlAqq5z",
            "stream_id": "bxdSOIEYPwJdSlAqq5z",
            "stream_name": "test-dis",
            "task_id": "lJ4Ts5ObPd2UOpcRj3K",
            "task_name": "test-dump-task"
        }

        return dump_task.DumpTask(**object_info)
