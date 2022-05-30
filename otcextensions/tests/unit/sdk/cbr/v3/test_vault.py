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

from otcextensions.sdk.cbr.v3 import vault

EXAMPLE = {
    'id': 'vault-id',
    'auto_bind': False,
    'auto_expand': False,
    'description': 'my vault',
    'billing': {
        'protect_type': 'backup',
        'object_type': 'server',
        'size': 40,
        'cloud_type': 'public',
        'consistent_level': 'crash_consistent',
        'charging_mode': 'post_paid'
    },
    'name': 'vault-name',
    'resources': [
        {
            'name': 'server-name',
            'type': 'OS::Nova::Server',
            'id': 'server-id',
        }
    ]
}


class TestVault(base.TestCase):

    def setUp(self):
        super(TestVault, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.default_microversion = None
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.retriable_status_codes = ()
        self.sot = vault.Vault()

    def test_basic(self):
        sot = vault.Vault()
        self.assertEqual('vault', sot.resource_key)
        self.assertEqual('vaults', sot.resources_key)
        self.assertEqual('/vaults', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = vault.Vault.existing(**EXAMPLE)
        self.assertFalse(sot.auto_bind)
        self.assertFalse(sot.auto_expand)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(
            EXAMPLE['billing']['protect_type'], sot.billing.protect_type)
        self.assertEqual(
            EXAMPLE['billing']['object_type'], sot.billing.object_type)
        self.assertEqual(
            EXAMPLE['billing']['size'], sot.billing.size)
        self.assertEqual(
            EXAMPLE['billing']['cloud_type'], sot.billing.cloud_type)
        self.assertEqual(
            EXAMPLE['billing']['consistent_level'],
            sot.billing.consistent_level)
        self.assertEqual(
            EXAMPLE['billing']['charging_mode'], sot.billing.charging_mode)
        self.assertEqual(
            EXAMPLE['name'], sot.name)
        self.assertEqual(
            EXAMPLE['resources'][0]['name'],
            sot.resources[0].name)
        self.assertEqual(
            EXAMPLE['resources'][0]['type'],
            sot.resources[0].type)
        self.assertEqual(
            EXAMPLE['resources'][0]['id'],
            sot.resources[0].id)

    def test_get(self):
        sot = vault.Vault.existing(
            id=EXAMPLE['id'])
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'vault': EXAMPLE.copy()}

        self.sess.get.return_value = mock_response

        result = sot.fetch(self.sess)

        self.sess.get.assert_called_once_with(
            'vaults/%s' %
            EXAMPLE['id'],
            microversion=None,
            params={}
        )

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['id'], result.id)
        self.assertEqual(EXAMPLE['name'], result.name)

    def test_bind_policy(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = vault.Vault.existing(id=EXAMPLE['id'])

        sot.bind_policy(self.sess, 'policy_id')

        self.sess.post.assert_called_once_with(
            'vaults/%s/associatepolicy' % EXAMPLE['id'],
            json={'policy_id': 'policy_id'}
        )

    def test_unbind_policy(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = vault.Vault.existing(id=EXAMPLE['id'])

        sot.unbind_policy(self.sess, 'policy_id')

        self.sess.post.assert_called_once_with(
            'vaults/%s/dissociatepolicy' % EXAMPLE['id'],
            json={'policy_id': 'policy_id'}
        )

    def test_associate_resources(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        resources = [{
            'id': 'server1_id',
            'type': 'OS::Nova::Server'
        }, {
            'id': 'server2_id',
            'type': 'OS::Nova::Server'}
        ]
        sot = vault.Vault.existing(id=EXAMPLE['id'])

        sot.associate_resources(self.sess, resources)

        self.sess.post.assert_called_once_with(
            'vaults/%s/addresources' % EXAMPLE['id'],
            json={'resources': resources}
        )

    def test_dissociate_resources(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        resources = ['id1', 'id2']
        sot = vault.Vault.existing(id=EXAMPLE['id'])

        sot.dissociate_resources(self.sess, resources)

        self.sess.post.assert_called_once_with(
            'vaults/%s/removeresources' % EXAMPLE['id'],
            json={'resource_ids': resources}
        )
