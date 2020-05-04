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

from otcextensions.sdk.cce.v3 import cluster
from otcextensions.sdk.cce.v3 import cluster_node
from otcextensions.tests.unit.osclient import test_base


class TestCCE(test_base.TestCommand):

    def setUp(self):
        super(TestCCE, self).setUp()

        self.app.client_manager.cce = mock.Mock()
        self.client = self.app.client_manager.cce


class FakeCluster(test_base.Fake):
    """Fake one or more Cluster"""

    @classmethod
    def generate(cls):
        object_info = {
            'kind': 'Cluster',
            'metadata': {
                'uid': 'id-' + uuid.uuid4().hex,
                'name': 'name-' + uuid.uuid4().hex,
            },
            'spec': {
                'type': random.choice(['VirtualMachine', 'BareMetal']),
                'flavor': uuid.uuid4().hex,
                'version': uuid.uuid4().hex,
                'host_network': {
                    'vpc': 'vpc-' + uuid.uuid4().hex,
                    'subnet': 'subnet-' + uuid.uuid4().hex,
                },
                'container_network': {
                    'mode': random.choice(['overlay_l2']),
                }
            },
            'status': {
                'phase': 'Available',
                'endpoints': {
                    'internal': uuid.uuid4().hex,
                    'external_otc': uuid.uuid4().hex,
                },
                'jobID': uuid.uuid4().hex
            }
        }
        obj = cluster.Cluster.existing(**object_info)
        return obj


class FakeClusterNode(test_base.Fake):
    """Fake one or more Cluster node"""

    @classmethod
    def generate(cls):
        object_info = {
            'kind': 'Node',
            'metadata': {
                'uid': 'id-' + uuid.uuid4().hex,
                'name': 'name-' + uuid.uuid4().hex,
            },
            'spec': {
                'flavor': 'flavor-' + uuid.uuid4().hex,
                'availability_zone': 'az-' + uuid.uuid4().hex,
                'os': 'os-' + uuid.uuid4().hex,
                'login': {
                    'sshKey': 'key-' + uuid.uuid4().hex,
                },
                'data_volumes': [
                    {
                        'type': 'dt' + uuid.uuid4().hex,
                        'size': random.randint(1, 15000),
                    },
                    {
                        'type': 'dt' + uuid.uuid4().hex,
                        'size': random.randint(1, 15000),
                    },
                ],
            },
            'status': {
                'phase': 'Available',
                'server_id': 'sid-' + uuid.uuid4().hex,
                'floating_ip': 'fip-' + uuid.uuid4().hex,
                'private_ip': 'pip-' + uuid.uuid4().hex,
            },
        }
        obj = cluster_node.ClusterNode.existing(**object_info)
        return obj
