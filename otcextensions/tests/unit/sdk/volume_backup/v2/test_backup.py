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
import json
import os

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.volume_backup.v2 import backup as _backup

TESTDATA_DIR = os.path.join(os.path.dirname(__file__))


class TestBackup(base.TestCase):

    def setUp(self):
        super(TestBackup, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.list = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.delete = mock.Mock()

        get_fixture = os.path.join(
            TESTDATA_DIR,
            'data_files/get_backup.json')
        list_fixture = os.path.join(
            TESTDATA_DIR,
            'data_files/list_backups.json')
        with open(get_fixture, 'r') as get_data, \
                open(list_fixture, 'r') as list_data:
            self.get_backup_data = json.load(get_data)
            self.list_backup_data = json.load(list_data)

        obj = self.get_backup_data['backup']
        self.sot = _backup.Backup.existing(**obj)

    def test_basic(self):
        sot = _backup.Backup()
        self.assertEqual('backup', sot.resource_key)
        self.assertEqual('backups', sot.resources_key)
        self.assertEqual('/backups',
                         sot.base_path)
        self.assertEqual('vbs', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_update)

    def test_make_it(self):
        obj = self.get_backup_data['backup']
        sot = self.sot
        self.assertEqual(obj['id'], sot.id)
        self.assertEqual(obj['volume_id'], sot.volume_id)
        self.assertEqual(obj['status'], sot.status)
        self.assertEqual(obj['description'], sot.description)
        self.assertEqual(obj['availability_zone'], sot.availability_zone)
        self.assertEqual(obj['size'], sot.size)
        self.assertEqual(obj['container'], sot.container)
        self.assertEqual(obj['created_at'], sot.created_at)

    def mocked_requests_list(*args, **kwargs):

        class MockResponse(object):
            def __init__(self, json_data, status_code):
                self.json_data = copy.deepcopy(json_data)
                self.status_code = status_code

            def json(self):
                return self.json_data

        if args[1] == '/backups':
            list_fixture = os.path.join(
                TESTDATA_DIR,
                'data_files/list_backups.json')
            with open(list_fixture, 'r') as data:
                response = json.load(data)
            return MockResponse(response, 200)

        return MockResponse({'backups': []}, 200)

    def test_list(self):
        """Test list together with pagination
        """

        self.sess.get.side_effect = self.mocked_requests_list

        result = list(self.sot.list(
            self.sess,
            paginated=True,
            name='test_name',
            status='test_status',
            # offset=4,
            # limit=1,
            volume_id='vol_id'))

        calls = [
            mock.call(
                '/backups',
                params={
                    'name': 'test_name',
                    'status': 'test_status',
                    'volume_id': 'vol_id'}),
            mock.call(
                self.list_backup_data['backups_links'][0]['href'],
                params={
                    'name': 'test_name',
                    'status': 'test_status',
                    'volume_id': 'vol_id'
                }),
        ]

        self.sess.get.assert_has_calls(calls)

        self.assertEqual(len(self.list_backup_data), len(result))


    # def test_get(self):
    #     sot = _job.Job.existing(id=EXAMPLE['job_id'])
    #
    #     mock_response = mock.Mock()
    #     mock_response.status_code = 200
    #     mock_response.headers = {}
    #     mock_response.json.return_value = copy.deepcopy(EXAMPLE)
    #
    #     self.sess.get.return_value = mock_response
    #
    #     result = sot.get(self.sess)
    #
    #     self.sess.get.assert_called_once_with(
    #         'jobs/%s' % EXAMPLE['job_id'],
    #     )
    #
    #     self.assertDictEqual(
    #         _job.Job.existing(**EXAMPLE).to_dict(),
    #         result.to_dict())
