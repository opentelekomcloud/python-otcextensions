# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import copy

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.cce.v1 import cluster_node

OS_HEADERS = {
    'Content-Type': 'application/json',
}

EXAMPLE_LIST = {
    'kind': 'list',
    'apiVersion': 'v1',
    'metadata': {},
    'spec': {
        'hostList': [{
            'kind': 'host',
            'apiVersion': 'v1',
            'metadata': {
                'name': 'ag-test-node-1',
                'uuid': '580add6d-db4a-4571-ae02-9b3364818f8a',
                'spaceuuid': 'de213bc4-4949-2a70-1a28-ae6c54e4ea23',
                'createAt': '2018-04-03 13:37:27.993379777 +0000 UTC',
                'updateAt': '2018-04-03 13:37:27.993379777 +0000 UTC'},
            'spec': {
                'clusteruuid': '5a66a449-668c-492f-8c33-5cdbdeaadd2e',
                'clustername': 'ag-test',
                'flavor': 's1.medium',
                'cpu': 1,
                'memory': 4096,
                'label': 'fake',
                'status': {
                    'capacity': {
                        'cpu': '',
                        'memory': '',
                        'pods': ''
                    },
                    'allocatable': {
                        'cpu': '',
                        'memory': '',
                        'pods': ''
                    },
                    'conditions': None,
                    'addresses': None,
                    'daemonEndpoints': {
                        'kubeletEndpoint': {'Port': 0}
                    },
                    'nodeInfo': {
                        'machineID': '',
                        'systemUUID': '',
                        'bootID': '',
                        'kernelVersion': '',
                        'osImage': '',
                        'containerRuntimeVersion': '',
                        'kubeletVersion': '',
                        'kubeProxyVersion': ''},
                    'images': None
                }
            },
            'replicas': 1,
            'status': 'BUILD'
        }]
    }
}

EXAMPLE_CREATE = {
    "kind": "host",
    "apiVersion": "v1",
    "spec": {
        "flavor": "s1.medium",
        "label": "",
        "volume": [{
            "diskType": "root",
            "diskSize": 40,
            "volumeType": "SAS"
        }, {
            "diskType": "data",
            "diskSize": 100,
            "volumeType": "SATA"
        }],
        "sshkey": "SSHkey-1864",
        "snat": False,
        "az": "eu-de-01",
        "tags": ["aaa.111", "bbb.222"]
    },
    "replicas": 1
}


class TestClusterNode(base.TestCase):

    def setUp(self):
        super(TestClusterNode, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.delete = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.get = mock.Mock()

        self.sot = cluster_node.ClusterNode(cluster_uuid='cluster_uuid')

    def test_basic(self):
        sot = cluster_node.ClusterNode()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)
        self.assertEqual('/clusters/%(cluster_uuid)s/hosts',
                         sot.base_path)
        self.assertEqual('cce', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    # def test_make_it(self):
    #     obj = EXAMPLE_LIST[0]
    #     sot = cluster.Cluster.existing(**obj)
    #     self.assertEqual(obj['metadata']['uuid'], sot.id)
    #     self.assertEqual(obj['kind'], sot.kind)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST)

        self.sess.get.return_value = mock_response

        result = list(
            self.sot.list(
                self.sess,
                headers=OS_HEADERS,
                cluster_uuid='cluster_uuid',
            )
        )

        self.sess.get.assert_called_once_with(
            '/clusters/%s/hosts' % self.sot.cluster_uuid,
            params={},
            headers=OS_HEADERS
        )

        expected_list = [
            cluster_node.ClusterNode.existing(
                **EXAMPLE_LIST['spec']['hostList'][0]),
        ]

        self.assertEqual(expected_list, result)

    def test_get(self):
        host = EXAMPLE_LIST['spec']['hostList'][0]
        sot = cluster_node.ClusterNode.existing(
            id=host['metadata']['uuid'],
            cluster_uuid='cluster_uuid'
        )

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = host.copy()

        self.sess.get.return_value = mock_response

        result = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            'clusters/%s/hosts/%s' % (
                'cluster_uuid',
                sot.id
            ),
            headers=OS_HEADERS
        )

        self.assertDictEqual(
            cluster_node.ClusterNode.existing(**host).to_dict(),
            result.to_dict()
        )

    def test_delete(self):
        sot = cluster_node.ClusterNode.existing(
            cluster_uuid='bla',
            **EXAMPLE_LIST['spec']['hostList'][0])

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = None

        self.sess.delete.return_value = mock_response

        sot.delete(self.sess)

        self.sess.delete.assert_called_once_with(
            '/clusters/%s/hosts' % 'bla',
            json={'hosts': [{'name': 'ag-test-node-1'}]},
            headers=OS_HEADERS)

    def test_create(self):
        sot = cluster_node.ClusterNode.new(
            cluster_uuid='bla',
            **EXAMPLE_CREATE)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = [{}]

        self.sess.post.return_value = mock_response

        sot.create(self.sess)

        self.sess.post.assert_called_once_with(
            '/clusters/%s/hosts' % 'bla',
            json=EXAMPLE_CREATE,
            headers=OS_HEADERS)
