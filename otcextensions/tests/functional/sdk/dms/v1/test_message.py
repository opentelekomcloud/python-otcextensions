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
# from openstack import exceptions
# from openstack import utils

from otcextensions.tests.functional import base
import time

_logger = openstack._log.setup_logging('openstack')


class TestMessage(base.BaseFunctionalTest):
    QUEUE_ALIAS = 'sdk_test_queue'
    queues = []
    groups = []
    messages = []
    received_messages = []

    def setUp(self):
        super(TestMessage, self).setUp()
        openstack.enable_logging(debug=True, http_debug=True)
        try:
            self.queue = self.conn.dms.create_queue(
                name=TestMessage.QUEUE_ALIAS
            )

        except openstack.exceptions.BadRequestException:
            self.queue = self.conn.dms.find_queue(TestMessage.QUEUE_ALIAS)

        self.queues.append(self.queue)

        try:
            self.group = self.conn.dms.create_group(
                self.queue, "test_group"
            )

        except openstack.exceptions.DuplicateResource:
            self.queue = self.conn.dms.groups(self.queue)

        self.groups.append(self.group)

    def tearDown(self):
        super(TestMessage, self).tearDown()
        try:
            for queue in self.queues:
                if queue.id:
                    self.conn.dms.delete_queue(queue)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_list(self):
        self.queues = list(self.conn.dms.queues())
        self.assertGreaterEqual(len(self.queues), 0)
        if len(self.queues) > 0:
            queue = self.queues[0]
            q = self.conn.dms.get_queue(queue=queue.id)
            self.assertIsNotNone(q)

    def test_group(self):
        self.queues = list(self.conn.dms.queues())
        # self.assertGreaterEqual(len(self.queues), 0)
        if len(self.queues) > 0:
            # queue = self.queues[0]
            # q = self.conn.dms.get_queue(queue=queue.id)
            # self.assertIsNotNone(q)
            try:
                self.group = self.conn.dms.create_group(
                    self.queue, "test_group2"
                )

            except openstack.exceptions.BadRequestException:
                self.queue = self.conn.dms.groups(self.queue)

            self.groups.append(self.group)

    # OS_TEST_TIMEOUT=60 is needed due to testbed slowness
    def test_message(self):
        self.queues = list(self.conn.dms.queues())
        # self.assertGreaterEqual(len(self.queues), 0)
        if len(self.queues) > 0:
            # queue = self.queues[0]
            # q = self.conn.dms.get_queue(queue=queue.id)
            time.sleep(50)

            # self.assertIsNotNone(q)
            self.message = self.conn.dms.send_messages(
                self.queue,
                messages=[
                    {"body": "TEST11",
                        "attributes":
                            {
                                "attribute1": "value1",
                                "attribute2": "value2"}}
                ]
            )
            #        ,{ "body" : { "foo" : "test02" },
            #        "attributes" : {
            #            "attribute1" : "value1",
            #            "attribute2" : "value2" } }

            self.messages.append(self.message)
            try:
                self.group = self.conn.dms.create_group(
                    self.queue, "test_group3"
                )

            except openstack.exceptions.BadRequestException:
                self.queue = self.conn.dms.groups(self.queue)

            self.groups.append(self.group)

            self.received_messages = self.conn.dms.consume_message(
                self.queue,
                self.group
            )
            self.assertGreaterEqual(len(list(self.received_messages)), 0)
