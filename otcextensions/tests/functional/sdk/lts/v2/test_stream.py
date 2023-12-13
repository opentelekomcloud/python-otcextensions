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


class TestStream(base.BaseFunctionalTest):

    def setUp(self):
        super(TestStream, self).setUp()
        self.lts = self.conn.lts
        self.log_group_name = 'teststream' + uuid.uuid4().hex[:8]
        self.log_stream_name = 'teststream' + uuid.uuid4().hex[:8]
        self.log_group = self.lts.create_group(
            log_group_name=self.log_group_name,
            ttl_in_days=5
        )
        self.assertIsNotNone(self.log_group)
        self.assertIsNotNone(self.log_group.id)

        attrs = {
            'log_group': self.log_group.id,
            'log_stream_name': self.log_stream_name,
            'ttl_in_days': 5
        }
        self.log_stream = self.lts.create_stream(**attrs)
        self.assertIsNotNone(self.log_stream)
        self.assertIsNotNone(self.log_stream.id)

    def test_list(self):
        objects = list(self.lts.streams(log_group=self.log_group.id))
        self.assertGreaterEqual(len(objects), 0)

    def tearDown(self):
        super(TestStream, self).tearDown()
        log_stream = self.lts.delete_stream(log_stream=self.log_stream.id,
                                            log_group=self.log_group.id,
                                            ignore_missing=False)
        self.assertIsNone(log_stream)
        log_stream = self.lts.delete_stream(log_stream=self.log_stream.id,
                                            log_group=self.log_group.id,
                                            ignore_missing=True)
        self.assertIsNone(log_stream)
        log_group = self.lts.delete_group(group=self.log_group.id)
        self.assertIsNone(log_group)
