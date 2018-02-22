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

from keystoneauth1 import adapter
import mock

from openstack.tests.unit import base

from otcextensions.sdk.rds.v1 import backup


PROJECT_ID = '23'
IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'id': IDENTIFIER,
    'name': '50deafb3e45d451a9406ca146b71fe9a_rds',
    'description': '',
    'locationRef': '',
    'created': '2016-08-23T03:59:23',
    'updated': '2016-08-23T04:01:40',
    'size': 0.0,
    'status': 'COMPLETED',
    'backuptype': '1',
    'dataStore': {
        'type': 'MySQL',
        'version': '5.6.30',
        'version_id': 'e8a8b8cc-63f8-4fb5-8d4a-24c502317a61'
    },
    'instance_id': '4f87d3c4-9e33-482f-b962-e23b30d1a18c',
    'parent_id': None
}

EXAMPLE_POLICY = {
    'keepday': 7,
    'starttime': '00:00:00'
}


class TestBackup(base.TestCase):

    def setUp(self):
        super(TestBackup, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)
        self.sot = backup.Backup(**EXAMPLE)
        # print(self.sot.to_dict())

    def test_basic(self):
        sot = backup.Backup()
        self.assertEqual('backup', sot.resource_key)
        self.assertEqual('backups', sot.resources_key)
        self.assertEqual('/%(project_id)s/backups', sot.base_path)
        self.assertEqual('rds', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = backup.Backup(**EXAMPLE)
        self.assertEqual(IDENTIFIER, sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['created'], sot.created)

    def test_list(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'backups': [EXAMPLE]}

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess, project_id=PROJECT_ID))

        self.sess.get.assert_called_once_with(
            '/%s/backups' % (PROJECT_ID),
            headers={"Content-Type": "application/json"},
            params={})

        self.assertEqual([backup.Backup(**EXAMPLE)], result)

    def test_create(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'backup': copy.deepcopy(EXAMPLE)}
        mock_response.headers = {}

        self.sess.post.return_value = mock_response

        sot = backup.Backup.new(
            project_id=PROJECT_ID,
            name='backup_name',
            description='descr',
            instance='some_instance')

        result = sot.create(self.sess)

        self.sess.post.assert_called_once_with(
            '/%s/backups' % (PROJECT_ID),
            headers={},
            json={'backup': {
                'instance': 'some_instance',
                'description': 'descr',
                'name': 'backup_name'}
            }
        )

        self.assertEqual(
            backup.Backup(
                **EXAMPLE,
                project_id=PROJECT_ID,
                instance='some_instance'),
            result)

    def test_delete(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {}

        self.sess.delete.return_value = mock_response

        sot = backup.Backup(
            **EXAMPLE,
            project_id=PROJECT_ID
        )

        sot.delete(self.sess)

        url = '%(project_id)s/backups/%(id)s' % \
            {
                'project_id': PROJECT_ID,
                'id': sot.id
            }

        # utils.urljoin strips leading '/', but it is not a problem
        self.sess.delete.assert_called_once_with(
            url,
            headers={
                'Content-Type': 'application/json',
                'Accept': ''
            }
        )

    def test_policy_update(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'policy':
            copy.deepcopy(EXAMPLE_POLICY)}
        mock_response.headers = {}
        instance_id = 'instance_id'

        self.sess.put.return_value = mock_response

        sot = backup.BackupPolicy(
            **EXAMPLE_POLICY,
            project_id=PROJECT_ID,
            instance_id=instance_id)

        self.assertIsNone(sot.update(self.sess))

        url = '/%(project_id)s/instances/%(instance_id)s/backups/policy' % \
            {
                'project_id': PROJECT_ID,
                'instance_id': instance_id
            }

        self.sess.put.assert_called_once_with(
            url,
            headers={
                'Content-Type': 'application/json',
                'X-Language': 'en-us'},
            json={'policy': EXAMPLE_POLICY}
        )
