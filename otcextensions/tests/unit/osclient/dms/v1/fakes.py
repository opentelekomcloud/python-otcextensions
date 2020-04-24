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
from otcextensions.sdk.dms.v1 import instance
from otcextensions.sdk.dms.v1 import queue
from otcextensions.sdk.dms.v1 import quota
from otcextensions.sdk.dms.v1 import topic


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


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


class FakeInstance(test_base.Fake):
    @classmethod
    def generate(cls):
        object_info = {
            'name': 'name-' + uuid.uuid4().hex,
            'description': 'name-' + uuid.uuid4().hex,
            'engine_name': 'engine-' + uuid.uuid4().hex,
            'engine_version': 'ver-' + uuid.uuid4().hex,
            'storage': random.randint(1, 100),
            'access_user': 'user-' + uuid.uuid4().hex,
            'password': uuid.uuid4().hex,
            'router_id': 'router_id-' + uuid.uuid4().hex,
            'router_name': 'router_name-' + uuid.uuid4().hex,
            'network_id': 'net_id-' + uuid.uuid4().hex,
            'subnet_name': 'subnet_name-' + uuid.uuid4().hex,
            'security_group_id': 'security_group_id-' + uuid.uuid4().hex,
            'security_group_name': 'security_group_name-' + uuid.uuid4().hex,
            'availability_zones': ['az' + uuid.uuid4().hex],
            'product_id': 'product-' + uuid.uuid4().hex,
            'maintenance_begin': 'mb-' + uuid.uuid4().hex,
            'maintenance_end': 'me-' + uuid.uuid4().hex,
            'is_public': random.choice([True, False]),
            'is_ssl': random.choice([True, False]),
            'kafka_public_status': 'kps-' + uuid.uuid4().hex,
            'public_bandwidth': random.randint(1, 100),
            'retention_policy': random.choice(['produce_reject', 'time_base']),
            'storage_spec_code': random.choice(['dms.physical.storage.high',
                                                'dms.physical.storage.ultra'])
        }

        obj = instance.Instance.existing(**object_info)
        return obj


class FakeTopic(test_base.Fake):
    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'replication': random.randint(1, 3),
            'partition': random.randint(1, 21),
            'retention_time': random.randint(1, 169),
            'is_sync_replication': random.choice([True, False]),
            'is_sync_flush': random.choice([True, False]),
            'instance_id': 'iid-' + uuid.uuid4().hex
        }

        obj = topic.Topic.existing(**object_info)
        return obj
