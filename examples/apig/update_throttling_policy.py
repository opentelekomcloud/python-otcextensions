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
Update throttling policy in gateway
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
attrs = {
    "time_unit": "SECOND",
    "name": "throttle_demo",
    "api_call_limits": 100,
    "time_interval": 1,
    "remark": "Total: 800 calls/second;"
              " user: 500 calls/second;"
              " app: 300 calls/second;"
              " IP address: 600 calls/second",
}
environment = conn.apig.update_throttling_policy(
    gateway="gateway_id",
    policy="policy_id",
    **attrs
)
