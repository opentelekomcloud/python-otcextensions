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
from otcextensions.tests.functional.sdk.apig import TestApiG


class TestTags(TestApiG):

    def setUp(self):
        super(TestTags, self).setUp()
        self.create_gateway()

    def tearDown(self):
        super(TestTags, self).tearDown()
        self.delete_gateway()

    def test_list_tags(self):
        tags = list(self.client.tags(gateway=TestTags.gateway))
        print("Tags:", tags)
        self.assertGreater(len(tags), 0, "No tags found")
