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
Authorize Apps
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    "env_id": "DEFAULT_ENVIRONMENT_RELEASE_ID",
    "app_ids": ["74593f5c94f64a139db38b61a7705df3"],
    "api_ids": ["64182cc7e77245ebbae8cf3b8522a540"]
}

result = conn.apig.create_auth_in_api(gateway="id",
                                      **attrs)
print(list(result))
