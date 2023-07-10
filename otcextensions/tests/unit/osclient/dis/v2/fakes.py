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
