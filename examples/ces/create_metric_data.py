#!/usr/bin/env python3
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
'''
Add CloudEye metric data
'''
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

# not working due to lag of compatible API: list instead of proper JSON
attrs = [
	{
		"metric": {
			"namespace": "MINE.APP",
			"dimensions": [
				{
					"name": "instance_id",
					"value": "33328f02-3814-422e-b688-bfdba93d4050"
				}
			],
			"metric_name": "cpu_util"
		},
		"ttl": 172800,
		"collect_time": 1598266684000,
		"type": "int",
		"value": 60,
		"unit": "%"
	},
	{
		"metric": {
			"namespace": "MINE.APP",
			"dimensions": [
				{
					"name": "instance_id",
					"value": "33328f02-3814-422e-b688-bfdba93d4050"
				}
			],
			"metric_name": "cpu_util"
		},
		"ttl": 172800,
		"collect_time": 1598266685000,
		"type": "int",
		"value": 70,
		"unit": "%"
	}
]


data = conn.ces.create_metric_data(**attrs)
print(data)
