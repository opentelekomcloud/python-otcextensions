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

from otcextensions.sdk.elb.v2 import elb_certificate

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "id": FAKE_ID,
    "name": "fake_name",
    "private_key": "fake",
    "certificate": "fake",
    "update_time": 1499817600,
    "create_time": 1499817600
}


class TestElbCertificate(base.TestCase):

    def setUp(self):
        super(TestElbCertificate, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

    def test_basic(self):
        sot = elb_certificate.Certificate()

        self.assertEqual('/lbaas/certificates', sot.base_path)
        self.assertEqual('certificates', sot.resources_key)
        self.assertIsNone(sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make(self):
        sot = elb_certificate.Certificate(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['update_time'], sot.update_time)
        self.assertEqual(EXAMPLE['create_time'], sot.create_time)

        self.assertDictEqual({
            'limit': 'limit',
            'marker': 'marker'},
            sot._query_mapping._mapping
        )
