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
import copy
import json
import os

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.volume_backup.v2 import backup_task as _backup_task

TESTDATA_DIR = os.path.join(os.path.dirname(__file__))


def _get_fixture(name):
    fixture = os.path.join(
        TESTDATA_DIR,
        'data_files/',
        name)
    with open(fixture, 'r') as data:
        return json.load(data)


EXAMPLE = {
    "status": "EXECUTE_SUCCESS",
    "job_id": "c11b5a18-4559-4731-b7b3-58e2bd89cdb9",
    "created_at": "2016-12-02T09:06:46.706",
    "finished_at": "2016-12-02T13:00:00.121",
    "backup_name": "autobk_e6d2",
    "resource_id": "f47a4ab5-11f5-4509-97f5-80ce0dd74e37",
    "resource_type": "volume"
}


class TestBackupPolicyTask(base.TestCase):

    def setUp(self):
        super(TestBackupPolicyTask, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()

        self.sot = _backup_task.BackupTask()

    def test_basic(self):
        sot = self.sot
        self.assertEqual('tasks', sot.resources_key)
        self.assertEqual(
            '/backuppolicy/%(policy_id)s/backuptasks', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_update)

    def test_make_it(self):
        data = EXAMPLE
        sot = _backup_task.BackupTask.existing(**data)
        self.assertEqual(data['job_id'], sot.id)
        self.assertEqual(data['backup_name'], sot.backup_name)
        self.assertEqual(data['status'], sot.status)
        self.assertEqual(data['resource_id'], sot.resource_id)
        self.assertEqual(data['resource_type'], sot.resource_type)
        if data['created_at']:
            self.assertEqual(data['created_at'], sot.created_at)
        self.assertEqual(data['finished_at'], sot.finished_at)

    def test_list(self):
        response = _get_fixture('list_tasks.json')
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(response)

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess, policy_id='pol_id'))

        self.sess.get.assert_called_once_with(
            '/backuppolicy/%s/backuptasks' % 'pol_id',
            params={}
        )

        self.assertIsNotNone(result)

        for bp in result:
            assert isinstance(bp, _backup_task.BackupTask)
