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
Update a RDS configuration template
"""
import openstack


openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


values = {
    'max_connections': '11'
}
name_or_id = 'configuration_name_or_id'
configuration = conn.rds.find_configuration(name_or_id=name_or_id)
configuration = conn.rds.create_configuration(config=configuration,
                                              name='configuration_update',
                                              description='my new config',
                                              values=values)
print(configuration)
