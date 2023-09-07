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
from otcextensions.sdk.dis.v2 import stream


EXAMPLE = {
    "stream_id": "8QM3Nt9YTLOwtUVYJhO",
    "stream_name": "newstream",
    "create_time": 1593569685875,
    "last_modified_time": 1599050091026,
    "retention_period": 24,
    "status": "RUNNING",
    "stream_type": "COMMON",
    "data_type": "BLOB",
    "writable_partition_count": 1,
    "readable_partition_count": 1,
    "tags": [],
    "auto_scale_enabled": False,
    "auto_scale_min_partition_count": 0,
    "auto_scale_max_partition_count": 0,
    "partitions": [
        {
            "status": "ACTIVE",
            "partition_id": "shardId-0000000000",
            "hash_range": "[0 : 9223372036854775807]",
            "sequence_number_range": "[289911 : 289927]"
        }
    ],
    "has_more_partitions": False
}


class TestStream(base.TestCase):

    def test_basic(self):
        sot = stream.Stream()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('stream_info_list', sot.resources_key)
        path = '/streams'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = stream.Stream(**EXAMPLE)
        updated_sot_attrs = (
            'auto_scale_enabled',
            'create_time',
            'last_modified_time',
            'stream_name',
        )
        self.assertEqual(EXAMPLE['create_time'], sot.created_at)
        self.assertEqual(EXAMPLE['stream_id'], sot.id)
        self.assertEqual(EXAMPLE['stream_name'], sot.name)
        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
