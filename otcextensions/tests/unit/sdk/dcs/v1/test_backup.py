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

from otcextensions.sdk.dcs.v1 import backup

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
FAKE_INSTANCE_ID = "some_fake_id"
EXAMPLE = {
    "backup_id": FAKE_ID,
    "status": "succeed",
    "remark": "remark",
    "period": "22:00-23:00",
    "progress": "100.00",
    "size": 126,
    "created_at": "2018-04-15T22:00:00.780Z",
    "updated_at": "2018-04-15T22:01:10.823Z",
    "backup_type": "auto",
    "backup_name": "backup_20180415230000",
    "error_code": None,
    "is_support_restore": "TRUE"
}


class TestBackup(base.TestCase):

    def test_basic(self):
        sot = backup.Backup()

        self.assertEqual('/instances/%(instance_id)s/backups', sot.base_path)

        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):

        sot = backup.Backup(instance_id=FAKE_INSTANCE_ID, **EXAMPLE)
        self.assertEqual(FAKE_INSTANCE_ID, sot.instance_id)
        self.assertEqual(EXAMPLE['backup_id'], sot.id)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['remark'], sot.description)
        self.assertEqual(EXAMPLE['period'], sot.period)
        self.assertEqual(EXAMPLE['progress'], sot.progress)
        self.assertEqual(EXAMPLE['size'], sot.size)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
        self.assertEqual(EXAMPLE['backup_type'], sot.type)
        self.assertEqual(EXAMPLE['backup_name'], sot.name)
        self.assertEqual(EXAMPLE['error_code'], sot.error_code)
        self.assertEqual(True, sot.is_restorable)
