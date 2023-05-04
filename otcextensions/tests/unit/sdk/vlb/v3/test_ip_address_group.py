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

from otcextensions.sdk.vlb.v3 import ip_address_group

EXAMPLE = {
    'id': 'ip-address-id',
    'description': 'ip address group',
    'project_id': 'project-id',
    'name': 'ipgroup-name',
    'ip_list': [
        {
            'ip': '192.168.0.2',
            'description': 'ip description'
        }
    ],
    'listeners': [{'id': "8e92b7c3-cdae-4039-aa62-c76d09a5950a"}],
    'enterprise_project_id': 'enterprise-project-id',
    'created_at': 'created-at',
    'updated_at': 'updated-at'
}


class TestIpAddressGroup(base.TestCase):

    def setUp(self):
        super(TestIpAddressGroup, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.default_microversion = None
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.retriable_status_codes = ()
        self.sot = ip_address_group.IpAddressGroup()

    def test_basic(self):
        sot = ip_address_group.IpAddressGroup()
        self.assertEqual('ipgroup', sot.resource_key)
        self.assertEqual('ipgroups', sot.resources_key)
        self.assertEqual('/elb/ipgroups', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = ip_address_group.IpAddressGroup.existing(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(
            EXAMPLE['ip_list'][0]['ip'], sot.ip_list[0]['ip'])
        self.assertEqual(
            EXAMPLE['ip_list'][0]['description'],
            sot.ip_list[0]['description'])
        self.assertEqual(
            EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['listeners'], sot.listeners)
        self.assertEqual(
            EXAMPLE['enterprise_project_id'], sot.enterprise_project_id)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)

    def test_get(self):
        sot = ip_address_group.IpAddressGroup.existing(id=EXAMPLE['id'])
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'ipgroup': EXAMPLE.copy()}

        self.sess.get.return_value = mock_response

        result = sot.fetch(self.sess)

        self.sess.get.assert_called_once_with(
            'elb/ipgroups/%s' %
            EXAMPLE['id'],
            microversion=None,
            params={},
            skip_cache=False
        )

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['id'], result.id)
        self.assertEqual(EXAMPLE['name'], result.name)

    def test_update_ip_addresses(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = ip_address_group.IpAddressGroup.existing(id=EXAMPLE['id'])

        sot.update_ip_addresses(self.sess, ip_list=[{'ip': '192.168.0.2',
                                                     'description': 'test'}])

        self.sess.post.assert_called_once_with(
            'elb/ipgroups/%s/iplist/create-or-update' % EXAMPLE['id'],
            json={'ipgroup': {'ip_list': [{'ip': '192.168.0.2',
                                           'description': 'test'}]}}
        )

    def test_delete_ip_addresses(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {}

        self.sess.post.return_value = mock_response

        sot = ip_address_group.IpAddressGroup.existing(id=EXAMPLE['id'])

        sot.delete_ip_addresses(self.sess, ip_list=[{'ip': '192.168.0.2'}])

        self.sess.post.assert_called_once_with(
            'elb/ipgroups/%s/iplist/batch-delete' % EXAMPLE['id'],
            json={'ipgroup': {'ip_list': [{'ip': '192.168.0.2'}]}}
        )
