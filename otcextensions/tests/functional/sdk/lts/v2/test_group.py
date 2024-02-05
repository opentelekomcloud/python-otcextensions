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

from openstack import _log

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestGroup(base.BaseFunctionalTest):

    def setUp(self):
        super(TestGroup, self).setUp()
        self.lts = self.conn.lts
        self.log_group_name = 'testgroup' + uuid.uuid4().hex[:8]
        attrs = {
            'log_group_name': self.log_group_name,
            'ttl_in_days': 5
        }
        self.log_group = self.lts.create_group(**attrs)
        self.assertIsNotNone(self.log_group.id)

    def tearDown(self):
        super(TestGroup, self).tearDown()
        log_group = self.lts.delete_group(group=self.log_group.id,
                                          ignore_missing=False)
        self.assertIsNone(log_group)
        log_group = self.lts.delete_group(group=self.log_group.id,
                                          ignore_missing=True)
        self.assertIsNone(log_group)

    def test_list(self):
        objects = list(self.lts.groups())
        self.assertGreaterEqual(len(objects), 0)

    def test_update(self):
        attrs = {
            'ttl_in_days': 7
        }
        log_group = self.lts.update_group(group=self.log_group.id,
                                          **attrs)
        self.assertEqual(log_group.ttl_in_days, 7)
