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
Update security policy
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

attrs = {
    "name": "test-security-policy",
    "protocols": ["TLSv1.2", "TLSv1", "TLSv1.3"],
    "ciphers": ["ECDHE-ECDSA-AES128-SHA", "TLS_AES_128_GCM_SHA256"]
}

security_policy = conn.vlb.ipdate_security_policy(load_balancer="name")
print(security_policy)
