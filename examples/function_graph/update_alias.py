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
Update alias
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

func_attrs = {
    'func_name': 'test-function',
    'package': 'default',
    'runtime': 'Python3.9',
    'handler': 'index.handler',
    'timeout': 30,
    'memory_size': 128,
    'code_type': 'inline',
}
fg = conn.functiongraph.create_function(**func_attrs)

alias_attrs = {
    'name': 'a1',
    'version': 'new-version'
}
alias = conn.functiongraph.create_alias(
    fg.func_urn, **alias_attrs
)

new_attrs = {
    'version': 'new-version',
    'description': 'new',
}
updated = conn.functiongraph.update_alias(
    fg, alias, **new_attrs)
