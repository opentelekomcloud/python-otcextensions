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

from otcextensions.sdk.dcs.v1 import instance
from otcextensions.sdk.dcs.v1 import statistic


class TestDCS(utils.TestCommand):

    def setUp(self):
        super(TestDCS, self).setUp()

        self.app.client_manager.dcs = mock.Mock()
        self.client = self.app.client_manager.dcs

        self.client.get_instance = mock.Mock()
        self.client.find_instance = mock.Mock()
        self.client.instances = mock.Mock()
        self.client.delete_instance = mock.Mock()
        self.client.update_instance = mock.Mock()
        self.client.create_instance = mock.Mock()
        self.client.extend_instance = mock.Mock()


class FakeInstance(test_base.Fake):
    """Fake one or more Instance"""

    @classmethod
    def generate(cls):
        object_info = {
            'name': 'group-' + uuid.uuid4().hex,
            'id': 'id-' + uuid.uuid4().hex,
            'description': 'SOME description',
            'status': random.choice(['CREATING', 'CREATEFILED',
                                     'RUNNING', 'ERROR', 'STARTING',
                                     'RESTARTING', 'CLOSING', 'CLOSED',
                                     'EXTENDING']),
            'engine': uuid.uuid4().hex,
            'capacity': random.randint(1, 100),
            'ip': uuid.uuid4().hex,
            'port': random.randint(1, 65535),
            'resource_spec_code': random.choice(['dcs.single_node',
                                                 'dcs.master_standby',
                                                 'dcs.cluster'
                                                 ]),
            'engine_version': uuid.uuid4().hex,
            'internal_version': uuid.uuid4().hex,
            'charging_mode': random.randint(0, 10),
            'vpc_id': uuid.uuid4().hex,
            'vpc_name': uuid.uuid4().hex,
            'subnet_id': uuid.uuid4().hex,
            'subnet_name': uuid.uuid4().hex,
            'subnet_cidr': uuid.uuid4().hex,
            'security_group_id': uuid.uuid4().hex,
            'security_group_name': uuid.uuid4().hex,
            'created_at': uuid.uuid4().hex,
            'error_code': uuid.uuid4().hex,
            'product_id': random.choice(['OTC_DCS_SINGLE',
                                         'OTC_DCS_MS',
                                         'OTC_DCS_CL']),
            'available_zones': uuid.uuid4().hex,
            'max_memory': random.randint(0, 10),
            'used_memory': random.randint(0, 10),
            'user_id': uuid.uuid4().hex,
            'user_name': uuid.uuid4().hex,
            'order_id': uuid.uuid4().hex,
            'maintain_begin': uuid.uuid4().hex,
            'maintain_end': uuid.uuid4().hex,
        }
        obj = instance.Instance.existing(**object_info)
        return obj


class FakeStatistic(test_base.Fake):
    """Fake one or more Statistic"""

    @classmethod
    def generate(cls):
        object_info = {
            'instance_id': 'instance_id-' + uuid.uuid4().hex,
            'max_memory': random.randint(1, 65535),
            'used_memory': random.randint(1, 65535),
            'cmd_get_count': random.randint(1, 65535),
            'cmd_set_count': random.randint(1, 65535),
            'used_cpu': 'cpu-' + uuid.uuid4().hex,
            'input_kbps': 'input-' + uuid.uuid4().hex,
            'output_kbps': 'output-' + uuid.uuid4().hex,

        }
        obj = statistic.Statistic.existing(**object_info)
        return obj
