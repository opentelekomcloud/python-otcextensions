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
import random
import uuid

import mock

from otcextensions.sdk.cce.v1 import cluster
from otcextensions.sdk.cce.v1 import cluster_node
from otcextensions.tests.unit.osclient import test_base


class TestCCE(test_base.TestCommand):

    def setUp(self):
        super(TestCCE, self).setUp()

        self.app.client_manager.cce = mock.Mock()
        self.client = self.app.client_manager.cce


class FakeCluster(test_base.Fake):
    """Fake one or more Cluster"""

    @classmethod
    def generate(cls, cnt_hosts=1):
        hosts = []
        for i in range(cnt_hosts - 1):
            host = {'kind': 'host'}
            hosts.append(host)
        object_info = {
            'kind': 'cluster',
            'metadata': {
                'uuid': 'id-' + uuid.uuid4().hex,
                'name': 'name-' + uuid.uuid4().hex,
            },
            'spec': {
                'cpu': random.randint(1, 15),
                'memory': random.randint(1, 150000),
                'endpoint': 'endpoint-' + uuid.uuid4().hex,
                'availability_zone': 'az-' + uuid.uuid4().hex,
                'vpc': 'vpc-' + uuid.uuid4().hex,
                'hostList': {
                    'spec': {
                        'hostList': hosts
                    }
                }
            },
            'status': {
                'status': 'sts'
            }
        }
        obj = cluster.Cluster.existing(**object_info)
        return obj

    @classmethod
    def create_one(cls, cnt_hosts=1):
        """Create a fake resource.
        """
        resource = cls.generate(cnt_hosts)

        return resource

    @classmethod
    def create_multiple(cls, count=2, attrs=None):
        """Create multiple fake resources.
        """
        objects = []
        for i in range(0, count):
            objects.append(
                cls.create_one(1))

        return objects


class FakeClusterNode(test_base.Fake):
    """Fake one or more Cluster node"""

    @classmethod
    def generate(cls):
        object_info = {
            'kind': 'host',
            'metadata': {
                'uuid': 'id-' + uuid.uuid4().hex,
                'name': 'name-' + uuid.uuid4().hex,
            },
            'spec': {
                'cluster_uuid': 'clid-' + uuid.uuid4().hex,
                'cpu': random.randint(1, 15),
                'memory': random.randint(1, 150000),
                'availability_zone': 'az-' + uuid.uuid4().hex,
                'flavor': 'flavor-' + uuid.uuid4().hex,
                'public_ip': 'public_ip-' + uuid.uuid4().hex,
                'private_ip': 'private_ip-' + uuid.uuid4().hex,
                'volume': [
                    {
                        'disk_type': 'dt' + uuid.uuid4().hex,
                        'disk_size': random.randint(1, 15000),
                    },
                    {
                        'disk_type': 'dt' + uuid.uuid4().hex,
                        'disk_size': random.randint(1, 15000),
                    },
                ],
                'status': {
                    'capacity': {
                        'cpu': random.randint(1, 15),
                        'memory': random.randint(1, 15000),
                        'pods': random.randint(1, 15000),
                    },
                    'allocatable': {
                        'cpu': random.randint(1, 15),
                        'memory': random.randint(1, 15000),
                        'pods': random.randint(1, 15000),
                    },
                    'conditions': []
                },
            },
            'status': 'sts'
        }
        obj = cluster_node.ClusterNode.existing(**object_info)
        return obj
