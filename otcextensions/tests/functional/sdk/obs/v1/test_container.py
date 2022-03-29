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
import openstack
import uuid

from otcextensions.tests.functional import base

_logger = openstack._log.setup_logging('openstack')


class TestContainer(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    bucket_name = 'obs-test-' + uuid_v4
    container = None

    def setUp(self):
        super(TestContainer, self).setUp()
        self.client = self.conn.obs
        self.container = self.client.create_container(
            name=self.bucket_name,
            storage_acl='public-read-write',
            storage_class='STANDARD'
        )
        self.addCleanup(self.client.delete_container, self.container)

    def test_01_get_container(self):
        bucket = self.client.get_container(self.bucket_name)
        self.assertIsNotNone(bucket)
        self.assertIsNotNone(bucket.name, self.bucket_name)

    def test_02_list_containers(self):
        containers = list(self.client.containers())
        self.assertIsNotNone(containers)
