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
Create Auto-Scaling Policy.
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    "scaling_group_id": "as_group_id",
    "scaling_policy_name": "as_policy_name",
    "scaling_policy_type": "ALARM",
    "alarm_id": "cloudeye_alarm_id",
    "scheduled_policy": {},
    "cool_down_time": 300,
    "scaling_policy_action": {
        "operation": "ADD",
        "instance_number": 1
    }
}

policy = conn.auto_scaling.create_policy(**attrs)
print(policy)
