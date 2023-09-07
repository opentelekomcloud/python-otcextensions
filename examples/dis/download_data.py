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
Downloading Data from DIS Stream.
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

partition_cursor = "eyJpdGVyR2VuVGltZSI6MTQ5MDk1MD.."
result = conn.dis.download_data(partition_cursor)
print(result)

# To download Data to a CSV File
filename = "my_data.csv"
conn.dis.download_data(partition_cursor, filename=filename)
