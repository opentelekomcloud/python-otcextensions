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
Stop a running Devenv Instance (Notebook).
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect()

instance_id = "DE-1369d64a-8eb6-11ee-9af2-0255c0a800ac"
response = conn.modelartsv1.stop_devenv_instance(instance_id)
print(response)
