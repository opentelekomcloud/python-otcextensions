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
import uuid

import mock
from openstackclient.tests.unit import utils
from osc_lib import utils as _osc_lib_utils

from otcextensions.sdk.dws.v1 import cluster
from otcextensions.sdk.dws.v1 import flavor
from otcextensions.sdk.dws.v1 import snapshot
from otcextensions.tests.unit.osclient import test_base

# from collections import defaultdict
# from datetime import datetime


def gen_data(obj, columns, formatters=None):
    """Fill expected data tuple based on columns list"""
    return _osc_lib_utils.get_item_properties(
        obj, columns, formatters=formatters
    )


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list"""
    return tuple(data.get(attr, '') for attr in columns)


class TestDws(utils.TestCommand):
    def setUp(self):
        super(TestDws, self).setUp()

        self.app.client_manager.dws = mock.Mock()

        self.client = self.app.client_manager.dws


class FakeCluster(test_base.Fake):
    """Fake one or more DWS Clusters."""

    @classmethod
    def generate(cls):
        """Create a fake DWS Cluster.

        :return:
            A FakeResource object, with id, name and so on
        """

        object_info = {
            'action_progress': {},
            'availability_zone': 'eu-de-01',
            'created': '2023-01-16T02:11:19',
            # "elb": None,
            'endpoints': [{
                'connect_info': 'test.example.com',
                'jdbc_url': 'jdbc:postgresql://test.example.com:8000/gaussdb',
            }],
            'enterprise_project_id': uuid.uuid4().hex,
            'guest_agent_version': '8.1.1.202',
            'id': uuid.uuid4().hex,
            'logical_cluster_initialed': False,
            'logical_cluster_mode': False,
            'maintain_window': {
                'day': 'Thu',
                'end_time': '02:00',
                'start_time': '22:00',
            },
            'name': 'test-dws-6433a577',
            'node_type': 'dws.m3.xlarge',
            'node_type_id': uuid.uuid4().hex,
            'nodes': [{'id': uuid.uuid4().hex, 'status': '200'}],
            'number_of_free_node': 0,
            'number_of_node': 6,
            'parameter_group': {
                'id': uuid.uuid4().hex,
                'name': 'parameterGroupFor_' + uuid.uuid4().hex,
                'status': 'In-Sync',
            },
            'plugins': [
                {
                    'aarchType': 'all',
                    'autoInstall': 'install|upgrade',
                    'datastoreType': 'dws',
                    'datastoreVersion': '8.1.1.202',
                    'id': uuid.uuid4().hex,
                    'packageName': '8.1.1.202-inspect-xxxx.tar.gz',
                    'status': '0',
                    'type': 'inspect',
                    'updateTime': 1666792707000,
                    'version': '8.1.1.202',
                }
            ],
            'port': 8000,
            'private_ip': ['192.168.1.192', '192.168.1.15', '192.168.1.73'],
            'public_endpoints': [{
                'jdbc_url': 'jdbc:postgresql://test.example.com:8000/gaussdb',
                'public_connect_info': 'test.example.com',
            }],
            'public_ip': {
                'eip_address': '1.2.3.4',
                'eip_id': uuid.uuid4().hex,
                'public_bind_type': 'auto_assign',
            },
            'recent_event': 9,
            'security_group_id': uuid.uuid4().hex,
            'spec_version': 'v1.0',
            'status': 'AVAILABLE',
            'sub_status': 'NORMAL',
            'subnet_id': uuid.uuid4().hex,
            'tags': [{'key': 'key2', 'value': 'value2'}],
            'task_status': 'SNAPSHOTTING',
            'updated': '2023-01-16T02:11:19',
            'use_logical_cluster': False,
            'user_name': 'dbadmin',
            'version': '8.1.1.202',
            'vpc_id': uuid.uuid4().hex,
        }
        return cluster.Cluster(**object_info)


class FakeSnapshot(test_base.Fake):
    """Fake one or more DWS Snapshot"""

    @classmethod
    def generate(cls):
        """Create a fake DWS Snapshot.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            'id': uuid.uuid4().hex,
            'name': 'snapshot-1',
            'description': 'snapshot description',
            'started': '2016-08-23T03:59:23Z',
            'finished': '2016-08-23T04:01:40Z',
            'size': 500,
            'status': 'AVAILABLE',
            'type': 'MANUAL',
            'cluster_id': uuid.uuid4().hex,
        }
        return snapshot.Snapshot(**object_info)


class FakeFlavor(test_base.Fake):
    """Fake one or more Flavor"""

    @classmethod
    def generate(cls):
        """Create a fake DWS Flavor.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            'id': uuid.uuid4().hex,
            'availabileZones': 'eu-de-02,eu-de-01',
            'detail': [
                {'value': '4', 'type': 'vCPU'},
                {'value': '160', 'type': 'SSD', 'unit': 'GB'},
                {'value': '32', 'type': 'mem', 'unit': 'GB'},
                {'value': 'eu-de-02,eu-de-01', 'type': 'availableZones'},
            ],
            'disk_size': 160,
            'disk_type': 'SSD',
            'spec_name': 'dws.m3.xlarge',
            'mem': 32,
            'vCPU': 4,
        }

        return flavor.Flavor(**object_info)
