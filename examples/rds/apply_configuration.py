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
Apply a RDS configuration to a several RDS instances
"""
import openstack


openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

configuration = '43f3a58705aa43bf9cfa4f06df80552epr01'
instance_list = [
    'instance_id1',
    'instance_id2'
]
response = conn.rds.apply_configuration(configuration=configuration,
                                        instances=instance_list)
print(response)
