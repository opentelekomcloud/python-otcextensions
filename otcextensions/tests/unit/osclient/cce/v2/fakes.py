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
from otcextensions.sdk.cce.v3 import node_pool
from otcextensions.sdk.cce.v3 import cluster_cert
from otcextensions.tests.unit.osclient import test_base


class TestCCE(test_base.TestCommand):

    def setUp(self):
        super(TestCCE, self).setUp()

        self.app.client_manager.cce = mock.Mock()
        self.app.client_manager.sdk_connection = mock.Mock()
        self.client = self.app.client_manager.cce
        self.sdk_client = self.app.client_manager.sdk_connection


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
                'rootVolume': {
                    'type': 'SATA',
                    'size': random.randint(40, 100)
                },
                'dataVolumes': [
                    {
                        'type': 'SSD',
                        'size': random.randint(1, 15000),
                    },
                    {
                        'type': 'SAS',
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


class FakeNodePool(test_base.Fake):
    """Fake one or more CCE Nodepools"""

    @classmethod
    def generate(cls):
        object_info = {
            'kind': 'NodePool',
            'apiVersion': 'v3',
            'metadata': {
                'name': 'name-' + uuid.uuid4().hex
            },
            'spec': {
                'initialNodeCount': 0,
                'type': 'vm',
                'autoscaling': {
                    'enable': random.choice([True, False]),
                    'minNodeCount': 0,
                    'maxNodeCount': random.randint(0, 100),
                    'scaleDownCooldownTime': random.randint(1, 10),
                    'priority': random.randint(1, 99)
                },
                'nodeManagement': {
                    'serverGroupReference': 'sg-' + uuid.uuid4().hex
                },
                'nodeTemplate': {
                    'flavor': 's2.large.2 ',
                    'az': random.choice([
                        'random',
                        'eu-de-01',
                        'eu-de-02',
                        'eu-de-03']),
                    'os': 'EulerOS 2.5',
                    'login': {
                        'sshKey': 'key-' + uuid.uuid4().hex
                    },
                    'rootVolume': {
                        'volumetype': random.choice(['SAS', 'SATA', 'SSD']),
                        'size': random.randint(40, 32768),
                    },
                    'dataVolumes': [
                        {
                            'volumetype': random.choice([
                                'SAS', 'SATA', 'SSD']),
                            'size': random.randint(100, 32768),
                            'extendParam': {
                                'useType': 'docker'
                            }
                        }
                    ],
                    'billingMode': 0,
                    'extendParam': {
                        'alpha.cce/preInstall': 'bHMgLWw=',
                        'alpha.cce/postInstall': 'bHMgLWwK',
                        'maxPods': 110,
                    },
                    'k8sTags': {
                        't1-' + uuid.uuid4().hex: 'v1-' + uuid.uuid4().hex,
                        't2-' + uuid.uuid4().hex: 'v2-' + uuid.uuid4().hex,
                    },
                    'taints': [
                        {
                            'key': 'key-' + uuid.uuid4().hex,
                            'value': 'value-' + uuid.uuid4().hex,
                            'effect': random.choice([
                                'NoSchedule',
                                'PrefereNoSchedule',
                                'NoExecute'])
                        },
                        {
                            'key': 'key-' + uuid.uuid4().hex,
                            'value': 'value-' + uuid.uuid4().hex,
                            'effect': random.choice([
                                'NoSchedule',
                                'PrefereNoSchedule',
                                'NoExecute'])
                        }
                    ],
                    'userTags': [
                        {
                            'key': 'key-' + uuid.uuid4().hex,
                            'value': 'value-' + uuid.uuid4().hex,
                        },
                        {
                            'key': 'key-' + uuid.uuid4().hex,
                            'value': 'value-' + uuid.uuid4().hex,
                        }
                    ],
                    'nodeNicSpec': {
                        'primaryNic': {
                            'subnetId': 'nw-' + uuid.uuid4().hex,
                        }
                    }
                }
            },
            'status': {
                'currentNode': random.randint(0, 100),
                'phase': ''
            }
        }
        obj = node_pool.NodePool.existing(**object_info)
        return obj


class FakeClusterCertificate(test_base.Fake):
    """Fake one or more Cluster Certificate"""

    @classmethod
    def generate(cls):
        object_info = {
            'ca': uuid.uuid4().hex,
            'client_certificate': uuid.uuid4().hex,
            'client_key': uuid.uuid4().hex,
            'context': {
                'name': uuid.uuid4().hex[:8],
                'user': uuid.uuid4().hex[:8],
                'cluster': uuid.uuid4().hex[:8],
            },
        }
        obj = cluster_cert.ClusterCertificate.existing(**object_info)
        return obj
