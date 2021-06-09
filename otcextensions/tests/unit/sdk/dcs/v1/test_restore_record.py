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

from otcextensions.sdk.dcs.v1 import restore_record

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
FAKE_INSTANCE_ID = "some_fake_id"
EXAMPLE = {
    "status": "succeed",
    "progress": "100.00",
    "restore_id": "a6155972-800c-4170-a479-3231e907d2f6",
    "backup_id": "f4823e9e-fe9b-4ffd-be79-4e5d6de272bb",
    "restore_remark": "doctest",
    "backup_remark": None,
    "created_at": "2017-07-18T21:41:20.721Z",
    "updated_at": "2017-07-18T21:41:35.182Z",
    "restore_name": "restore_20170718214120",
    "backup_name": "backup_20170718000002",
    "error_code": None
}


class TestRestoreRecord(base.TestCase):

    def test_basic(self):
        sot = restore_record.RestoreRecord()

        self.assertEqual('/instances/%(instance_id)s/restores', sot.base_path)

        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = restore_record.RestoreRecord(
            instance_id=FAKE_INSTANCE_ID,
            **EXAMPLE)
        self.assertEqual(FAKE_INSTANCE_ID, sot.instance_id)
        self.assertEqual(EXAMPLE['restore_id'], sot.id)
        self.assertEqual(EXAMPLE['backup_id'], sot.backup_id)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['progress'], sot.progress)
        self.assertEqual(EXAMPLE['restore_remark'], sot.restore_description)
        self.assertEqual(EXAMPLE['backup_remark'], sot.backup_description)
        self.assertEqual(EXAMPLE['restore_name'], sot.restore_name)
        self.assertEqual(EXAMPLE['backup_name'], sot.backup_name)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
        self.assertEqual(EXAMPLE['error_code'], sot.error_code)
