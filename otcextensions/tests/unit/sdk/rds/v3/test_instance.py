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
import copy

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.rds.v3 import instance

# RDS requires those headers to be present in the request, to native API
# otherwise 404
RDS_HEADERS = {
    'Content-Type': 'application/json',
    'X-Language': 'en-us'
}

# RDS requires those headers to be present in the request, to OS-compat API
# otherwise 404
OS_HEADERS = {
    'Content-Type': 'application/json',
}

# PROJECT_ID = '123'
IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
      "flavor_ref": "rds.mysql.s1.large",
      "id": IDENTIFIER,
      "status": "ACTIVE",
      "name": "mysql-0820-022709-01",
      "port": 3306,
      "type": "Single",
      "region": "eu-de",
      "volume": {
          "type": "ULTRAHIGH",
          "size": 100
      },
      "datastore": {
          "type": "mysql",
          "version": "5.7"
      },
      "created": "2018-08-20T02:33:49+0800",
      "updated": "2018-08-20T02:33:50+0800",
      "nodes": [{
          "id": "06f1c2ad57604ae89e153e4d27f4e4b8no01",
          "name": "mysql-0820-022709-01_node0",
          "role": "master",
          "status": "ACTIVE",
          "availability_zone": "eu-de-01"
      }],
      "private_ips": ["192.168.0.142"],
      "public_ips": ["10.154.219.187", "10.154.219.186"],
      "db_user_name": "root",
      "vpc_id": "b21630c1-e7d3-450d-907d-39ef5f445ae7",
      "subnet_id": "45557a98-9e17-4600-8aec-999150bc4eef",
      "security_group_id": "38815c5c-482b-450a-80b6-0a301f2afd97",
      "switch_strategy": "",
      "backup_strategy": {
          "start_time": "19:00-20:00",
          "keep_days": 7
      },
      "maintenance_window": "02:00-06:00",
      "related_instance": [],
      "disk_encryption_id": "",
      "time_zone": ""
}

class TestInstance(base.TestCase):

    def setUp(self):
        super(TestInstance, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        # self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)
        self.sot = instance.Instance(**EXAMPLE)

    def test_basic(self):
        sot = instance.Instance()
        self.assertEqual('instance', sot.resource_key)
        self.assertEqual('instances', sot.resources_key)
        self.assertEqual('/instances', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = instance.Instance(**EXAMPLE)
        self.assertEqual(IDENTIFIER, sot.id)
        self.assertEqual(EXAMPLE['volume'], sot.volume)
        self.assertEqual(EXAMPLE['flavor_ref'], sot.flavor_ref)
        self.assertEqual(EXAMPLE['datastore'], sot.datastore)
        self.assertEqual(EXAMPLE['region'], sot.region)
        self.assertEqual(EXAMPLE['port'], sot.port)
        self.assertEqual(EXAMPLE['disk_encryption_id'], sot.disk_encryption_id)
        self.assertEqual(EXAMPLE['vpc_id'], sot.vpc_id)
        self.assertEqual(EXAMPLE['subnet_id'], sot.subnet_id)
        self.assertEqual(EXAMPLE['security_group_id'], sot.security_group_id)
        self.assertEqual(EXAMPLE['private_ips'], sot.private_ips)
        self.assertEqual(EXAMPLE['public_ips'], sot.public_ips)
        self.assertEqual(EXAMPLE['nodes'], sot.nodes)
        self.assertEqual(EXAMPLE['db_user_name'], sot.db_user_name)
        self.assertEqual(EXAMPLE['backup_strategy'], sot.backup_strategy)
        self.assertEqual(EXAMPLE['switch_strategy'], sot.switch_strategy)
        self.assertEqual(EXAMPLE['maintenance_window'], sot.maintenance_window)
        self.assertEqual(EXAMPLE['related_instance'], sot.related_instance)
        self.assertEqual(EXAMPLE['disk_encryption_id'], sot.disk_encryption_id)
        self.assertEqual(EXAMPLE['time_zone'], sot.time_zone)

    def test_list(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "instances": [{
                "id": IDENTIFIER,
                "status": "ACTIVE",
                "name": "mysql-0820-022709-01",
                "port": 3306,
                "type": "Single",
                "region": "eu-de",
                "datastore": {
                    "type": "mysql",
                    "version": "5.7"
                },
                "created": "2018-08-20T02:33:49+0800",
                "updated": "2018-08-20T02:33:50+0800",
                "volume": {
                    "type": "ULTRAHIGH",
                    "size": 100
                },
                "nodes": [{
                    "id": "06f1c2ad57604ae89e153e4d27f4e4b8no01",
                    "name": "mysql-0820-022709-01_node0",
                    "role": "master",
                    "status": "ACTIVE",
                    "availability_zone": "eu-de-01"
                }],
                "private_ips": ["192.168.0.142"],
                "public_ips": ["10.154.219.187", "10.154.219.186"],
                "db_user_name": "root",
                "vpc_id": "b21630c1-e7d3-450d-907d-39ef5f445ae7",
                "subnet_id": "45557a98-9e17-4600-8aec-999150bc4eef",
                "security_group_id": "38815c5c-482b-450a-80b6-0a301f2afd97",
                "flavor_ref": "rds.mysql.s1.large",
                "switch_strategy": "",
                "backup_strategy": {
                    "start_time": "19:00-20:00",
                    "keep_days": 7
                },
                "maintenance_window": "02:00-06:00",
                "related_instance": [],
                "disk_encryption_id": "",
                "time_zone": ""
            }], 
            "total_count": 1
        } 

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess))

        self.sess.get.assert_called_once_with(
            '/instances',
            params={},
        )

        self.assertEqual([instance.Instance(**EXAMPLE)], result)


#    def test_action_restore(self):
#        sot = instance.Instance(**EXAMPLE)
#        response = mock.Mock()
#        response.json = mock.Mock(return_value='')
#        sess = mock.Mock()
#        sess.post = mock.Mock(return_value=response)
#        backupRef = 'backupRef'
#
#        self.assertIsNotNone(sot.restore(sess, backupRef))
#
#        url = ("instances/%(id)s/action" % {
#            'id': IDENTIFIER,
#        })
#        body = {'restore': {'backupRef': backupRef}}
#        sess.post.assert_called_with(url, json=body, headers={'X-Language': 'en-us'})
