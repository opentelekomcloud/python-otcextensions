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
Confirm Messages
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

queue_name_or_id = '05da4695-f9f7-492c-8074-c71bc7245f18'
queue = conn.dms.find_queue(name_or_id=queue_name_or_id)
group_name_or_id = 'g-70ebb4ba-3cc3-456c-89fc-968a5f7a8ff1'
group = conn.dms.find_group(queue, name_or_id=group_name_or_id)


attrs = {
    'queue': queue,  # Required; Queue-instance
    'group': group,  # Required; Group-instance
    'messages': [
        {
            'handler': 'handler_id',  # Required
            'status': 'success'  # Required
        }
    ]
}
for raw in conn.dms.ack_message(**attrs):
    print(raw)
