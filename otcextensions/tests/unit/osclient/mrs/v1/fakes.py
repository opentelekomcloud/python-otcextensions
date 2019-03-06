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

from otcextensions.sdk.mrs.v1 import host
from otcextensions.sdk.mrs.v1 import host_type
from otcextensions.sdk.mrs.v1 import server


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


class TestMrs(utils.TestCommand):

    def setUp(self):
        super(TestMrs, self).setUp()

        self.app.client_manager.mrs = mock.Mock()
        self.client = self.app.client_manager.mrs


class FakeHost(test_base.Fake):
    """Fake one or more Host"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            # 'dedicated_host_ids': ['id-' + uuid.uuid4().hex],
            'name': uuid.uuid4().hex,
            'auto_placement': random.choice(['on', 'off']),
            'availability_zone': uuid.uuid4().hex,
            'state': random.choice(['available', 'fault', 'released']),
            'project_id': uuid.uuid4().hex,
            'available_vcpus': random.randint(1, 600),
            'available_memory': random.randint(1, 600),
            'instance_total': random.randint(1, 600),
            'allocated_at': uuid.uuid4().hex,
            'released_at': uuid.uuid4().hex,
            'host_properties': {
                'vcpus': random.randint(1, 600),
                'cores': random.randint(1, 600),
                'sockets': random.randint(1, 600),
                'memory': random.randint(1, 600),
                'host_type': uuid.uuid4().hex,
                'host_type_name': uuid.uuid4().hex,
                'available_instance_capacities': [
                    {'flavor': uuid.uuid4().hex}
                ],
            }
        }
        obj = host.Host.existing(**object_info)
        return obj


class FakeHostType(test_base.Fake):
    """Fake one or more Host type"""

    @classmethod
    def generate(cls):
        object_info = {
            'host_type': uuid.uuid4().hex,
            'host_type_name': uuid.uuid4().hex,
        }
        obj = host_type.HostType.existing(**object_info)
        return obj


class FakeServer(test_base.Fake):
    """Fake one or more HostServers"""

    @classmethod
    def generate(cls):
        object_info = {
            'addresses': {
                'id-' + uuid.uuid4().hex: [{
                    'addr': 'addr-' + uuid.uuid4().hex,
                    'version': 4
                }]
            },
            'created_at': uuid.uuid4().hex,
            'updated_at': uuid.uuid4().hex,
            'flavor': {'id-' + uuid.uuid4().hex},
            'id': 'id-' + uuid.uuid4().hex,
            'metadata': {
                'os_type': uuid.uuid4().hex
            },
            'name': uuid.uuid4().hex,
            'status': uuid.uuid4().hex,
            'tenant_id': uuid.uuid4().hex,
            'user_id': uuid.uuid4().hex
        }
        obj = server.Server.existing(**object_info)
        return obj
