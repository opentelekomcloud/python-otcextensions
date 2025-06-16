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
List API calls for a specified period
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
attrs = {
    'api_id': '64182cc7e77245ebbae8cf3b8522a540',
    'duration': '1h',
}
found = conn.apig.list_api_calls_for_period(gateway='gateway_id_here',
                                            **attrs)
