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
Create Distributed Cache Service Instance
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    "name": "dcs-test",
    "engine": "Redis",
    "capacity": 2,
    "resource_spec_code": "dcs.single_node",
    "engine_version": "3.0.7",
    "vpc_id": "26ca2783-dc40-4e3a-95b1-5a0756441e12",
    "vpc_name": "vpc-test",
    "product_id": "OTC_DCS_SINGLE",
    "password": "PASSWORD",
    "user_id": "18569c6d589c4be3a300b6401c74d936",
    "user_name": "iam_user",
    "maintain_begin": "02:00:00",
    "maintain_end": "06:00:00",
    "enable_publicip": False,
    "enable_ssl": False,
    "service_upgrade": False,
    "service_task_id": "",
    "available_zones": [
        "eu-de-03"
    ],
    "subnet_id": "25d24fc8-d019-4a34-9fff-0a09fde6a9cb",
    "security_group_id": "bb0e60ab-b6e0-4c61-a503-63213c18effa"
}

instance = conn.dcs.create_instance(**attrs)
print(instance)
