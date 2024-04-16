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


class TestPredefinedTag(base.BaseFunctionalTest):

    def setUp(self):
        super(TestPredefinedTag, self).setUp()
        self.tms = self.conn.tms

    def test_create_tag(self):
        attrs = {
            'key': 'key2',
            'value': 'value2'
        }
        self.tms.create_predefined_tag(**attrs)
        attrs = {
            'key': 'key1',
            'value': 'value1'
        }
        self.tms.create_predefined_tag(**attrs)

    def test_update_tag(self):
        attrs = {
            "new_tag": {
                "key": "check_this",
                "value": "mate"},
            "old_tag": {
                'key': 'key1',
                'value': 'value1'
            }
        }
        self.tms.update_predefined_tag(**attrs)

    def test_delete_tag(self):
        attrs = {
            'key': 'key2',
            'value': 'value2'
        }
        self.tms.delete_predefined_tag(**attrs)

    def test_tags_list(self):
        tags = list(self.tms.predefined_tags())
        self.assertGreaterEqual(len(tags), 0)

    def test_clear_tags(self):
        attrs = {
            "key": "check_this",
            "value": "mate"
        }
        self.tms.delete_predefined_tag(**attrs)
        attrs = {
            'key': 'key1',
            'value': 'value1'
        }
        self.tms.delete_predefined_tag(**attrs)

