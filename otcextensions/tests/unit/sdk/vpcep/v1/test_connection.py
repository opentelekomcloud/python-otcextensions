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
from otcextensions.sdk.vpcep.v1 import connection
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

VPCEP_SERVICE_ID = uuid.uuid4().hex

EXAMPLE = {
    'id': uuid.uuid4().hex,
    'status': 'accepted',
    'marker_id': 16777510,
    'domain_id': '5fc973eea581490997e82ea11a1df31f',
    'created_at': '2018-09-17T11:10:11Z',
    'updated_at': '2018-09-17T11:10:12Z',
}


class TestConnection(base.TestCase):

    def setUp(self):
        super(TestConnection, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = connection.Connection()
        self.assertEqual('connections', sot.resources_key)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(
            '/vpc-endpoint-services/%(endpoint_service_id)s/connections',
            sot.base_path,
        )

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

        self.assertDictEqual(
            {
                'id': 'id',
                'limit': 'limit',
                'marker': 'marker',
                'marker_id': 'marker_id',
                'offset': 'offset',
                'sort_dir': 'sort_dir',
                'sort_key': 'sort_key',
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = connection.Connection(**EXAMPLE)
        assert_attributes_equal(self, sot, EXAMPLE)

    def test_action(self):
        sot = connection.Connection.existing(
            id=None, endpoint_service_id=VPCEP_SERVICE_ID
        )
        action = 'receive'
        endpoints = ['123', '456']
        json_body = {'endpoints': endpoints, 'action': action}
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {'connections': [EXAMPLE]}
        response.headers = {}
        self.sess.post.return_value = response

        rt = list(sot._action(self.sess, action, endpoints))
        self.sess.post.assert_called_with(
            'vpc-endpoint-services/%s/connections/action' % VPCEP_SERVICE_ID,
            json=json_body,
        )
        self.assertEqual(rt, [connection.Connection.existing(**EXAMPLE)])

    def test_receive(self):
        sot = connection.Connection.existing(
            id=None, endpoint_service_id=VPCEP_SERVICE_ID
        )
        sot._action = mock.Mock()

        endpoints = ['123', '456']
        rt = sot.accept(self.sess, endpoints)
        sot._action.assert_called_with(self.sess, 'receive', endpoints)
        self.assertIsNotNone(rt)

    def test_reject(self):
        sot = connection.Connection.existing(
            id=None, endpoint_service_id=VPCEP_SERVICE_ID
        )
        sot._action = mock.Mock()

        endpoints = ['123', '456']
        rt = sot.reject(self.sess, endpoints)
        sot._action.assert_called_with(self.sess, 'reject', endpoints)
        self.assertIsNotNone(rt)
