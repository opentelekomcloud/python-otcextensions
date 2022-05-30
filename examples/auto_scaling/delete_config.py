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
Delete Auto-Scaling Configuration by id or instance of class Config
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


config_id = '1234567-ad7a-48ce-8f92-b55c651439d2'
conn.auto_scaling.delete_config(config_id)
