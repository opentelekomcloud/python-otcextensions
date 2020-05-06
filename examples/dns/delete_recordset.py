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
Delete DNS recordset by id or class Recordset
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


zone = 'ff8080826ec87fdb0171a1b6e977666a'
recordset = 'ff8080826ec87fdb0171eaa952333c1a'
conn.dns.delete_recordset(zone=zone, recordset=recordset, ignore_missing=True)
