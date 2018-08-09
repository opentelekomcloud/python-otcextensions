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

RDS_HEADERS = {
    'content-type': 'application/json',
    'x-language': 'en-us'
}

# PROJECT_ID = '23'
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
    'parent_id': None,
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
        # self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)
        self.sot = backup.Backup(**EXAMPLE)

    def test_basic(self):
        sot = backup.Backup()
        self.assertEqual('backup', sot.resource_key)
        self.assertEqual('backups', sot.resources_key)
        self.assertEqual('/backups', sot.base_path)
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

        result = list(self.sot.list(
            self.sess,
            headers=RDS_HEADERS))

        self.sess.get.assert_called_once_with(
            '/backups',
            headers=RDS_HEADERS,
            params={},
        )

        self.assertEqual([backup.Backup(**EXAMPLE)], result)

    def test_create(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'backup': copy.deepcopy(EXAMPLE)}
        mock_response.headers = {}

        self.sess.post.return_value = mock_response

        sot = backup.Backup.new(
            # project_id=PROJECT_ID,
            name='backup_name',
            description='descr',
            instance='some_instance')

        result = sot.create(self.sess, headers=RDS_HEADERS)

        self.sess.post.assert_called_once_with(
            '/backups',
            headers=RDS_HEADERS,
            json={'backup': {
                'instance': 'some_instance',
                'description': 'descr',
                'name': 'backup_name'}
            }
        )

        self.assertEqual(
            backup.Backup(
                # project_id=PROJECT_ID,
                instance='some_instance',
                **EXAMPLE),
            result)

    def test_delete(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {}

        self.sess.delete.return_value = mock_response

        sot = backup.Backup(
            # project_id=PROJECT_ID,
            **EXAMPLE
        )

        sot.delete(self.sess, headers=RDS_HEADERS)

        url = 'backups/%(id)s' % \
            {
                'id': sot.id
            }

        # utils.urljoin strips leading '/', but it is not a problem
        self.sess.delete.assert_called_once_with(
            url,
            headers=RDS_HEADERS
        )

    def test_policy_basic(self):
        sot = backup.BackupPolicy()
        self.assertEqual('policy', sot.resource_key)
        self.assertEqual(None, sot.resources_key)
        self.assertEqual('/instances/%(instance_id)s/'
                         'backups/policy', sot.base_path)
        self.assertEqual('rds', sot.service.service_type)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_policy_make_it(self):
        sot = backup.BackupPolicy(**EXAMPLE_POLICY)
        self.assertEqual(EXAMPLE_POLICY['keepday'], sot.keepday)
        self.assertEqual(EXAMPLE_POLICY['starttime'], sot.starttime)

    def test_policy_update(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'policy':
            copy.deepcopy(EXAMPLE_POLICY)}
        mock_response.headers = {}
        instance_id = 'instance_id'

        self.sess.put.return_value = mock_response

        sot = backup.BackupPolicy.new(
            # project_id=PROJECT_ID,
            instance_id=instance_id,
            **EXAMPLE_POLICY)

        self.assertIsNone(sot.update(self.sess, headers=RDS_HEADERS))

        url = '/instances/%(instance_id)s/backups/policy' % \
            {
                'instance_id': instance_id
            }

        self.sess.put.assert_called_once_with(
            url,
            headers=RDS_HEADERS,
            json={'policy': EXAMPLE_POLICY}
        )

    def test_policy_get(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'policy':
            copy.deepcopy(EXAMPLE_POLICY)}
        mock_response.headers = {}
        instance_id = 'instance_id'

        self.sess.get.return_value = mock_response

        sot = backup.BackupPolicy.new(
            # **EXAMPLE_POLICY,
            # project_id=PROJECT_ID,
            instance_id=instance_id)

        res = sot.get(self.sess, requires_id=False, headers=RDS_HEADERS)

        url = '/instances/%(instance_id)s/backups/policy' % \
            {
                'instance_id': instance_id
            }

        self.sess.get.assert_called_once_with(
            url,
            headers=RDS_HEADERS
        )

        self.assertEqual(EXAMPLE_POLICY['keepday'], res.keepday)
        self.assertEqual(EXAMPLE_POLICY['starttime'], res.starttime)
