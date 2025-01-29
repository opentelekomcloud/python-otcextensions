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
Get all dependency versions
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

u = 'https://fg-test-files.obs.eu-de.otc.t-systems.com/dependency.zip'
attrs = {
    'depend_link': u,
    'depend_type': 'obs',
    'runtime': 'Python3.10',
    'name': 'test-dep-1'
}
d = conn.functiongraph.create_dependency_version(**attrs)
for dv in conn.functiongraph.dependency_versions(d):
    print(dv)
