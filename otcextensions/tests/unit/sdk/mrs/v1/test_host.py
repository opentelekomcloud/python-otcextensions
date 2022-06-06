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

from otcextensions.sdk.mrs.v1 import cluster

EXAMPLE = {
    "id": "063d1d47-ae91-4a48-840c-b3cfe4efbcf0",
    "name": "a78e161c-d14f-4b68-8c2d-0219920ce844_node_core_IQhiC",
    "ip": "192.168.0.169",
    "status": "ACTIVE",
    "flavor": "c2.2xlarge.linux.mrs",
    "type": "Core",
    "mem": "16384",
    "cpu": "8",
    "root_volume_size": "40",
    "data_volume_type": "SATA",
    "data_volume_size": 100,
    "data_volume_count": 1
}


class TestHost(base.TestCase):

    def test_basic(self):
        sot = cluster.Host()
        self.assertEqual('host', sot.resource_key)
        self.assertEqual('hosts', sot.resources_key)
        path = '/clusters/%(cluster_id)s/hosts'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_update)

    def test_make_it(self):
        sot = cluster.Host(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['ip'], sot.ip)
        self.assertEqual(EXAMPLE['mem'], sot.mem)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['flavor'], sot.flavor)
        self.assertEqual(EXAMPLE['cpu'], sot.cpu)
        self.assertEqual(EXAMPLE['data_volume_size'], sot.data_volume_size)
