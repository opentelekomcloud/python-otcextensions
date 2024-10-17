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

from otcextensions.sdk.dds.v3 import recycle_instance

EXAMPLE = {
    "total_count": 1,
    "instances": [
        {
            "id": "07fc12a8e0e94df7a3fcf53d0b5e1605in02",
            "name": "test1",
            "mode": "ReplicaSet",
            "datastore": {
                "type": "DDS-Community",
                "version": "4.0"
            },
            "pay_mode": "0",
            "enterprise_project_id": "0",
            "backup_id": "bf9ee62a7f7044c583c6765c916c36edbr02",
            "created_at": "2022-01-01T10:00:00",
            "deleted_at": "2022-02-01T10:00:00",
            "retained_until": "2022-05-01T10:00:00",
            "status": "Active"
        }
    ]
}


class TestRecycleInstance(base.TestCase):
    def test_basic(self):
        sot = recycle_instance.RecycleInstance()
        path = '/recycle-instances'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = recycle_instance.RecycleInstance(**EXAMPLE)
        self.assertEqual(EXAMPLE['total_count'], sot.total_count)
