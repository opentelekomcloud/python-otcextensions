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
import mock

from keystoneauth1 import adapter
from openstack.tests.unit import base

from otcextensions.sdk.cbr.v3 import member

EXAMPLE = {
    'status': 'accepted',
    'backup_id': 'backup_id',
    'image_id': 'image_id',
    'vault_id': 'vault_id',
    'dest_project_id': 'dest_project_id',
    'updated_at': '2020-02-24T09:36:00.479031',
    'created_at': '2020-02-24T09:36:00.479033',
    'id': 'member_id'
}

ADD_MEMBER = {
    'status': 'pending',
    'backup_id': 'backup_id',
    'members' : ['member_1', 'member_2']
}


class TestMember(base.TestCase):

    def setUp(self):
        super(TestMember, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.default_microversion = None
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.retriable_status_codes = ()
        self.sot = member.Member()

    def test_basic(self):
        sot = member.Member()
        self.assertEqual('member', sot.resource_key)
        self.assertEqual('members', sot.resources_key)
        self.assertEqual('/backups/%(backup_id)s/members', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = member.Member.existing(**EXAMPLE)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['backup_id'], sot.backup_id)
        self.assertEqual(EXAMPLE['image_id'], sot.image_id)
        self.assertEqual(EXAMPLE['vault_id'], sot.vault_id)
        self.assertEqual(EXAMPLE['dest_project_id'], sot.dest_project_id)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)

'''TO BE DONE
    def test_add_members(self):
        sot = member.Member.existing(**ADD_MEMBER)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = member.Member.existing(id=EXAMPLE['id'])

        members = ['member1', 'member2']

        sot.add_members(self.sess, members)

        self.sess.post.assert_called_once_with(
            'backups/%s/members' % EXAMPLE['id'],
            json={'members': members}
        )
'''