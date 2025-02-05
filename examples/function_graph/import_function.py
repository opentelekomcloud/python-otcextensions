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
Import a function
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

attrs = {
    'func_name': 'test',
    'file_type': 'zip',
    'file_name': 'test.zip',
    'file_code': 'UEsDBBQAAAAIAPBbPFpOs3AMAgEAAEwCAAAGAAAAZGVwLnB5jVHB'
                 'asMwDL37K4R3iSGMMtglsNNW2HH0B4oXq9SjtY2shJbSf5/tpl5y'
                 'GFQX23qS3nuWPQZPDD/ROyGEwR3stTMHpAZHdNxC7x3jiVUnIAXT'
                 '+XbJ8QRfmiIC7xGsCwND6YHGaNaqlhVom3PwVoieD16beCNQYj6O'
                 'bGrP4wL50Ro0kNtqRch4IzfYox0nsJPtjGExboM8kAMNhDF4F7Fi'
                 '90QSdKnJHDKy5iG+e4Oyg5fVql3C396cE7CTH9kOTUI6uPxJuMra'
                 'cp0RFinFvRmOITZ3CZNiPPUYGNblsD6pjoDzr/4sawEk8hRrvjy3'
                 'D9p5/d/OOs9JNiKnxasHLSzJlfgFUEsBAhQDFAAAAAgA8Fs8Wk6z'
                 'cAwCAQAATAIAAAYAAAAAAAAAAAAAAKSBAAAAAGRlcC5weVBLBQYA'
                 'AAAAAQABADQAAAAmAQAAAAA='
}
func = conn.functiongraph.import_function(**attrs)
print(func)
