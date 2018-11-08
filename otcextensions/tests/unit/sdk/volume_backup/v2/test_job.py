# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import copy

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.volume_backup.v2 import job as _job


EXAMPLE = {
    'status': 'SUCCESS',
    'entities': {
        'bks_create_volume_name': 'autobk_volume',
        'backup_id': 'ba5401a2-7cd2-4c01-8c0d-c936ab412d6d',
        'volume_id': '7e5fdc5a-5e36-4b22-8bcc-7f17037290cc',
        'snapshot_id': 'a77a96bf-dd18-40bf-a446-fdcefc1719ec'
    },
    'job_id': '4010b39b5281d3590152874bfa3b1604',
    'job_type': 'bksCreateBackup',
    'begin_time': '2016-01-28T16:14:09.466Z',
    'end_time': '2016-01-28T16:25:27.690Z',
    'error_code': None,
    'fail_reason': None
}


class TestJob(base.TestCase):

    def setUp(self):
        super(TestJob, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()

    def test_basic(self):
        sot = _job.Job()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)
        self.assertEqual('/jobs',
                         sot.base_path)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        obj = EXAMPLE
        sot = _job.Job.existing(**obj)
        self.assertEqual(obj['job_id'], sot.id)
        self.assertEqual(obj['job_type'], sot.type)

    def test_get(self):
        sot = _job.Job.existing(id=EXAMPLE['job_id'])

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = copy.deepcopy(EXAMPLE)

        self.sess.get.return_value = mock_response

        result = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            'jobs/%s' % EXAMPLE['job_id'],
        )

        self.assertDictEqual(
            _job.Job.existing(**EXAMPLE).to_dict(),
            result.to_dict())
