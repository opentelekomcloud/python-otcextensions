#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
# import datetime
import random
import uuid

import mock

from openstackclient.tests.unit import utils
from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.dms.v1 import group
from otcextensions.sdk.dms.v1 import queue
from otcextensions.sdk.dms.v1 import quota


class TestDMS(utils.TestCommand):

    def setUp(self):
        super(TestDMS, self).setUp()

        self.app.client_manager.dms = mock.Mock()


class FakeQueue(test_base.Fake):
    """Fake one or more Queue"""

    @classmethod
    def generate(cls):
        object_info = {
            'name': 'group-' + uuid.uuid4().hex,
            'id': 'id-' + uuid.uuid4().hex,
            'description': 'SOME description',
            'queue_mode': random.choice(['NORMAL', 'FIFO',
                                         'KAFKA_HA', 'KAFKA_HT']),
            'redrive_policy': random.choice(['enable', 'disable']),
            'max_consume_count': random.randint(1, 100),
            'retention_hours': random.randint(1, 72)
        }
        obj = queue.Queue.existing(**object_info)
        return obj


class FakeGroup(test_base.Fake):
    """Fake one or more Group"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'group-' + uuid.uuid4().hex,
            'produced_messages': random.randint(1, 100),
            'consumed_messages': random.randint(1, 100),
            'available_messages': random.randint(1, 100),
            'produced_deadletters': random.randint(1, 100),
            'available_deadletters': random.randint(1, 100),
        }
        obj = group.Group.existing(**object_info)
        return obj


class FakeQuota(test_base.Fake):
    """Fake one or more Quota"""

    @classmethod
    def generate(cls):
        object_info = {
            'type': 'type-' + uuid.uuid4().hex,
            'quota': random.randint(1, 100),
            'min': random.randint(1, 100),
            'max': random.randint(1, 100),
            'used': random.randint(1, 100),
        }
        obj = quota.Quota.existing(**object_info)
        return obj
