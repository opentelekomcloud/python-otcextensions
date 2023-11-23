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
import random
import string

from openstack import _log

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestGroup(base.BaseFunctionalTest):

    def setUp(self):
        super(TestGroup, self).setUp()
        self.lts = self.conn.lts

    def test_list(self):
        objects = list(self.lts.groups())
        self.assertGreaterEqual(len(objects), 0)

    def test_create(self):
        attrs = {
            'log_group_name': print(''.join(
                random.choices(string.ascii_lowercase, k=5))),
            'ttl_in_days': 5
        }
        log_group = self.lts.create_group(**attrs)
        self.assertIsNotNone(log_group.id)

    def test_delete(self):
        attrs = {
            'log_group_name': print(''.join(
                random.choices(string.ascii_lowercase, k=5))),
            'ttl_in_days': 5
        }
        log_group = self.lts.create_group(**attrs)
        self.assertIsNotNone(log_group.id)
