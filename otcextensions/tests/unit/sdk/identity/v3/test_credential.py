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

from otcextensions.sdk.identity.v3 import credential


FAKE_ID = "945d-fe449be00148"
EXAMPLE = {
    "access": FAKE_ID,
    "create_time": "2020-01-08T06:26:08.123059Z",
    "user_id": "07609fb9358010e21f7bc0037...",
    "description": "",
    "status": "active"
}


class TestCredential(base.TestCase):

    def setUp(self):
        super(TestCredential, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

    def test_basic(self):
        sot = credential.Credential()

        self.assertEqual('/v3.0/OS-CREDENTIAL/credentials', sot.base_path)
        self.assertEqual('credentials', sot.resources_key)
        self.assertEqual('credential', sot.resource_key)
        self.assertEqual('PUT', sot.commit_method)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):

        sot = credential.Credential(connection=self.cloud, **EXAMPLE)
        # Check how the override with "real" connection works
        self.assertEqual(
            'https://identity.example.com/v3.0/OS-CREDENTIAL/credentials',
            sot.base_path)

        self.assertEqual(EXAMPLE['access'], sot.id)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['create_time'], sot.created_at)
