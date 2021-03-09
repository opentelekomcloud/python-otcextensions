#!/usr/bin/env python3
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
'''
Create CCE Cluster node
'''
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    'kind': 'Node',
    'apiVersion': 'v3',
    'metadata': {
        'name': 'myhost',
        'labels': {
            'foo': 'bar'
        },
        'annotations': {
            'annotation1': 'abc'
        }
    },
    'spec': {
        'flavor': 's2.large.2',
        'az': 'eu-de-02',
        'login': {
            'sshKey': 'keypair-pub'
        },
        'rootVolume': {
            'size': 40,
            'volumetype': 'SATA'
        },
        'dataVolumes': [
            {
                'size': 100,
                'volumetype': 'SATA'
            }
        ],
        'userTags': [
            {
                'key': 'tag1',
                'value': 'aaaa'
            },
            {
                'key': 'tag2',
                'value': 'bbbb'
            }
        ],
        'k8sTags': {
            'label-test': 'test'
        },
        'publicIP': {
            # ids: ['1234', '5678']
            'count': 2,
            'eip': {
                'iptype': '5_bgp',
                'bandwidth': {
                    'chargemode': 'traffic',
                    'size': 10,
                    'sharetype': 'PER'
                }
            }
        },
        'count': 2,
        'nodeNicSpec': {
            'primaryNic': {
                'subnetId': 'bbfc0a20-d66c-4f36-b4c1-265d669b8c62'
            }
        },
    }
}

cluster = 'name_or_id'
cluster = conn.cce.find_cluster(name_or_id=cluster)
conn.cce.create_cluster_node(cluster=cluster, **attrs)
