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

from otcextensions.sdk.cbr.v3 import checkpoint as _checkpoint


EXAMPLE = {
    'status': 'protecting',
    'created_at': '2021-02-09T12:03:42.554535',
    'project_id': uuid.uuid4(),
    'id': uuid.uuid4(),
    'vault': {
        'skipped_resources': [],
        'id': uuid.uuid4(),
        'resources': [
            {
                'name': uuid.uuid4(),
                'backup_size': '0',
                'resource_size': '6',
                'protect_status': 'available',
                'backup_count': '0',
                'type': 'OS::Nova::Server',
                'id': uuid.uuid4(),
                'extra_info': {}
            }
        ],
        'name': uuid.uuid4(),
    },
    'extra_info': {
        'retention_duration': -1,
        'name': uuid.uuid4(),
        'description': uuid.uuid4(),
    }
}


class TestCheckpoint(base.TestCase):

    def setUp(self):
        super(TestCheckpoint, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _checkpoint.Checkpoint()
        self.sot_expected = _checkpoint.Checkpoint(**EXAMPLE)

    def test_basic(self):
        sot = _checkpoint.Checkpoint()
        self.assertEqual('checkpoint', sot.resource_key)
        self.assertEqual('', sot.resources_key)
        self.assertEqual('/checkpoints',
                         sot.base_path)
        self.assertFalse(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        test_checkpoint = _checkpoint.Checkpoint(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['status'],
            test_checkpoint.status)
        self.assertEqual(
            EXAMPLE['created_at'],
            test_checkpoint.created_at)
        self.assertEqual(
            EXAMPLE['project_id'],
            test_checkpoint.project_id)
        self.assertEqual(
            EXAMPLE['id'],
            test_checkpoint.id)
        self.assertEqual(
            EXAMPLE['vault']['skipped_resources'],
            test_checkpoint.vault.skipped_resources)
        self.assertEqual(
            EXAMPLE['vault']['id'],
            test_checkpoint.vault.id)
        self.assertEqual(
            EXAMPLE['vault']['resources'][0]['name'],
            test_checkpoint.vault.resources[0].name)
        self.assertEqual(
            EXAMPLE['vault']['resources'][0]['backup_size'],
            test_checkpoint.vault.resources[0].backup_size)
        self.assertEqual(
            EXAMPLE['vault']['resources'][0]['resource_size'],
            test_checkpoint.vault.resources[0].resource_size)
        self.assertEqual(
            EXAMPLE['vault']['resources'][0]['protect_status'],
            test_checkpoint.vault.resources[0].protect_status)
        self.assertEqual(
            EXAMPLE['vault']['resources'][0]['backup_count'],
            test_checkpoint.vault.resources[0].backup_count)
        self.assertEqual(
            EXAMPLE['vault']['resources'][0]['type'],
            test_checkpoint.vault.resources[0].type)
        self.assertEqual(
            EXAMPLE['vault']['resources'][0]['id'],
            test_checkpoint.vault.resources[0].id)
        self.assertEqual(
            EXAMPLE['vault']['resources'][0]['extra_info'],
            test_checkpoint.vault.resources[0].extra_info)
        self.assertEqual(
            EXAMPLE['vault']['name'],
            test_checkpoint.vault.name)
        self.assertEqual(
            EXAMPLE['extra_info']['retention_duration'],
            test_checkpoint.extra_info.retention_duration)
        self.assertEqual(
            EXAMPLE['extra_info']['name'],
            test_checkpoint.extra_info.name)
