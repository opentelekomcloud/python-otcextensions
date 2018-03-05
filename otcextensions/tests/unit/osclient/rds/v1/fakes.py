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
# import datetime
import random
import uuid

import mock
# from osc_lib import utils as common_utils

# from openstackclient.tests.unit import fakes
from openstackclient.tests.unit import utils

from otcextensions.sdk.rds.v1.datastore import Datastore
from otcextensions.sdk.rds.v1.flavor import Flavor


class TestRds(utils.TestCommand):

    def setUp(self):
        super(TestRds, self).setUp()

        self.app.client_manager.rds = mock.Mock()

        self.datastore_mock = FakeDatastore
        self.flavor_mock = FakeFlavor


class FakeDatastore(object):
    """Fake one or more datastore versions."""

    @staticmethod
    def create_one_datastore(attrs=None, methods=None):
        """Create a fake datastore.

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
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'datastore': 'datastore-' + uuid.uuid4().hex,
            'image': 'image-' + uuid.uuid4().hex,
            'packages': 'packages-' + uuid.uuid4().hex,
        }

        # Overwrite default attributes.
        # object_info.update(attrs)
        return Datastore(**object_info)

    @staticmethod
    def create_datastores(attrs=None, methods=None, count=2):
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
            objects.append(FakeDatastore.create_one_datastore(attrs, methods))

        return objects


class FakeFlavor(object):
    """Fake one or more Flavor."""

    @staticmethod
    def create_one_flavor(attrs=None, methods=None):
        """Create a fake flavor.

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
            'str_id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'ram': random.randint(1, 10280),
            'specCode': 'image-' + uuid.uuid4().hex,
            'flavor_detail': None,
            'price_detail': None,
            # 'flavor': 'flavor-' + uuid.uuid4().hex,
        }

        # Overwrite default attributes.
        # object_info.update(attrs)
        return Flavor(**object_info)

    @staticmethod
    def create_flavors(attrs=None, methods=None, count=2):
        """Create multiple fake flavors.

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
            objects.append(FakeFlavor.create_one_flavor(attrs, methods))

        return objects
