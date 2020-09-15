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

from openstack.tests.unit import base

from otcextensions.sdk.identity.v3 import agency


FAKE_ID = "945d-fe449be00148"
EXAMPLE = {
    "trust_domain_name": "exampledomain",
    "description": " testsfdas ",
    "trust_domain_id": "b3f266d0c08544a0859740de8b84e850",
    "id": "afca8ddf2e92469a8fd26a635da5206f",
    "duration": None,
    "create_time": "2017-01-04T09:09:15.000000",
    "expire_time": None,
    "domain_id": "0ae9c6993a2e47bb8c4c7a9bb8278d61",
    "name": "exampleagency"
}


class TestAgency(base.TestCase):

    def setUp(self):
        super(TestAgency, self).setUp()

    def test_basic(self):
        sot = agency.Agency()

        self.assertEqual('/v3.0/OS-AGENCY/agencies', sot.base_path)
        self.assertEqual('agencies', sot.resources_key)
        self.assertEqual('agency', sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

        self.assertDictEqual({
            'domain_id': 'domain_id',
            'limit': 'limit',
            'marker': 'marker',
            'name': 'name',
            'trust_domain_id': 'trust_domain_id'},
            sot._query_mapping._mapping
        )

    def test_make_it(self):

        sot = agency.Agency(connection=self.cloud, **EXAMPLE)
        # Check how the override with "real" connection works
        self.assertEqual(
            'https://identity.example.com/v3.0/OS-AGENCY/agencies',
            sot.base_path)

        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['trust_domain_id'], sot.trust_domain_id)
        self.assertEqual(EXAMPLE['create_time'], sot.created_at)
        self.assertEqual(EXAMPLE['expire_time'], sot.expire_at)
        self.assertEqual(EXAMPLE['domain_id'], sot.domain_id)
