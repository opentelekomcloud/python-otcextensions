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

from openstack.tests.unit import base

from otcextensions.sdk.dds.v3 import eip

EXAMPLE = {
    "job_id": "3711e2ad-5787-49bc-a47f-3f0b066af9f5",
    "node_id": "52a4c096bb1f455d8d866956a959519eno02",
    "node_name": "mongodb-8977_mongos_node_1",
    "public_ip": "10.145.51.128",
    "public_ip_id": "45da4782-e0c8-4aa4-a290-b8740014f710"
}


class TestEip(base.TestCase):
    def test_basic(self):
        sot = eip.Eip()
        path = '/nodes'
        self.assertEqual(path, sot.base_path)

    def test_make_it(self):
        sot = eip.Eip(**EXAMPLE)
        self.assertEqual(EXAMPLE['job_id'], sot.job_id)
        self.assertEqual(EXAMPLE['node_id'], sot.node_id)
        self.assertEqual(EXAMPLE['node_name'], sot.node_name)
        self.assertEqual(EXAMPLE['public_ip'], sot.public_ip)
        self.assertEqual(EXAMPLE['public_ip_id'], sot.public_ip_id)
