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
import mock

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.cce.v1 import cluster

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

        self.sot = cluster.Cluster()

    def test_basic(self):
        sot = cluster.Cluster()
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
        sot = cluster.Cluster.existing(**obj)
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
            params={}
        )

        expected_list = [
            cluster.Cluster.existing(**EXAMPLE_LIST[0]),
        ]

        self.assertEqual(expected_list, result)

    def test_get(self):
        sot = cluster.Cluster.existing(id=EXAMPLE_LIST[0]['metadata']['uuid'])

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST[0])

        self.sess.get.return_value = mock_response

        result = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            'clusters/%s' % EXAMPLE_LIST[0]['metadata']['uuid']
        )

        self.assertDictEqual(
            cluster.Cluster.existing(**EXAMPLE_LIST[0]).to_dict(),
            result.to_dict())

    def test_delete(self):
        sot = cluster.Cluster.existing(id=EXAMPLE_LIST[0]['metadata']['uuid'])

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = None

        self.sess.delete.return_value = mock_response

        sot.delete(self.sess)

        self.sess.delete.assert_called_once_with(
            'clusters/%s' % sot.id)
