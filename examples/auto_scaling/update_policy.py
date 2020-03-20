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
Update Auto-Scaling Policy by using id or an instance of class Policy.
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


policy = "policy_name_or_id"
attrs = {
    "scaling_policy_type": "RECURRENCE",
    "scaling_policy_name": "policy_01",
    "scheduled_policy": {
        "launch_time": "16:00",
        "recurrence_type": "Daily",
        "end_time": "2016-02-08T17:31Z",
        "start_time": "2016-01-08T17:31Z"
    },
    "scaling_policy_action": {
        "operation": "SET",
        "instance_number": 2
    }
}

policy = conn.auto_scaling.find_policy(policy)
conn.auto_scaling.update_policy(policy, **attrs)
