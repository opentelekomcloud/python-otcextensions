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
import copy

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.cce.v3 import cluster_node

EXAMPLE_LIST = {
    "kind": "List",
    "apiVersion": "v3",
    "items": [
        {
            "kind": "Node",
            "apiVersion": "v3",
            "metadata": {
                "name": "node-demo",
                "uid": "c33b6898-38c9-11e9-b246-0255ac101413",
                "creationTimestamp": "2019-02-25 06:19:05.789461541 +0000 UTC",
                "updateTimestamp": "2019-02-25 06:19:05.789462592 +0000 UTC",
                "annotations": {
                    "kubernetes.io/node-pool.id":
                        "eu-de-02#s2.large.1#EulerOS 2.2"
                }
            },
            "spec": {
                "flavor": "s2.large.1",
                "az": "eu-de-02",
                "os": "EulerOS 2.2",
                "login": {
                    "sshKey": "KeyPair-demo",
                },
                "rootVolume": {
                    "volumetype": "SATA",
                    "size": 40
                },
                "dataVolumes": [
                    {
                        "volumetype": "SATA",
                        "size": 100
                    }
                ],
                "publicIP": {
                    "eip": {
                        "bandwidth": {}
                    }
                },
                "billingMode": 0
            },
            "status": {
                "phase": "Active",
                "serverId": "99de97f0-a10a-4215-ace7-817de0136ff5",
                "privateIP": "192.168.0.218",
                "publicIP": "10.154.50.127"
            }
        }
    ]
}

EXAMPLE_CREATE = {
    "kind": "Node",
    "apiVersion": "v3",
    "metadata": {
        "name": "mycluster-demo",
        "labels": {
            "foo": "bar"
        },
        "annotations": {
            "annotation1": "abc"
        }
    },
    "spec": {
        "flavor": "s1.large",
        "az": "eu-de",
        "login": {
            "sshKey": "KeyPair-demo"
        },
        "rootVolume": {
            "size": 40,
            "volumetype": "SATA"
        },
        "dataVolumes": [
            {
                "size": 100,
                "volumetype": "SATA"
            }
        ],
        "publicIP": {
            "count": 1,
            "eip": {
                "type": "5_bgp",
                "bandwidth": {
                    "chargemode": "traffic",
                    "size": 10,
                    "sharetype": "PER"
                }
            }
        },
        "count": 1
    }
}


class TestClusterNode(base.TestCase):

    def setUp(self):
        super(TestClusterNode, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)

        self.sot = cluster_node.ClusterNode(cluster_id='cluster_id')

    def test_basic(self):
        sot = cluster_node.ClusterNode()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)
        self.assertEqual('/clusters/%(cluster_id)s/nodes',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        obj = EXAMPLE_LIST['items'][0]
        sot = cluster_node.ClusterNode.existing(**obj)
        self.assertEqual(obj['metadata']['uid'], sot.id)
        self.assertEqual(obj['kind'], sot.kind)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST)

        self.sess.get.return_value = mock_response

        result = list(
            self.sot.list(
                self.sess,
                cluster_id='cluster_id',
            )
        )

        self.sess.get.assert_called_once_with(
            '/clusters/%s/nodes' % self.sot.cluster_id,
            params={},
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        expected_list = [
            cluster_node.ClusterNode.existing(
                **EXAMPLE_LIST['items'][0]),
        ]

        self.assertEqual(
            set(i.id for i in expected_list),
            set(i.id for i in result))
