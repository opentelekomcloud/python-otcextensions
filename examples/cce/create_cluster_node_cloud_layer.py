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
Create CCE Cluster node
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


node = conn.create_cce_cluster_node(
    annotations={'annotation1': 'abc'},
    availability_zone='eu-de-01',
    cluster='d9b37539-c927-11eb-bc4e-0255ac101123',
    count=1,
    flavor='s2.large.2',
    k8s_tags={
        "muh": "kuh"},
    ssh_key='keypair-pub',
    labels={'foo': 'bar'},
    max_pods=16,
    name='node2',
    network='25d24fc8-d019-4a34-9fff-0a09fde6a123',
    offload_node=False,
    os='CentOS 7.7',
    root_volume_size=40,
    root_volume_type='SATA',
    tags=[
        {
            'key': 'hellokey1',
            'value': 'hellovalue1'
        }, {
            'key': 'hellokey2',
            'value': 'hellovalue2'
        }],
    data_volumes=[{
        'volumetype': 'SATA',
        'size': 110,
        'encrypted': False,
        'cmk_id': ''
    }, {
        'volumetype': 'SAS',
        'size': 120,
        'encrypted': False,
        'cmk_id': ''
    }],
    wait=False)
print(node)
