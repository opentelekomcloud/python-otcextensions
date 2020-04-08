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
Update CTS Tracker by using id or an instance of class Tracker
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


tracker = "system"
attrs = attrs = {
    "bucket_name": "cloudtraceservice",
    "file_prefix_name": "newPrefix-",
    "lts": {
        "is_lts_enabled": True,
        "log_group_name": "CTS",
        "log_topic_name": "system-trace",
        "log_group_id": "1186622b-78ec-11ea-997c-286ed488c87f",
        "log_topic_id": "751f0409-78ec-11ea-90c7-286ed488c880"
    },
    "status": "enabled",
    "tracker_name": "system",
    "detail": ""
}

tracker = conn.cts.get_tracker(tracker)
conn.cts.update_tracker(tracker, **attrs)
