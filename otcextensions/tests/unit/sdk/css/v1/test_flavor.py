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

import mock
from keystoneauth1 import adapter

from openstack.tests.unit import base
from otcextensions.sdk.css.v1 import flavor

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"

EXAMPLE = {
    "versions": [
        {
            "type": "ess",
            "version": "7.6.2",
            "flavors": [
                {
                    "cpu": 1,
                    "ram": 8,
                    "name": "css.medium.8",
                    "region": "eu-de",
                    "diskrange": "40,640",
                    "availableAZ": "eu-de-01,eu-de-02,eu-de-03",
                    "flavor_id": "6b6c0bcf-750d-4f8a-b6f5-c45a143f5198",
                }
            ],
        }
    ]
}


class TestFlavor(base.TestCase):

    def setUp(self):
        super(TestFlavor, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)

    def test_basic(self):
        sot = flavor.Flavor()

        self.assertEqual('/flavors', sot.base_path)
        self.assertEqual('flavors', sot.resources_key)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        data = EXAMPLE['versions'][0]['flavors'][0]
        sot = flavor.Flavor(**data)
        self.assertEqual(data['name'], sot.name)
        self.assertEqual(data['cpu'], sot.vcpus)
        self.assertEqual(data['ram'], sot.ram)
        self.assertEqual(data['region'], sot.region)
        self.assertEqual(data['diskrange'], sot.disk_range)
        self.assertEqual(data['flavor_id'], sot.id)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(EXAMPLE)

        self.sess.get.return_value = mock_response

        sot = flavor.Flavor()

        result = list(sot.list(self.sess))

        self.assertEqual(1, len(result))
        self.assertEqual(EXAMPLE['versions'][0]['version'], result[0].version)
        self.assertEqual(EXAMPLE['versions'][0]['type'], result[0].type)
