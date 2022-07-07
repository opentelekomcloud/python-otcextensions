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
'''
Update MRS Datasource
'''
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    "name": "my-data-source-update",
    "url": "/simple/mapreduce/input",
    "is_protected": False,
    "is_public": False,
    "type": "hdfs",
    "description": "this is the data source template"
}

datasource = 'ds1'
datasource = conn.mrs.find_datasource(name_or_id=datasource)
datasource = conn.mrs.update_datasource(datasource=datasource, **attrs)
print(datasource)
