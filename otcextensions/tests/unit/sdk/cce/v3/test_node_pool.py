#!/usr/bin/env python3
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

from otcextensions.sdk.cce.v3 import node_pool

EXAMPLE_LIST = {
    "kind": "List",
    "apiVersion": "v3",
    "items": [
        {
            "kind": "NodePool",
            "apiVersion": "v3",
            "metadata": {
                "name": "wyr-17-nodepool-53042",
                "uid": "feec6013-cd7e-11ea-8c7a-0255ac100be7"
            },
            "spec": {
                "initialNodeCount": 0,
                "type": "vm",
                "nodeTemplate": {
                    "flavor": "s6.large.2",
                    "az": "eu-de-01",
                    "os": "EulerOS 2.5",
                    "login": {
                        "sshKey": "KeyPair-nodepool",
                        "userPassword": {}
                    },
                    "rootVolume": {
                        "volumetype": "SATA",
                        "size": 40
                    },
                    "dataVolumes": [
                        {
                            "volumetype": "SATA",
                            "size": 100,
                            "extendParam": {
                                "useType": "docker"
                            }
                        }
                    ],
                    "publicIP": {
                        "eip": {
                            "bandwidth": {}
                        }
                    },
                    "nodeNicSpec": {
                        "primaryNic": {
                            "subnetId": "31be174a-0c7f-4b71-bb0d"
                        }
                    },
                    "billingMode": 0,
                    "taints": [
                        {
                            "key": "aaa",
                            "value": "bbb",
                            "effect": "NoSchedule"
                        },
                        {
                            "key": "ccc",
                            "value": "ddd",
                            "effect": "NoSchedule"
                        }
                    ],
                    "k8sTags": {
                        "cce.cloud.com/cce-nodepool": "wyr-17-nodepool",
                        "tag1": "value1",
                        "tag2": "value2"
                    },
                    "userTags": [
                        {
                            "key": "resource-tag1",
                            "value": "value1"
                        },
                        {
                            "key": "resource-tag2",
                            "value": "value2"
                        }
                    ],
                    "extendParam": {
                        "DockerLVMConfigOverride": "dockerThinpool",
                        "alpha.cce/NodeImageID": "85bd7ec5",
                        "alpha.cce/postInstall": "bHMgLWwK",
                        "alpha.cce/preInstall": "bHMgLWw=",
                        "maxPods": 110,
                        "publicKey": "ssh-key"
                    }
                },
                "autoscaling": {
                    "enable": True,
                    "minNodeCount": 1,
                    "maxNodeCount": 3,
                    "scaleDownCooldownTime": 10,
                    "priority": 1
                },
                "nodeManagement": {
                    "serverGroupReference": "grpref"
                }
            },
            "status": {
                "currentNode": 0,
                "phase": ""
            }
        }
    ]
}

EXAMPLE_CREATE = {
    "kind": "NodePool",
    "apiVersion": "v3",
    "metadata": {
        "name": "wyr-17-nodepool-53042"
    },
    "spec": {
        "initialNodeCount": 0,
        "type": "vm",
        "autoscaling": {
            "enable": True,
            "minNodeCount": 1,
            "maxNodeCount": 3,
            "scaleDownCooldownTime": 10,
            "priority": 1
        },
        "nodeManagement": {
            "serverGroupReference": "grpref"
        },
        "nodeTemplate": {
            "flavor": "s6.large.2",
            "az": "eu-de-01",
            "os": "EulerOS 2.5",
            "login": {
                "sshKey": "KeyPair-nodepool"
            },
            "rootVolume": {
                "volumetype": "SATA",
                "size": 40
            },
            "dataVolumes": [
                {
                    "volumetype": "SATA",
                    "size": 100,
                    "extendParam": {
                        "useType": "docker"
                    }
                }
            ],
            "billingMode": 0,
            "extendParam": {
                "alpha.cce/preInstall": "bHMgLWw=",
                "alpha.cce/postInstall": "bHMgLWwK",
                "alpha.cce/NodeImageID": "85bd7ec5",
                "maxPods": 110,
                "DockerLVMConfigOverride": "dockerThinpool"
            },
            "k8sTags": {
                "tag1": "value1",
                "tag2": "value2"
            },
            "taints": [
                {
                    "key": "aaa",
                    "value": "bbb",
                    "effect": "NoSchedule"
                },
                {
                    "key": "ccc",
                    "value": "ddd",
                    "effect": "NoSchedule"
                }
            ],
            "userTags": [
                {
                    "key": "resource-tag1",
                    "value": "value1"
                },
                {
                    "key": "resource-tag2",
                    "value": "value2"
                }
            ],
            "nodeNicSpec": {
                "primaryNic": {
                    "subnetId": "31be174a-0c7f-4b71-bb0d"
                }
            }
        }
    }
}


class TestNodePool(base.TestCase):

    def setUp(self):
        super(TestNodePool, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)

        self.sot = node_pool.NodePool(cluster_id='cluster_id')

    def test_basic(self):
        sot = node_pool.NodePool()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)
        self.assertEqual('/clusters/%(cluster_id)s/nodepools',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        obj = EXAMPLE_LIST['items'][0]
        sot = node_pool.NodePool.existing(**obj)
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
            '/clusters/%s/nodepools' % self.sot.cluster_id,
            params={},
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        expected_list = [
            node_pool.NodePool.existing(
                **EXAMPLE_LIST['items'][0]),
        ]

        self.assertEqual(
            set(i.id for i in expected_list),
            set(i.id for i in result))
