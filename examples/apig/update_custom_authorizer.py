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
Update custom authorizer
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
attrs = {
    'name': 'custom_auth_test',
    'type': 'BACKEND',
    'authorizer_type': 'FUNC',
    'authorizer_uri': 'urn:fss:eu-de:7ed5f793b8354ea9b27a849f17af4733'
                      ':function:default:test_apig_authorizer:latest',
    'authorizer_version': '1',
    'ttl': 5,
    "identities": [{
        "name": "header",
        "location": "HEADER"
    }]
}
updated = conn.apig.update_custom_authorizer(gateway='gateway_id',
                                             custom_authorizer='authorizer_id',
                                             **attrs)
