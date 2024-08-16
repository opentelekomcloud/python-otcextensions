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
    bucket_name = 's3-test-' + uuid_v4
    container = None
    region = 'eu-de'

    def setUp(self):
        super(TestContainer, self).setUp()
        self.client = self.conn.s3
        self.container = self.client.create_container(
            container_name=self.bucket_name,
            region=self.region
        )

    def tearDown(self):
        container = self.client.delete_container(
            container_name=self.bucket_name,
            region=self.region)
        self.assertIsNotNone(container)

    def test_01_get_container(self):
        bucket = self.client.get_container(container_name=self.bucket_name,
                                           region=self.region)
        self.assertIsNotNone(bucket)

    def test_02_list_containers(self):
        containers = list(self.client.containers(region=self.region))
        self.assertIsNotNone(containers)

    def test_03_put_container_acl(self):
        container = self.client.put_container_acl(
            container_name=self.bucket_name,
            region=self.region, ACL='private')
        self.assertIsNotNone(container)

    def test_04_get_container_acl(self):
        container = self.client.get_container_acl(
            container_name=self.bucket_name,
            region=self.region)
        self.assertIsNotNone(container)
