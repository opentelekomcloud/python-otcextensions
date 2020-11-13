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
Create a DNS zone
"""
import openstack
from otcextensions.sdk.dns.v2.zone import Router

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


zone = conn.dns.create_zone(
    name='private-zone',
    description='My private Zone',
    zone_type='private',
    ttl=300,
    email='zone-admin@example.com',
    router=Router(router_id='vpc_id',
                  router_region='eu-de'
                  )
)
print(zone)

'''
attrs = {
    "name": "private-zone.",
    "description": "My private Zone",
    "zone_type": "private",
    "email": "zone-admin@example.com",
    "router": {
        "router_id": "vpc_id",
        "router_region": "eu-de"
    }
}

zone = conn.dns.create_zone(**attrs)
print(zone)
'''
