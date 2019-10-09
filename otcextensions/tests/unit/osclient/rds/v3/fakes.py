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
#
import random
import uuid

import mock

from openstackclient.tests.unit import utils

from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.rds.v3 import configuration
from otcextensions.sdk.rds.v3 import datastore
from otcextensions.sdk.rds.v3 import flavor
from otcextensions.sdk.rds.v3 import instance
from otcextensions.sdk.rds.v3 import backup


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestRds(utils.TestCommand):
    def setUp(self):
        super(TestRds, self).setUp()

        self.app.client_manager.rds = mock.Mock()

        self.client = self.app.client_manager.rds

        self.datastore_mock = FakeDatastore
        self.flavor_mock = FakeFlavor
        self.instance_mock = FakeInstance
        self.backup_mock = FakeBackup
        self.configuration_mock = FakeConfiguration


class FakeDatastore(test_base.Fake):
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
        return datastore.Datastore(**object_info)

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


class FakeConfiguration(test_base.Fake):
    """Fake one or more Configuration."""

    @classmethod
    def generate(cls):
        """Create a fake Configuration.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param Dictionary methods:
            A dictionary with all methods
        :return:
            A FakeResource object, with id, name, metadata, and so on
        """
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'description': 'descriptions-' + uuid.uuid4().hex,
            'datastore_name': uuid.uuid4().hex,
            'datastore_version_name': uuid.uuid4().hex,
            'values': {},
            'configuration_parameters':
                list({
                    'name': 'name-' + uuid.uuid4().hex,
                    'value': 'value-' + uuid.uuid4().hex,
                    'restart_required': bool(random.getrandbits(1)),
                    'readonly': bool(random.getrandbits(1)),
                    'value_range': uuid.uuid4().hex,
                    'type': 'type-' + uuid.uuid4().hex,
                    'description': 'descr-' + uuid.uuid4().hex

                } for i in range(3)),
            'is_user_defined': bool(random.getrandbits(1))

        }

        obj = configuration.Configuration.existing(**object_info)
        return obj


class FakeInstance(test_base.Fake):
    """Fake one or more Instance."""
    @classmethod
    def generate(cls):
        """Create a fake Configuration.

        :return:
            A FakeResource object, with id, name, metadata, and so on
        """

        # Set default attributes.
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'status': 'status-' + uuid.uuid4().hex,
            'datastore': {
                'type': 'datastore-' + uuid.uuid4().hex,
                'version': 'version-' + uuid.uuid4().hex,
            },
            'flavor_ref': {
                'id': uuid.uuid4().hex
            },
            'volume': {
                'type': 'type' + uuid.uuid4().hex,
                'size': random.randint(1, 10280),
            },
            'region': 'region' + uuid.uuid4().hex,
        }

        return instance.Instance(**object_info)


class FakeBackup(test_base.Fake):
    """Fake one or more Backup"""
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
            'status':
            random.choice(['BUILDING', 'COMPLETED', 'FAILED', 'DELETING']),
            'type': random.choice(['auto', 'manual']),
            'begin_time': uuid.uuid4().hex,
            'end_time': uuid.uuid4().hex
        }
        obj = backup.Backup.existing(**object_info)
        return obj


class FakeBackupFile(test_base.Fake):
    """Fake one or more BackupFile"""
    @classmethod
    def generate(cls):
        object_info = {
            'size': random.randint(1, 100000),
            'name': 'name-' + uuid.uuid4().hex,
            'download_link': uuid.uuid4().hex,
            'expires_at': 'expires-' + uuid.uuid4().hex
        }
        obj = backup.BackupFile.existing(**object_info)
        return obj
