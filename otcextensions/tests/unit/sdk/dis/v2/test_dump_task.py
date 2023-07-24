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

from openstack.tests.unit import base
from otcextensions.sdk.dis.v2 import dump_task

EXAMPLE = {
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


class TestDumpTask(base.TestCase):

    def test_basic(self):
        sot = dump_task.DumpTask()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('tasks', sot.resources_key)
        path = '/streams/%(uri_stream_name)s/transfer-tasks'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_patch)

    def test_make_it(self):
        sot = dump_task.DumpTask(**EXAMPLE)
        updated_sot_attrs = (
            'create_time',
            'state',
            'streamId',
            'obs_destination_description',
        )
        self.assertEqual(EXAMPLE['create_time'], sot.created_at)
        self.assertEqual(EXAMPLE['state'], sot.status)
        self.assertEqual(EXAMPLE['streamId'], sot.stream_id)
        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

        obs_dest = EXAMPLE['obs_destination_description']
        sot_obs_dest = dump_task.ObsDestinationSpec(**obs_dest)
        for key, value in obs_dest.items():
            self.assertEqual(getattr(sot_obs_dest, key), value)
