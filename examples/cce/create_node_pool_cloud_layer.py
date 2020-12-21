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
Create CCE Node Pool via OpenStack cloud layer
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


pool = conn.create_cce_node_pool(
    autoscaling_enabled=False,
    availability_zone='random',
    billing_mode=0,
    cluster='bca73490-394c-11eb-8fe2-0255ac101695',
    count=0,
    flavor='s2.large.2',
    initial_node_count=0,
    k8s_tags={
        "muh": "kuh"},
    ssh_key='tischrei-pub',
    name='test-node-pool3',
    os='CentOS 7.7',
    root_volume_size=40,
    root_volume_type='SATA',
    subnet_id='25d24fc8-d019-4a34-9fff-0a09fde6a9cb',
    tags=[
        {
            'key': 'hellokey1',
            'value': 'hellovalue1'
        }, {
            'key': 'hellokey2',
            'value': 'hellovalue2'
        }],
    wait=False)
print(pool)
