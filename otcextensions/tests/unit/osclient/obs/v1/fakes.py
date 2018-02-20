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
#

# import copy
import datetime
import random
import uuid

import mock
# from osc_lib import utils as common_utils

# from openstackclient.tests.unit import fakes
from openstackclient.tests.unit import utils

from otcextensions.sdk.obs.v1.bucket import Bucket
from otcextensions.sdk.obs.v1.object import Object

# from otcextensions.obs.v1.api import API


class TestObs(utils.TestCommand):

    def setUp(self):
        super(TestObs, self).setUp()

        self.app.client_manager.obs = mock.Mock()

        # s3api = API(client=self.app.client_manager.obs)
        # self.app.client_manager.obs.api = s3api

        self.bucket_mock = FakeBucket
        self.object_mock = FakeObject


class FakeBucket(object):
    """Fake one or more compute servers."""

    @staticmethod
    def create_one_bucket(attrs=None, methods=None):
        """Create a fake server.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param Dictionary methods:
            A dictionary with all methods
        :return:
            A FakeResource object, with id, name, metadata, and so on
        """
        attrs = attrs or {}
        methods = methods or {}

        # Set default attributes.
        object_info = {
            'creationdate': datetime.datetime(
                random.randint(2000, 2020),
                random.randint(1, 12),
                random.randint(1, 28)
            ),
            'name': 'bucket-' + uuid.uuid4().hex,
        }

        # Overwrite default attributes.
        # object_info.update(attrs)
        return Bucket(**object_info)

    @staticmethod
    def create_buckets(attrs=None, methods=None, count=2):
        """Create multiple fake servers.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param Dictionary methods:
            A dictionary with all methods
        :param int count:
            The number of servers to fake
        :return:
            A list of FakeResource objects faking the servers
        """
        objects = []
        for i in range(0, count):
            objects.append(FakeBucket.create_one_bucket(attrs, methods))

        return objects


class FakeObject(object):
    """Fake one or more compute servers."""

    @staticmethod
    def create_one_object(attrs=None, methods=None):
        """Create a fake server.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param Dictionary methods:
            A dictionary with all methods
        :return:
            A FakeResource object, with id, name, metadata, and so on
        """
        attrs = attrs or {}
        methods = methods or {}

        # Set default attributes.
        object_info = {
            'key': 'object-key-' + uuid.uuid4().hex,
            'size': random.randint(1, 99999999999),
            'lastmodified': datetime.datetime(
                random.randint(2000, 2020),
                random.randint(1, 12),
                random.randint(1, 28)
            ),
            'etag': 'image-id-' + uuid.uuid4().hex,
            'storageclass': 'storage-class-' + uuid.uuid4().hex,
        }

        # Overwrite default attributes.
        # object_info.update(attrs)
        return Object(**object_info)

    @staticmethod
    def create_objects(attrs=None, methods=None, count=2):
        """Create multiple fake servers.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param Dictionary methods:
            A dictionary with all methods
        :param int count:
            The number of servers to fake
        :return:
            A list of FakeResource objects faking the servers
        """
        objects = []
        for i in range(0, count):
            objects.append(FakeObject.create_one_object(attrs, methods))

        return objects
