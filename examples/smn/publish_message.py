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
Publish Message via SMN
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    'subject': 'my_message_subject',
    'message_structure': '{"default":"test v2 default", "email":"abc"}',
    'message_template_name': 'template_name',
    'message': 'my_message',
    'endpoint': '+49123123456789',
    'time_to_live': '3600'
}
response = conn.smn.publish_message(**attrs)
print(response)
