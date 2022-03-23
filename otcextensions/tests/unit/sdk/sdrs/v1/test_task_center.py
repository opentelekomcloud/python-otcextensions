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

import uuid
from keystoneauth1 import adapter
import mock
from openstack.tests.unit import base

from otcextensions.sdk.sdrs.v1 import task_center as _task_center


EXAMPLE = {
    "job_status": "FAIL",
    "resource_id": uuid.uuid4(),
    "resource_name": "Replication-Pair-4fb5",
    "resource_type": "replications",
    "failure_status": "expandFail",
    "job_id": uuid.uuid4(),
    "job_type": "expandReplicationPairNew",
    "begin_time": "2022-03-18T13:55:33.570Z",
    "error_code": "SDRS.1820",
    "fail_reason": "Failed to expand the capacity"
}


class TestTaskCenter(base.TestCase):

    def setUp(self):
        super(TestTaskCenter, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _task_center.FailedTask()

    def test_basic(self):
        sot = _task_center.FailedTask()
        self.assertEqual('', sot.resource_key)
        self.assertEqual('failure_jobs', sot.resources_key)
        self.assertEqual('/task-center/failure-jobs',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertDictEqual({
            'failure_status': 'failure_status',
            'limit': 'limit',
            'marker': 'marker',
            'offset': 'offset',
            'resource_name': 'resource_name',
            'resource_type': 'resource_type',
            'server_group_id': 'server_group_id'
        }, sot._query_mapping._mapping)

    def test_make_it(self):
        test_failed_task = _task_center.FailedTask(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['job_status'],
            test_failed_task.job_status)
        self.assertEqual(
            EXAMPLE['resource_id'],
            test_failed_task.resource_id)
        self.assertEqual(
            EXAMPLE['resource_name'],
            test_failed_task.resource_name)
        self.assertEqual(
            EXAMPLE['resource_type'],
            test_failed_task.resource_type)
        self.assertEqual(
            EXAMPLE['failure_status'],
            test_failed_task.failure_status)
        self.assertEqual(
            EXAMPLE['job_id'],
            test_failed_task.job_id)
        self.assertEqual(
            EXAMPLE['job_type'],
            test_failed_task.job_type)
        self.assertEqual(
            EXAMPLE['begin_time'],
            test_failed_task.begin_time)
        self.assertEqual(
            EXAMPLE['error_code'],
            test_failed_task.error_code)
        self.assertEqual(
            EXAMPLE['fail_reason'],
            test_failed_task.fail_reason)
