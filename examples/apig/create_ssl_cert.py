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
Create SSL certificate
"""
import openstack
from pathlib import Path

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
attrs = {
    "name": "cert_demo",
    "cert_content": Path("/mnt/c/Users/sand1/fullchain.pem")
    .read_text().replace('\r\n', '\n'),
    "private_key": Path("/mnt/c/Users/sand1/privkey.pem")
    .read_text().replace('\r\n', '\n'),
    "type": "instance",
    "instance_id": "gateway_id"
}
cert = conn.apig.create_ssl_certificate(**attrs)
