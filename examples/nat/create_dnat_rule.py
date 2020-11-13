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
Create a DNAT Rule
"""
import openstack


openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

nat_gateway_id = 'nat_gateway_id'
port_id = 'network_id'
private_ip = '192.168.199.3'
floating_ip_id = 'floating_ip_id'
protocol = 'TCP'
internal_service_port = 80
external_service_port = 80


attrs = {
    "nat_gateway_id": nat_gateway_id,
    "private_ip": private_ip,
    "port_id": port_id,
    "protocol": protocol,
    "internal_service_port": internal_service_port,
    "external_service_port": external_service_port,
    "floating_ip_id": floating_ip_id
}

dnat_rule = conn.nat.create_dnat_rule(**attrs)
print(dnat_rule)
