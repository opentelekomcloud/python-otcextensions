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
Update CBR policy with attributes
'''
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    'enabled': True,
    'name': 'policy001',
    'operation_definition': {
        'day_backups': 0,
        'month_backups': 0,
        'max_backups': 1,
        'timezone': 'UTC+08:00',
        'week_backups': 0,
        'year_backups': 0
    },
    'trigger': {
        'properties': {
            'pattern': [
                'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=14;BYMINUTE=00'
            ]
        }
    }
}

policy = 'name_or_id'
policy = conn.cbr.find_policy(name_or_id=policy)
policy = conn.cbr.update_policy(policy=policy, **attrs)
print(policy)
