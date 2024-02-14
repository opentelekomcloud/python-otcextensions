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
#
"""Create a visualization job from attributes."""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")

attrs = {
    "job_name": "visualization-job",
    "job_desc": "this is a visualization job",
    "train_url": "/obs/name/",
    "job_type": "mindinsight",
    "schedule": [
        {
            "type": "stop",
            "time_unit": "HOURS",
            "duration": 1,
        }
    ],
}

visjob = conn.modelartsv1.create_visualizationjob(**attrs)
print(visjob)
