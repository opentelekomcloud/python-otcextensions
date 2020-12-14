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
"""
Create CCE node pool
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    'metadata': {
        'name': 'test-node-pool'
    },
    'spec': {
        'initialNodeCount': 0,
        'type': 'vm',
        'autoscaling': {
            'enable': True,
            'minNodeCount': 1,
            'maxNodeCount': 3,
            'scaleDownCooldownTime': 10,
            'priority': 1
        },
        'nodeTemplate': {
            'flavor': 's2.large.2',
            'az': 'eu-de-01',
            'os': 'CentOS 7.7',
            'login': {
                'sshKey': 'sshkey-pub'
            },
            'rootVolume': {
                'volumetype': 'SATA',
                'size': 40
            },
            'dataVolumes': [
                {
                    'volumetype': 'SATA',
                    'size': 100,
                    'extendParam': {
                        'useType': 'docker'
                    }
                }
            ],
            'billingMode': 0,
            'extendParam': {
                'maxPods': 110,
                'DockerLVMConfigOverride': 'dockerThinpool=vgpaas/90%VG;'
                                           'kubernetesLV=vgpaas/10%VG;'
                                           'diskType=evs;lvType=linear'
            },
            'k8sTags': {
                'tag1': 'value1',
                'tag2': 'value2'
            },
            'taints': [
                {
                    'key': 'aaa',
                    'value': 'bbb',
                    'effect': 'NoSchedule'
                },
                {
                    'key': 'ccc',
                    'value': 'ddd',
                    'effect': 'NoSchedule'
                }
            ],
            'userTags': [
                {
                    'key': 'resource-tag1',
                    'value': 'value1'
                },
                {
                    'key': 'resource-tag2',
                    'value': 'value2'
                }
            ],
            'nodeNicSpec': {
                'primaryNic': {
                    'subnetId': 'subnet_id'
                }
            }
        }
    }
}
cluster = 'name_or_id'
cluster = conn.cce.find_cluster(name_or_id=cluster)
conn.cce.create_node_pool(cluster=cluster, **attrs)
