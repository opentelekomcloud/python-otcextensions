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
import copy

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.rds.v1 import flavor

# RDS requires those headers to be present in the request, to native API
# otherwise 404
RDS_HEADERS = {
    'Content-Type': 'application/json',
    'X-Language': 'en-us'
}

# RDS requires those headers to be present in the request, to OS-compat API
# otherwise 404
OS_HEADERS = {
    'Content-Type': 'application/json',
}

IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    # 'id': IDENTIFIER,
    'links': '1',
    'name': '2',
    'ram': 3,
    'str_id': 'some-str-id',
    # 'project_id': PROJECT_ID,
}


class TestFlavor(base.TestCase):

    def setUp(self):
        super(TestFlavor, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sot = flavor.Flavor.existing(**EXAMPLE)

    def test_basic(self):
        sot = flavor.Flavor()
        self.assertEqual('flavor', sot.resource_key)
        self.assertEqual('flavors', sot.resources_key)
        self.assertEqual('/flavors', sot.base_path)
        self.assertEqual('rds', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = flavor.Flavor.existing(**EXAMPLE)
        # self.assertEqual(EXAMPLE['str_id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['ram'], sot.ram)

    def test_list(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'flavors': [EXAMPLE]}

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess))

        self.sess.get.assert_called_once_with(
            '/flavors',
            params={},
        )

        self.assertEqual([flavor.Flavor(**EXAMPLE)], result)

    def test_get(self):

        sot = flavor.Flavor.existing(id=123)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}

        res_json = {
            "ram": 2048,
            "id": 1,
            "links": None,
            "name": "rds.pg.c2.medium",
            "specCode": "rds.pg.c2.medium",
        }

        # Sadly res_json is deleted somewhere in __GET__, so
        # pass a copy of it
        mock_response.json.return_value = copy.deepcopy(res_json)

        self.sess.get.return_value = mock_response

        res = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            'flavors/123',
        )

        self.assertEqual(2048, res.ram)
        self.assertEqual(res_json['name'], res.name)
