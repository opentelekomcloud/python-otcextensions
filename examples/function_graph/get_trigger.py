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
Get function trigger
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

func_attrs = {
    'func_name': 'test-function',
    'package': 'default',
    'runtime': 'Python3.9',
    'handler': 'index.handler',
    'timeout': 30,
    'memory_size': 128,
    'code_type': 'inline',
}
fg = conn.functiongraph.create_function(**func_attrs)
trigger_attrs = {
    "trigger_type_code": "TIMER",
    "trigger_status": "ACTIVE",
    "event_data": {
        "name": "Timer-l8v2",
        "schedule": "3m",
        "schedule_type": "Rate"
    }
}

trigger = conn.functiongraph.create_trigger(
    fg, **trigger_attrs
)
tr = conn.functiongraph.get_trigger(
    fg.func_urn,
    trigger_attrs["trigger_type_code"],
    trigger.trigger_id)
print(tr)
