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
from otcextensions.tests.functional import base
import uuid


class TestObsCleanup(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    bucket_name = 'obs-test-' + uuid_v4
    object_name = f'obs{uuid_v4}.object'
    folder_name = f'folder{uuid_v4}/'
    data = str(uuid.uuid4())

    def setUp(self):
        super(TestObsCleanup, self).setUp()
        self.client = self.conn.obs
        self.container = self.client.create_container(
            name=self.bucket_name,
            storage_acl='public-read-write',
            storage_class='STANDARD'
        )
        self.object = self.client.create_object(
            container=self.container,
            name=self.object_name,
            data=self.data
        )
        self.folder = self.client.create_object(
            container=self.container,
            name=self.folder_name
        )
        self.nested_object_name = f"{self.folder_name}nest_{self.uuid_v4}.txt"
        self.nested_object = self.client.create_object(
            container=self.container,
            name=self.nested_object_name,
            data="nested test data"
        )

    def test_cleanup(self):
        containers = list(self.client.containers())
        self.assertGreaterEqual(len(containers), 1)
        self.client._service_cleanup(dry_run=False, cont_name=self.bucket_name)
        containers = list(self.client.containers())
        self.assertEqual(len(containers), 0)
