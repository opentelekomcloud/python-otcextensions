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

from otcextensions.sdk.cbr.v3 import restore as _restore


EXAMPLE = {
    'mappings': [{
        'backup_id': 'backup',
        'volume_id': 'volume',
    }],
    'power_on': True,
    'server_id': uuid.uuid4(),
    'volume_id': uuid.uuid4(),
    'resource_id': uuid.uuid4(),
}


class TestRestore(base.TestCase):

    def setUp(self):
        super(TestRestore, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _restore.Restore()
        self.sot_expected = _restore.Restore(**EXAMPLE)

    def test_basic(self):
        sot = _restore.Restore()
        self.assertEqual('restore', sot.resource_key)
        self.assertEqual('', sot.resources_key)
        self.assertEqual('/backups/%(backup_id)s/restore',
                         sot.base_path)
        self.assertFalse(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)
        self.assertDictEqual({
            'limit': 'limit',
            'marker': 'marker',
        }, sot._query_mapping._mapping)

    def test_make_it(self):
        sot = _restore.Restore(**EXAMPLE)
        self.assertTrue(sot.power_on)
        self.assertEqual(
            EXAMPLE['server_id'],
            sot.server_id)
        self.assertEqual(
            EXAMPLE['volume_id'],
            sot.volume_id)
        self.assertEqual(
            EXAMPLE['resource_id'],
            sot.resource_id)
