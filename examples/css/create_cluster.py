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
Create CSS Cluster
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc-test')
sdk.register_otc_extensions(conn)

attrs = {
    'name': 'ES-Test',
    'instanceNum': 1,
    'datastore': {
        'type': 'elasticsearch',
        'version': '7.6.2'
    },
    'instance': {
        'flavorRef': 'css.xlarge.2',
        'volume': {
            'volume_type': 'COMMON',
            'size': 100
        },

        'nics': {
            'vpcId': 'vpcId',
            'netId': 'netId',
            'securityGroupId': 'securityGroupId'
        }
    },
    'httpsEnable': 'false',
    'diskEncryption': {
        'systemEncrypted': '0',
    },
    'backupStrategy': {
        'period': "00:00 GMT+03:00",
        'prefix': 'backup',
        'keepday': 1,
        'bucket': 'css-test-0',
        'agency': 'test-css',
        'basePath': 'css'
    },
}
result = conn.css.create_cluster(**attrs)
print(result)
