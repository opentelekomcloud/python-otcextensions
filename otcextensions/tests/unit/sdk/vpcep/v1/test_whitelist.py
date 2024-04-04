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
#
import uuid

import mock
from keystoneauth1 import adapter

from openstack.tests.unit import base
from otcextensions.sdk.vpcep.v1 import whitelist
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

VPCEP_SERVICE_ID = uuid.uuid4().hex

EXAMPLE = {
    'id': uuid.uuid4().hex,
    'permission': '*',
    'created_at': '2018-10-18T13:26:40Z',
}


class TestWhitelist(base.TestCase):
    def setUp(self):
        super(TestWhitelist, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = whitelist.Whitelist()
        self.assertEqual('permissions', sot.resources_key)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(
            '/vpc-endpoint-services/%(endpoint_service_id)s/permissions',
            sot.base_path,
        )
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = whitelist.Whitelist(**EXAMPLE)
        assert_attributes_equal(self, sot, EXAMPLE)

    def test_action(self):
        sot = whitelist.Whitelist.existing(
            id=None, endpoint_service_id=VPCEP_SERVICE_ID
        )
        action = 'add'
        domains = ['123', '456']
        formatted_domains = []
        for domain in domains:
            formatted_domains.append('iam:domain::' + domain)
        json_body = {'permissions': formatted_domains, 'action': action}
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {'permissions': formatted_domains}
        response.headers = {}
        self.sess.post.return_value = response

        rt = list(sot._action(self.sess, action, domains))
        self.sess.post.assert_called_with(
            'vpc-endpoint-services/%s/permissions/action' % VPCEP_SERVICE_ID,
            json=json_body,
        )
        self.assertEqual(
            rt[0],
            whitelist.Whitelist.existing(permission=formatted_domains[0]),
        )

    def test_add(self):
        sot = whitelist.Whitelist.existing(
            id=None, endpoint_service_id=VPCEP_SERVICE_ID
        )
        sot._action = mock.Mock()

        domains = ['123', '456']
        rt = sot.add(self.sess, domains)
        sot._action.assert_called_with(self.sess, 'add', domains)
        self.assertIsNotNone(rt)

    def test_remove(self):
        sot = whitelist.Whitelist.existing(
            id=None, endpoint_service_id=VPCEP_SERVICE_ID
        )
        sot._action = mock.Mock()

        domains = ['123', '456']
        rt = sot.remove(self.sess, domains)
        sot._action.assert_called_with(self.sess, 'remove', domains)
        self.assertIsNotNone(rt)
