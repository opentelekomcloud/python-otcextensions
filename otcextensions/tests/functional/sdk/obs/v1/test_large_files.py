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
import uuid
from otcextensions.tests.functional import base


class TestObsLargeFiles(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    bucket_name = 'obs-test-' + uuid_v4
    container = None

    def setUp(self):
        super(TestObsLargeFiles, self).setUp()
        self.client = self.conn.obs
        self.container = self.client.create_container(
            name=self.bucket_name,
            storage_acl='public-read-write',
            storage_class='STANDARD'
        )
        self.addCleanup(self.client.delete_container, self.container)

    def test_01_upload_large_file(self):
        fh = open("/mnt/d/Jellyfin/series/alien/s01.mkv", "rb")
        self.client.create_object(
            container=self.container,
            name='largefile',
            data=fh
        )
        self.object = self.client.get_object_metadata(
            container=self.container,
            obj='largefile'
        )
        self.client.delete_object(self.object)
