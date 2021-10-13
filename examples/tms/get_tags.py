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
Query Tags
"""
import openstack
from otcextensions import sdk

# openstack.enable_logging()
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

tag_id = "test"
attrs = {
    "key": "test",
    "value": "test",
    "limit": "1",
    "marker": "marker",
    "order_field": "key",
    "order_method": "asc",
}


tags = conn.tms.query_predefine_tag(**attrs)
print(tags)