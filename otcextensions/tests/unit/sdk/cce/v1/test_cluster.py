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

from otcextensions.sdk.cce.v1 import cluster as _cluster

OS_HEADERS = {
    'Content-Type': 'application/json',
}

EXAMPLE_LIST = [{
    'kind': 'cluster',
    'apiVersion': 'v1',
    'metadata': {
        'name': 'ag-test',
        'uuid': '5a66a449-668c-492f-8c33-5cdbdeaadd2e',
        'spaceuuid': 'de213bc4-4949-2a70-1a28-ae6c54e4ea23',
        'createAt': '2018-04-03 12:27:23.903327651 +0000 UTC',
        'updateAt': '2018-04-03 13:38:11.018224077 +0000 UTC'},
    'spec': {
        'description': 'some description',
        'hostList': {
            'kind': 'list',
            'apiVersion': 'v1',
            'metadata': {},
            'spec': {
                'hostList': [{
                    'kind': 'host',
                    'apiVersion': 'v1',
                    'metadata': {
                        'name': 'ag-test-node-1',
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
        },
        'az': 'eu-de-01',
        'cpu': 1,
        'memory': 4096,
        'vpc': 'ag-vpc-636e',
        'vpcid': '4056b8b9-ff86-4cc0-8442-c75eba1034de',
        'subnet': 'ag-subnet-636e',
        'cidr': '192.168.0.0/24',
        'clustertype': 'Single',
        'latestversion': {
            'version': 'V1.2.0',
            'date': '2017-10-28 02:58:43.052591366 +0000 UTC',
            'detail': 'k8s-v1.7.3'},
        'security_group_id': '',
        'versioninfo': {
            'version': 'V1.2.0',
            'date': '2017-10-28 02:58:43.052591366 +0000 UTC',
            'detail': 'k8s-v1.7.3'
        }
    },
    'clusterStatus': {'status': 'DEPLOYING'},
    'k8s_version': '1.7.3',
    'commit_id': '2c2fe6e8278a5db2d15a013987b53968c743f2a1'}
]


class TestCluster(base.TestCase):

    def setUp(self):
        super(TestCluster, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.put = mock.Mock()

        self.sot = _cluster.Cluster()

    def test_basic(self):
        sot = _cluster.Cluster()
        self.assertEqual('', sot.resource_key)
        self.assertEqual('', sot.resources_key)
        self.assertEqual('/clusters',
                         sot.base_path)
        self.assertEqual('cce', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        obj = EXAMPLE_LIST[0]
        sot = _cluster.Cluster.existing(**obj)
        self.assertEqual(obj['metadata']['uuid'], sot.id)
        self.assertEqual(obj['kind'], sot.kind)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST)

        self.sess.get.return_value = mock_response

        result = list(
            self.sot.list(
                self.sess,
            )
        )

        self.sess.get.assert_called_once_with(
            '/clusters',
            params={},
            headers=OS_HEADERS
        )

        expected_list = [
            _cluster.Cluster.existing(**EXAMPLE_LIST[0]),
        ]

        self.assertEqual(expected_list, result)

    def test_get(self):
        sot = _cluster.Cluster.existing(id=EXAMPLE_LIST[0]['metadata']['uuid'])

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST[0])

        self.sess.get.return_value = mock_response

        result = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            'clusters/%s' % EXAMPLE_LIST[0]['metadata']['uuid'],
            headers=OS_HEADERS
        )

        self.assertDictEqual(
            _cluster.Cluster.existing(**EXAMPLE_LIST[0]).to_dict(),
            result.to_dict())

    def test_create(self):
        cluster = {
            'metadata': {
                'name': 'test',
            },
            'spec': {
                'description': 'descr',
                'vpc': 'vpc-id',
                'subnet': 'subnet-id',
                'region': 'regio',
                'security_group_id': 'sg_id',
                'clustertype': 'Single'
            }
        }
        sot = _cluster.Cluster.new(**cluster)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST[0])

        self.sess.post.return_value = mock_response

        result = sot.create(self.sess, prepend_key=False)

        call_args = self.sess.post.call_args_list[0]

        expected_json = copy.deepcopy(cluster)
        expected_json['kind'] = 'cluster'
        expected_json['apiVersion'] = 'v1'

        self.assertEqual('/clusters', call_args[0][0])
        self.assertDictEqual(expected_json, call_args[1]['json'])

        self.sess.post.assert_called_once()

        self.assertDictEqual(
            result.to_dict(),
            _cluster.Cluster.existing(**EXAMPLE_LIST[0]).to_dict())

    def test_create_name_normalize(self):
        """Ensure name passed in the root is properly mapped into metadata
        """
        cluster = {
            'name': 'test',
            'spec': {
                'description': 'descr',
                'vpc': 'vpc-id',
                'subnet': 'subnet-id',
                'region': 'regio',
                'security_group_id': 'sg_id',
                'clustertype': 'Single'
            }
        }
        sot = _cluster.Cluster.new(**cluster)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST[0])

        self.sess.post.return_value = mock_response

        sot.create(self.sess, prepend_key=False)

        call_args = self.sess.post.call_args_list[0]

        expected_json = copy.deepcopy(cluster)
        expected_json['kind'] = 'cluster'
        expected_json['apiVersion'] = 'v1'
        expected_json['metadata'] = {'name': 'test'}
        expected_json.pop('name')

        self.assertEqual('/clusters', call_args[0][0])
        self.assertDictEqual(expected_json, call_args[1]['json'])

        self.sess.post.assert_called_once()

    def test_update(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST[0])

        self.sess.put.return_value = mock_response

        sot = _cluster.Cluster.existing(**EXAMPLE_LIST[0])

        sot._update(**{'spec': {
            'publicip_id': 'some_ip',
            'description': 'descr'}})

        sot.update(self.sess, prepend_key=False)

        call_args = self.sess.put.call_args_list[0]

        self.assertEqual('clusters/' + sot.id, call_args[0][0])
        self.assertDictEqual(
            {'spec': {'publicip_id': 'some_ip', 'description': 'descr'}},
            call_args[1]['json'])

        self.sess.put.assert_called_once()

    def test_delete(self):
        sot = _cluster.Cluster.existing(id=EXAMPLE_LIST[0]['metadata']['uuid'])

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = None

        self.sess.delete.return_value = mock_response

        sot.delete(self.sess)

        self.sess.delete.assert_called_once_with(
            'clusters/%s' % sot.id,
            headers=OS_HEADERS)

    def test_delete_nodes(self):
        sot = _cluster.Cluster.existing(id=EXAMPLE_LIST[0]['metadata']['uuid'])

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = None

        self.sess.delete.return_value = mock_response

        sot.delete_nodes(self.sess, ['n1', 'n2'])

        self.sess.delete.assert_called_once_with(
            'clusters/%s/hosts' % sot.id,
            json={
                'hosts': [
                    {'name': 'n1'},
                    {'name': 'n2'},
                ]
            },
            headers=OS_HEADERS
        )

        self.sess.delete.reset_mock()
        sot.delete_nodes(self.sess, 'n3')

        self.sess.delete.assert_called_once_with(
            'clusters/%s/hosts' % sot.id,
            json={
                'hosts': [
                    {'name': 'n3'},
                ]
            },
            headers=OS_HEADERS
        )
