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
from unittest import mock

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.sfsturbo.v1 import share as _share


IDENTIFIER = 'ID'
EXAMPLE = {
    "id": "share-id",
    "action_progress": {},
    "az_name": "az_name",
    "avail_capacity": "avail_capacity",
    "availability_zone": "availability_zone",
    "created_at": "created_at",
    "crypt_key_id": "crypt_key_id",
    "expand_type": "expand_type",
    "export_location": "export_location",
    "status": "status",
    "sub_status": "sub_status",
    "share_type": "share_type",
    "subnet_id": "subnet_id",
    "security_group_id": "security_group_id",
    "size": "size",
    "share_proto": "share_proto",
    "pay_model": "pay_model",
    "version": "version",
    "vpc_id": "vpc_id"
}


class TestShare(base.TestCase):

    def setUp(self):
        super(TestShare, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = _share.Share()
        self.assertEqual('share', sot.resource_key)
        self.assertEqual('shares', sot.resources_key)
        path = '/sfs-turbo/shares'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = _share.Share(**EXAMPLE)
        self.assertEqual(EXAMPLE['az_name'], sot.az_name)
        self.assertEqual(EXAMPLE['action_progress'], sot.action_progress),
        self.assertEqual(EXAMPLE['avail_capacity'], sot.avail_capacity)
        self.assertEqual(EXAMPLE['availability_zone'], sot.availability_zone)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['crypt_key_id'], sot.crypt_key_id)
        self.assertEqual(EXAMPLE['expand_type'], sot.expand_type)
        self.assertEqual(EXAMPLE['export_location'], sot.export_location)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['sub_status'], sot.sub_status)
        self.assertEqual(EXAMPLE['share_type'], sot.share_type)
        self.assertEqual(EXAMPLE['subnet_id'], sot.subnet_id)
        self.assertEqual(EXAMPLE['security_group_id'], sot.security_group_id)
        self.assertEqual(EXAMPLE['size'], sot.size)
        self.assertEqual(EXAMPLE['share_proto'], sot.share_proto)
        self.assertEqual(EXAMPLE['pay_model'], sot.pay_model)
        self.assertEqual(EXAMPLE['version'], sot.version)
        self.assertEqual(EXAMPLE['vpc_id'], sot.vpc_id)

    def test_expand_capacity(self):
        mock_response = mock.Mock()
        mock_response.status_code = 202
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response
        self.sess.default_microversion = '1'

        sot = _share.Share.existing(id=EXAMPLE['id'])

        sot.extend_capacity(self.sess, {'new_size': 5})

        self.sess.post.assert_called_once_with(
            'sfs-turbo/shares/%s/action' % EXAMPLE['id'],
            json={'extend': {'new_size': 5}}
        )

    def test_change_security_group(self):
        mock_response = mock.Mock()
        mock_response.status_code = 202
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response
        self.sess.default_microversion = '1'

        sot = _share.Share.existing(id=EXAMPLE['id'])

        sot.change_security_group(self.sess,
                                  {'security_group_id': 'secgroup-uuid'})

        self.sess.post.assert_called_once_with(
            'sfs-turbo/shares/%s/action' % EXAMPLE['id'],
            json={'change_security_group': {
                'security_group_id': 'secgroup-uuid'}}
        )
