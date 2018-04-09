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
import datetime
import random
import uuid

import mock

from openstackclient.tests.unit import utils

from otcextensions.sdk.kms.v1 import key
# from otcextensions.sdk.kms.v1 import data_key


class TestKMS(utils.TestCommand):

    def setUp(self):
        super(TestKMS, self).setUp()

        self.app.client_manager.kms = mock.Mock()


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


class FakeCMK(Fake):
    """Fake one or more CMK"""

    @classmethod
    def generate(cls):
        object_info = {
            'creation_date': datetime.datetime(
                random.randint(2000, 2020),
                random.randint(1, 12),
                random.randint(1, 28)
            ),
            'scheduled_deletion_date': datetime.datetime(
                random.randint(2000, 2020),
                random.randint(1, 12),
                random.randint(1, 28)
            ),
            'key_alias': 'alias-' + uuid.uuid4().hex,
            'id': 'id-' + uuid.uuid4().hex,
            'domain_id': 'domain-' + uuid.uuid4().hex,
            'key_status': 'SOME STATUS',
            'key_description': 'description-' + uuid.uuid4().hex,
            'realm': 'realm-' + uuid.uuid4().hex,
            'key_type': 'type-' + uuid.uuid4().hex,
        }
        obj = key.Key.existing(**object_info)
        return obj
