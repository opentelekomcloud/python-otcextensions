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

from otcextensions.sdk.dms.v1 import group
from otcextensions.sdk.dms.v1 import queue


class TestDMS(utils.TestCommand):

    def setUp(self):
        super(TestDMS, self).setUp()

        self.app.client_manager.dms = mock.Mock()


class Fake(object):

    @classmethod
    def create_one(cls, attrs=None):
        """Create a fake resource.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param Dictionary methods:
            A dictionary with all methods
        :return:
            A FakeResource object, with id, name, metadata, and so on
        """
        attrs = attrs or {}

        resource = cls.generate()
        # new_attrs = cls.generate()

        resource.update(attrs)

        return resource

    @classmethod
    def create_multiple(cls, count=2, attrs=None):
        """Create multiple fake resources.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param int count:
            The number of address scopes to fake
        :return:
            A list of FakeResource objects faking the address scopes
        """
        objects = []
        for i in range(0, count):
            objects.append(
                cls.create_one(attrs))

        return objects


class FakeQueue(Fake):
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


class FakeGroup(Fake):
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
