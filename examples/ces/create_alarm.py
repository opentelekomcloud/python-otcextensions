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
Create CloudEye alarm rule
'''
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    "alarm_name": "alarm-test", 
    "alarm_description": "Test Alarm", 
    "metric": {
        "namespace": "SYS.ECS", 
        "dimensions": [
            {
                "name": "instance_id", 
                "value": "33328f02-3814-422e-b688-bfdba93d4051"
            }
        ], 
        "metric_name": "network_outgoing"
    }, 
    "condition": {
        "period": 300, 
        "filter": "average", 
        "comparison_operator": ">=", 
        "value": 6, 
        "unit": "B/s", 
        "count": 1        
   }, 
    "alarm_enabled": True, 
    "alarm_action_enabled": True, 
    "alarm_level": 2, 
    "ok_actions": [
        {
            "type": "notification", 
            "notificationList": ["urn:smn:region:68438a86d98e427e907e0097b7e35d48:sd"]
        }
    ]
}




alarm = conn.ces.create_alarm(**attrs)
print(alarm)
