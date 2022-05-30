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
import random
import uuid
import time

import mock

from openstackclient.tests.unit import utils
from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.dns.v2 import zone
from otcextensions.sdk.dns.v2 import nameserver
from otcextensions.sdk.dns.v2 import recordset
from otcextensions.sdk.dns.v2 import floating_ip


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


class TestDNS(utils.TestCommand):

    def setUp(self):
        super(TestDNS, self).setUp()

        self.app.client_manager.dns = mock.Mock()
        self.client = self.app.client_manager.dns


class FakeZone(test_base.Fake):
    """Fake one or more Zone"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': uuid.uuid4().hex,
            'action': uuid.uuid4().hex,
            'created_at': uuid.uuid4().hex,
            'description': uuid.uuid4().hex,
            'email': uuid.uuid4().hex,
            'pool_id': uuid.uuid4().hex,
            'record_num': random.randint(1, 600),
            'router': {
                'router_id': uuid.uuid4().hex,
                'router_region': uuid.uuid4().hex,
                'status': uuid.uuid4().hex,
            },
            'serial': random.randint(1, 600),
            'status': uuid.uuid4().hex,
            'ttl': random.randint(1, 600),
            'updated_at': time.time() * 1000,
            'zone_type': uuid.uuid4().hex,
        }
        obj = zone.Zone.existing(**object_info)
        return obj


class FakeNameserver(test_base.Fake):
    """Fake one or more Zone"""

    @classmethod
    def generate(cls):
        object_info = {
            'zone_id': 'id-' + uuid.uuid4().hex,
            'address': uuid.uuid4().hex,
            'hostname': uuid.uuid4().hex,
            'priority': random.randint(1, 600),
        }
        obj = nameserver.NameServer.existing(**object_info)
        return obj


class FakeRecordset(test_base.Fake):
    """Fake one or more recordset"""

    @classmethod
    def generate(cls):
        object_info = {
            'zone_id': 'id-' + uuid.uuid4().hex,
            'name': uuid.uuid4().hex,
            'description': uuid.uuid4().hex,
            'status': uuid.uuid4().hex,
            'ttl': random.randint(1, 600),
            'type': random.choice(['A', 'AAAA', 'SRV']),
            'records': list(random.randint(1, 600) for i in range(0, 5))
        }
        obj = recordset.Recordset.existing(**object_info)
        return obj


class FakeFloatingIP(test_base.Fake):
    """Fake one or more recordset"""

    @classmethod
    def generate(cls):
        object_info = {
            'address': uuid.uuid4().hex,
            'floating_ip_id': uuid.uuid4().hex,
            'region': uuid.uuid4().hex,
            'id': uuid.uuid4().hex,
            'ptrdname': uuid.uuid4().hex,
            'description': uuid.uuid4().hex,
            'ttl': random.randint(1, 600),
        }
        obj = floating_ip.FloatingIP.existing(**object_info)
        return obj
