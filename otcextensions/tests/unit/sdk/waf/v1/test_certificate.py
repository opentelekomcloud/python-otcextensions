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

from otcextensions.sdk.waf.v1 import certificate


FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "id": FAKE_ID,
    "name": "fake_name",
    "content": "fake",
    "key": "fake",
    "timestamp": 1499817600,
    "expire_time": 1499817600
}


class TestCertificate(base.TestCase):

    def setUp(self):
        super(TestCertificate, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

    def test_basic(self):
        sot = certificate.Certificate()

        self.assertEqual('/waf/certificate', sot.base_path)
        self.assertEqual('items', sot.resources_key)
        self.assertIsNone(sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):

        sot = certificate.Certificate(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['expire_time'], sot.expire_time)
        self.assertEqual(EXAMPLE['timestamp'], sot.timestamp)

        self.assertDictEqual({
            'limit': 'limit',
            'marker': 'marker',
            'offset': 'offset'},
            sot._query_mapping._mapping
        )
