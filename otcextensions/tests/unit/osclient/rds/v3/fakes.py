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
import random
import uuid

import mock

from openstackclient.tests.unit import utils

from otcextensions.tests.unit.osclient import test_base

#from otcextensions.sdk.rds.v3.configuration import ConfigurationGroup
from otcextensions.sdk.rds.v3.datastore import Datastore
from otcextensions.sdk.rds.v3 import flavor
from otcextensions.sdk.rds.v3.instance import Instance
from otcextensions.sdk.rds.v3 import backup


class TestRds(utils.TestCommand):

    def setUp(self):
        super(TestRds, self).setUp()

        self.app.client_manager.rds = mock.Mock()

        self.client = self.app.client_manager.rds

        self.datastore_mock = FakeDatastore
        self.flavor_mock = FakeFlavor
        self.instance_mock = FakeInstance
        #self.configuration_mock = FakeConfiguration


class FakeDatastore(object):
    """Fake one or more datastore versions."""

    @staticmethod
    def create_one(attrs=None, methods=None):
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
            'name': 'name-' + uuid.uuid4().hex
        }

        # Overwrite default attributes.
        # object_info.update(attrs)
        return Datastore(**object_info)

    @staticmethod
    def create_multiple(attrs=None, methods=None, count=2):
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
            objects.append(FakeDatastore.create_one(attrs, methods))

        return objects


class FakeFlavor(test_base.Fake):
    """Fake one or more VBS Policy"""

    @classmethod
    def generate(cls):
        object_info = {
            'instance_mode': random.choice(['ha', 'replica', 'single']),
            'vcpus': str(random.randint(1, 100)),
            'spec_code': uuid.uuid4().hex,
            'ram': random.randint(1, 10280),
        }
        obj = flavor.Flavor.existing(**object_info)
        return obj


# class FakeConfiguration(object):
#    """Fake one or more Configuration."""
#
#    @staticmethod
#    def create_one(attrs=None, methods=None):
#        """Create a fake Configuration.
#
#        :param Dictionary attrs:
#            A dictionary with all attributes
#        :param Dictionary methods:
#            A dictionary with all methods
#        :return:
#            A FakeResource object, with id, name, metadata, and so on
#        """
#        attrs = attrs or {}
#        methods = methods or {}
#
#        # Set default attributes.
#        object_info = {
#            'id': 'id-' + uuid.uuid4().hex,
#            'name': 'name-' + uuid.uuid4().hex,
#            'description': 'descriptions-' + uuid.uuid4().hex,
#            'datastore_name': uuid.uuid4().hex,
#            'datastore_version_name': uuid.uuid4().hex,
#            'values': {},
#        }
#
#        # Overwrite default attributes.
#        # object_info.update(attrs)
#        return ConfigurationGroup(**object_info)
#
#    @staticmethod
#    def create_multiple(attrs=None, methods=None, count=2):
#        """Create multiple fake Configuration.
#
#        :param Dictionary attrs:
#            A dictionary with all attributes
#        :param Dictionary methods:
#            A dictionary with all methods
#        :param int count:
#            The number of servers to fake
#        :return:
#            A list of FakeResource objects faking the servers
#        """
#        objects = []
#        for i in range(0, count):
#            objects.append(
#                FakeConfiguration.create_one(attrs, methods)
#            )
#
#        return objects
#
#
class FakeInstance(object):
    """Fake one or more Instance."""

    @staticmethod
    def create_one(attrs=None, methods=None):
        """Create a fake Configuration.

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
            'status': 'status-' + uuid.uuid4().hex,
            'datastore': {
                'type': 'datastore-' + uuid.uuid4().hex,
                'version': 'version-' + uuid.uuid4().hex,
            },
            'flavor_ref': {'id': uuid.uuid4().hex},
            'volume': {
                'type': 'type' + uuid.uuid4().hex,
                'size': random.randint(1, 10280),
            },
            'region': 'region' + uuid.uuid4().hex,
        }

        # Overwrite default attributes.
        # object_info.update(attrs)
        return Instance(**object_info)

    @staticmethod
    def create_multiple(attrs=None, methods=None, count=2):
        """Create multiple fake Configuration.

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
            objects.append(
                FakeInstance.create_one(attrs, methods)
            )

        return objects


class FakeBackup(test_base.Fake):
    """Fake one or more VBS Policy"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'description': uuid.uuid4().hex,
            'datastore': {
                'type': 'datastore-' + uuid.uuid4().hex,
                'version': 'version-' + uuid.uuid4().hex,
            },
            'instance_id': 'instance_id-' + uuid.uuid4().hex,
            'size': random.randint(0, 100),
            'status': random.choice(['BUILDING', 'COMPLETED', 'FAILED',
                                     'DELETING']),
            'type': random.choice(['auto', 'manual']),
            'begin_time': uuid.uuid4().hex,
            'end_time': uuid.uuid4().hex
        }
        obj = backup.Backup.existing(**object_info)
        return obj
