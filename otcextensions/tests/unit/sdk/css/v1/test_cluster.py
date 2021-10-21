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

from otcextensions.sdk.css.v1 import cluster


FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "datastore": {
        "type": "elasticsearch",
        "version": "6.2.3"
    },
    "instanceNum": 4,
    "instance": {
        "flavorRef": "css.large.8",
        "volume": {
            "volume_type": "COMMON",
            "size": 100
        },
        "nics": {
            "vpcId": "fccd753c-91c3-40e2-852f-5ddf76d1a1b2",
            "netId": "af1c65ae-c494-4e24-acd8-81d6b355c9f1",
            "securityGroupId": "7e3fed21-1a44-4101-ab29-34e57124f614"
        }
    },
    "instances": [{
        "status": "200",
        "type": "ess",
        "id": "3c7fe582-a9f6-46fd-9d01-956bed4a8bbc",
        "name": "ES-1-16-test17-ess-esn-1-1"
    }],
    "updated": "2018-01-16T08:37:18",
    "name": "ES-1-16-test17",
    "created": "2018-01-16T08:37:18",
    "id": FAKE_ID,
    "status": "200",
    "endpoint": "192.168.0.8:9200",
    "httpsEnable": False,
    "diskEncrypted": True,
    "diskEncryption": {
        "systemEncrypted": "1",
        "systemCmkid": "42546bb1-8025-4ad1-868f-600729c341ae"
    },
    "cmkId": "42546bb1-8025-4ad1-868f-600729c341ae",
    "vpcId": "07761987-bb61-4bbf-9d14-a7e6b6909224",
    "subnetId": "675ae21c-cc1c-4fc5-9cb4-4c07fce79648",
    "securityGroupId": "e9e098c8-2116-4b92-823c-036f0f17360b",
    "actionProgress": {},
    "actions": []
}


class TestCluster(base.TestCase):

    def setUp(self):
        super(TestCluster, self).setUp()

    def test_basic(self):
        sot = cluster.Cluster()

        self.assertEqual('/clusters', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)
        self.assertDictEqual({'id': 'id',
                              'start': 'start',
                              'limit': 'limit',
                              'marker': 'marker'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = cluster.Cluster(**EXAMPLE)
        updated_sot_attrs = (
            'cmkId',
            'datastore',
            'httpsEnable',
            'diskEncrypted',
            'diskEncryption',
            'instance',
            'instanceNum',
            'actionProgress',
            'vpcId',
            'subnetId',
            'securityGroupId',
            'instances',
            'updated',
            'created',
        )

        self.assertEqual(EXAMPLE['cmkId'], sot.cmk_id)
        self.assertEqual(EXAMPLE['datastore']['type'], sot.datastore.type)
        self.assertEqual(EXAMPLE['datastore']['version'],
                         sot.datastore.version)
        self.assertEqual(EXAMPLE['diskEncrypted'], sot.is_disk_encrypted)
        self.assertEqual(EXAMPLE['diskEncryption']['systemCmkid'],
                         sot.disk_encryption.cms_id)
        instance = sot.instance
        self.assertEqual(EXAMPLE['instance']['flavorRef'], instance.flavor)
        self.assertEqual(EXAMPLE['instance']['nics']['vpcId'],
                         instance.nics.router_id)
        self.assertEqual(EXAMPLE['instance']['nics']['netId'],
                         instance.nics.network_id)
        self.assertEqual(EXAMPLE['instance']['nics']['securityGroupId'],
                         instance.nics.security_group_id)
        self.assertEqual(EXAMPLE['instances'], sot.nodes)
        self.assertEqual(EXAMPLE['instanceNum'], sot.instance_count)
        self.assertEqual(EXAMPLE['httpsEnable'], sot.is_https_enabled)
        self.assertEqual(EXAMPLE['actionProgress'], sot.progress)
        self.assertEqual(EXAMPLE['vpcId'], sot.router_id)
        self.assertEqual(EXAMPLE['securityGroupId'], sot.security_group_id)
        self.assertEqual(EXAMPLE['subnetId'], sot.subnet_id)
        self.assertEqual(EXAMPLE['updated'], sot.updated_at)
        self.assertEqual(EXAMPLE['created'], sot.created_at)

        for key, value in EXAMPLE.items():
            if key in updated_sot_attrs:
                pass
            else:
                self.assertEqual(getattr(sot, key), value)
