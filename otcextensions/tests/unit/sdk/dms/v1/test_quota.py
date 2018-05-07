# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import copy

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.dms.v1 import quota

EXAMPLE_LIST = {
    'quotas': {
        'resources': [
            {
                'type': 'queue',
                'used': 2,
                'quota': 25,
                'min': 1,
                'max': 50
            }
        ]
    }
}


class TestQuota(base.TestCase):

    def setUp(self):
        super(TestQuota, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()

        self.sot = quota.Quota()

    def test_basic(self):
        sot = quota.Quota()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('quotas.resources', sot.resources_key)
        self.assertEqual('/quotas/dms', sot.base_path)
        self.assertEqual('dms', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        obj = EXAMPLE_LIST['quotas']['resources'][0]
        sot = quota.Quota.existing(**obj)
        self.assertEqual(obj['type'], sot.type)
        self.assertEqual(obj['used'], sot.used)
        self.assertEqual(obj['quota'], sot.quota)
        self.assertEqual(obj['min'], sot.min)
        self.assertEqual(obj['max'], sot.max)


    def test_list(self):
        sot = quota.Quota()
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST)

        self.sess.get.return_value = mock_response

        result = list(sot.list(self.sess))

        self.sess.get.assert_called_once_with('/quotas/dms', params={})

        expected_list = [
            quota.Quota.existing(
                **EXAMPLE_LIST['quotas']['resources'][0])
                        ]

        self.assertEqual(expected_list, result)
