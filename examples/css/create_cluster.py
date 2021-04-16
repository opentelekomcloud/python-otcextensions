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
'''
Create CSS cluster
'''
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    'name': 'ES-Test',
    'instanceNum': 4,
    'instance': {
        'flavorRef': 'css.large.8',
        'volume': {
            'volume_type': 'COMMON',
            'size': 100
        },
        'nics': {
            'vpcId': 'vpc_id',
            'netId': 'network_id',
            'securityGroupId': 'security_group_id'
        }
    },
    'httpsEnable': 'false',
    'diskEncryption': {
        'systemEncrypted': '1',
        'systemCmkid': 'KMS_key_id'
    }
}
result = conn.css.create_cluster(**attrs)
print(result)
