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
Create CSS Cluster (opensearch)
"""

import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    'name': 'opensearch_test',
    'instanceNum': 3,
    'datastore': {
        'type': 'opensearch',
        'version': '1.3.6',
    },
    'instance': {
        'availability_zone': 'eu-de-01',
        'flavorRef': 'css.xlarge.2',
        'volume': {
            'volume_type': 'COMMON',
            'size': 100,
        },
        'nics': {
            'vpcId': 'VPC-ID',
            'netId': 'Network-ID',
            'securityGroupId': 'SecurityGroup-ID',
        },
    },
    'httpsEnable': 'false',
    'diskEncryption': {
        'systemEncrypted': '0',
    },
    'tags': [
        {'key': 'key0', 'value': 'value0'},
        {'key': 'key1', 'value': 'value1'},
    ],
    'backupStrategy': {
        'period': '00:00 GMT+01:00',
        'prefix': 'backup',
        'keepday': 1,
        'bucket': 'css-backup-1663481103064',
        'agency': 'test_agency',
        'basePath': 'css',
    },
}
result = conn.css.create_cluster(**attrs)
conn.css.wait_for_cluster(result)
cluster = conn.css.get_cluster(result)
print(cluster)
