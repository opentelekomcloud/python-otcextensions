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
from openstack import exceptions

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestQueue(base.BaseFunctionalTest):
    QUEUE_ALIAS = 'sdk_test_queue'
    queues = []

    def setUp(self):
        super(TestQueue, self).setUp()
        try:
            self.queue = self.conn.dms.create_queue(
                name=TestQueue.QUEUE_ALIAS
            )
        except exceptions.DuplicateResource:
            self.queue = self.conn.dms.find_queue(alias=TestQueue.QUEUE_ALIAS)

        self.queues.append(self.queue)

    def tearDown(self):
        super(TestQueue, self).tearDown()
        try:
            for queue in self.queues:
                if queue.id:
                    self.conn.dms.delete_queue(queue)
        except exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_list(self):
        self.queues = list(self.conn.dms.queues())
        self.assertGreaterEqual(len(self.queues), 0)
        if len(self.queues) > 0:
            queue = self.queues[0]
            q = self.conn.dms.get_queue(queue=queue.id)
            self.assertIsNotNone(q)
