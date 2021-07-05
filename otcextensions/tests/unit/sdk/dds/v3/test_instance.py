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

from otcextensions.sdk.dds.v3 import instance

EXAMPLE = {
    "name": "test-cluster-01",
    "datastore": {
        "type": "DDS-Community",
        "version": "3.4",
        "storage_engine": "wiredTiger"
    },
    "region": "aaa",
    "availability_zone": "bbb",
    "vpc_id": "674e9b42-cd8d-4d25-a2e6-5abcc565b961",
    "subnet_id": "f1df08c5-71d1-406a-aff0-de435a51007b",
    "security_group_id": "7aa51dbf-5b63-40db-9724-dad3c4828b58",
    "password": "Test@123",
    "mode": "Sharding",
    "flavor": [
        {
            "type": "mongos",
            "num": 2,
            "spec_code": "dds.mongodb.s2.medium.4.mongos"
        },
        {
            "type": "shard",
            "num": 2,
            "storage": "ULTRAHIGH",
            "size": 20,
            "spec_code": "dds.mongodb.s2.medium.4.shard"
        },
        {
            "type": "config",
            "num": 1,
            "storage": "ULTRAHIGH",
            "size": 20,
            "spec_code": "dds.mongodb.s2.large.2.config"
        }
    ],
    "backup_strategy": {
        "start_time": "08:15-09:15",
        "keep_days": "8"
    },
    "ssl_option": "1"
}


class TestFlavor(base.TestCase):

    def test_basic(self):
        sot = instance.Instance()

        self.assertEqual('/instances', sot.base_path)
        self.assertEqual('instances', sot.resources_key)
        self.assertEqual('instance', sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)
        self.assertDictEqual({
            'id': 'id',
            'name': 'name',
            'mode': 'mode',
            'marker': 'marker',
            'datastore_type': 'datastore_type',
            'vpc_id': 'vpc_id',
            'subnet_id': 'subnet_id',
            'limit': 'limit',
            'offset': 'offset'},
            sot._query_mapping._mapping)

    def test_make_it(self):
        sot = instance.Instance(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['flavor'], sot.flavor)
        self.assertEqual(EXAMPLE['subnet_id'], sot.subnet_id)
        self.assertEqual(EXAMPLE['security_group_id'], sot.security_group_id)
