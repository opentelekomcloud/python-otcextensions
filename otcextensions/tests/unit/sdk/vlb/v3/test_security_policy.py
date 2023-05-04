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

from otcextensions.sdk.vlb.v3 import security_policy

EXAMPLE = {
    'id': 'sec-policy-id',
    'description': 'description',
    'project_id': 'project-id',
    'name': 'name',
    'protocols': ["TLSv1.3", "TLSv1.1"],
    'listeners': [{'id': "8e92b7c3-cdae-4039-aa62-c76d09a5950a"}],
    'enterprise_project_id': 'enterprise-project-id',
    'ciphers': ["TLS_AES_128_GCM_SHA256"],
    'created_at': 'created-at',
    'updated_at': 'updated-at'
}


class TestSecurityPolicy(base.TestCase):

    def setUp(self):
        super(TestSecurityPolicy, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.default_microversion = None
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.retriable_status_codes = ()
        self.sot = security_policy.SecurityPolicy()

    def test_basic(self):
        sot = security_policy.SecurityPolicy()
        self.assertEqual('security_policy', sot.resource_key)
        self.assertEqual('security_policies', sot.resources_key)
        self.assertEqual('/elb/security-policies', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = security_policy.SecurityPolicy.existing(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['ciphers'], sot.ciphers)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['listeners'], sot.listeners)
        self.assertEqual(EXAMPLE['protocols'], sot.protocols)
        self.assertEqual(EXAMPLE['enterprise_project_id'],
                         sot.enterprise_project_id)
        self.assertEqual(EXAMPLE['listeners'], sot.listeners)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)

    def test_get(self):
        sot = security_policy.SecurityPolicy.existing(id=EXAMPLE['id'])
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'security_policy': EXAMPLE.copy()}

        self.sess.get.return_value = mock_response

        result = sot.fetch(self.sess)

        self.sess.get.assert_called_once_with(
            'elb/security-policies/%s' %
            EXAMPLE['id'],
            microversion=None,
            params={},
            skip_cache=False
        )

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['id'], result.id)
        self.assertEqual(EXAMPLE['name'], result.name)
