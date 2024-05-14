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

from openstack import _log

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestResourceTag(base.BaseFunctionalTest):
    def setUp(self):
        super(TestResourceTag, self).setUp()
        self.tms = self.conn.tms

    def test_create_tag(self):
        attrs = {
            "project_id": "786ef11caa5c43ff80256be4c7fee8b7",
            "resources": [{"resource_id": "2079d0a6-3dbc-4d59-99da-6b8b7c899a97",
                           "resource_type": "vpc"}],
            "tags": [{"key": "ENV1", "value": "dev1"}],
        }
        result = self.tms.create_resource_tag(**attrs)
        self.assertNotEqual(result, None)

    def test_delete_tag(self):
        attrs = {
            "project_id": "786ef11caa5c43ff80256be4c7fee8b7",
            "resources": [{"resource_id": "2079d0a6-3dbc-4d59-99da-6b8b7c899a97",
                           "resource_type": "vpc"}],
            "tags": [{"key": "ENV1", "value": "dev1"}],
        }
        result = self.tms.delete_resource_tag(**attrs)
        self.assertNotEqual(result, None)

    def test_tags_list(self):
        query = {
            "resource_id": "2079d0a6-3dbc-4d59-99da-6b8b7c899a97",
            "resource_type": "vpc",
            "project_id": "786ef11caa5c43ff80256be4c7fee8b7"
        }
        tags = list(self.tms.resource_tags(**query))
        self.assertGreaterEqual(len(tags), 0)
