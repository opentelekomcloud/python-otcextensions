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
'''
Bind resources to CBR vault
'''
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


vault = 'vault_name_or_id'
resources = [{
    'id': 'server_id',
    'type': 'OS::Nova::Server',
    # optional params
    # 'extra_info': {
    #     'include_volumes': [
    #         {
    #             'id': 'volume_id'
    #         },
    #         {
    #             'id': 'volume_id'
    #         },
    #     ],
    #     'exclude_volumes': [
    #         'vol1_id',
    #         'vol2_id'
    #     ]
    # },
}]

# For a disk vault
# resources = {
#   'id': 'volume_id',
#    'type': 'OS::Cinder::Volume',
# }]

vault = conn.cbr.find_vault(vault)
conn.cbr.associate_resources(vault=vault.id, resources=resources)
