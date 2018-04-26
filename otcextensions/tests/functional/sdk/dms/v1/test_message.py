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
from openstack import utils

from otcextensions.tests.functional import base
import time

_logger = _log.setup_logging('openstack')


class TestMessage(base.BaseFunctionalTest):
    QUEUE_ALIAS = 'sdk_test_queue'
    queues = []
    groups = []
    messages = []

    @classmethod
    def setUpClass(cls):
        super(TestMessage, cls).setUpClass()
        utils.enable_logging(debug=True, http_debug=True)
        try:
            cls.queue = cls.conn.dms.create_queue(
                name=TestMessage.QUEUE_ALIAS
            )

        except exceptions.BadRequestException:
            cls.queue = cls.conn.dms.get_queue(TestMessage.QUEUE_ALIAS)

        cls.queues.append(cls.queue)

        try:
            cls.group = cls.conn.dms.create_groups
            (
                cls.queue,
                groups = [{"name": "test_group"}]
            )

        except exceptions.DuplicateResource:
            cls.queue = cls.conn.dms.groups(cls.queue)

        cls.groups.append(cls.group)

    @classmethod
    def tearDownClass(cls):
        try:
            for queue in cls.queues:
                if queue.id:
                    cls.conn.dms.delete_queue(queue)
        except exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_list(cls):
        cls.queues = list(cls.conn.dms.queues())
        cls.assertGreaterEqual(len(cls.queues), 0)
        if len(cls.queues) > 0:
            queue = cls.queues[0]
            q = cls.conn.dms.get_queue(queue=queue.id)
            cls.assertIsNotNone(q)

    def test_group(cls):
        cls.queues = list(cls.conn.dms.queues())
        # cls.assertGreaterEqual(len(cls.queues), 0)
        if len(cls.queues) > 0:
            # queue = cls.queues[0]
            # q = cls.conn.dms.get_queue(queue=queue.id)
            # cls.assertIsNotNone(q)
            try:
                cls.group = cls.conn.dms.create_groups(
                    cls.queue, groups=[{"name": "test_group"}]
                )

            except exceptions.BadRequestException:
                cls.queue = cls.conn.dms.groups(cls.queue)

            cls.groups.append(cls.group)

    @classmethod
    def test_message(cls):
        cls.queues = list(cls.conn.dms.queues())
        # cls.assertGreaterEqual(len(cls.queues), 0)
        if len(cls.queues) > 0:
            # queue = cls.queues[0]
            # q = cls.conn.dms.get_queue(queue=queue.id)
            time.sleep(1)
            # cls.assertIsNotNone(q)
            cls.message = cls.conn.dms.send_messages(
                cls.queue, messages=[
                    {"body": "TEST11",
                        "attributes":
                            {
                                "attribute1": "value1",
                                "attribute2": "value2"}}
                            ])
            #        ,{ "body" : { "foo" : "test02" },
            #        "attributes" : {
            #            "attribute1" : "value1",
            #            "attribute2" : "value2" } }

            cls.messages.append(cls.message)
