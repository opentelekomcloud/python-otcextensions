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
Delete CCE node pool in cloud layer
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


cluster = 'bca73490-394c-11eb-8fe2-0255ac101695'
pool = '58d24fde-4042-11eb-8fea-0255ac10169f'
conn.delete_cce_node_pool(
    cluster=cluster,
    node_pool=pool)
