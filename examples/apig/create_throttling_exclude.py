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
Create an Excluded Request Throttling Configuration
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
attrs = {
    "api_call_limits": 100,
    "app_call_limits": 60,
    "enable_adaptive_control": "FALSE",
    "ip_call_limits": 60,
    "name": "throttle_demo",
    "remark": "Total: 800 calls/second;"
              " user: 500 calls/second;"
              " app: 300 calls/second;"
              " IP address: 600 calls/second",
    "time_interval": 1,
    "time_unit": "SECOND",
    "type": 1,
    "user_call_limits": 60
}
policy = conn.apig.create_throttling_policy(
    gateway="gateway_id",
    **attrs
)

ex_attrs = {
    "call_limits": 50,
    "object_id": "user_id",
    "object_type": "USER"
}

excluded = conn.apig.create_throttling_excluded_policy(
    gateway="gateway_id",
    policy=policy,
    **ex_attrs
)
