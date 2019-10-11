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
from keystoneauth1 import adapter

import copy
import mock

from openstack import resource

from openstack.tests.unit import base

from otcextensions.sdk.rds.v3 import configuration


IDENTIFIER = 'ID'
EXAMPLE = {
    "id": IDENTIFIER,
    "name": "paramsGroup-b6d2",
    "description": "",
    "datastore": {"type": "PostgreSQL"},
    "datastore_version_name": "2016_SE",
    "datastore_name": "sqlserver",
    "created": "2018-09-15T03:33:07+0800",
    "updated": "2018-09-15T03:33:07+0800",
    "user_defined": True,
    "vcpus": "1",
    "ram": 2,
    "spec_code": "rds.mysql.c2.medium.ha",
    "instance_mode": "ha",
    "values": {
        "max_connections": "10",
        "autocommit": "OFF"
    }
}


class TestConfiguration(base.TestCase):

    def setUp(self):
        super(TestConfiguration, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = configuration.Configuration()

        self.assertEqual('/configurations', sot.base_path)
        self.assertEqual('configurations', sot.resources_key)
        self.assertEqual('configuration', sot.resource_key)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = configuration.Configuration(**EXAMPLE)
        self.assertEqual(IDENTIFIER, sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['datastore'], sot.datastore)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['datastore_name'], sot.datastore_name)
        self.assertEqual(EXAMPLE['datastore_version_name'],
                         sot.datastore_version_name)
        self.assertEqual(EXAMPLE['created'], sot.created_at)
        self.assertEqual(EXAMPLE['updated'], sot.updated_at)
        self.assertEqual(EXAMPLE['user_defined'], sot.is_user_defined)
        self.assertEqual(EXAMPLE['values'], sot.values)

    def test_apply(self):
        sot = configuration.Configuration(id=IDENTIFIER)
        instances = ['id1', 'id2']

        resp = mock.Mock()
        resp.body = {
            "configuration_id": IDENTIFIER,
            "configuration_name": "paramsGroup-bcf9",
            "apply_results": [{
                "instance_id": "fe5f5a07539c431181fc78220713aebein01",
                "instance_name": "zyy1",
                "restart_required": False,
                "success": False
            }, {
                "instance_id": "73ea2bf70c73497f89ee0ad4ee008aa2in01",
                "instance_name": "zyy2",
                "restart_required": False,
                "success": False
            }],
            "success": False
        }
        resp.json = mock.Mock(return_value=copy.deepcopy(resp.body))
        resp.headers = {}
        resp.status_code = 200
        self.sess.put.return_value = resp

        updated = sot.apply(self.sess, instances)
        self.sess.put.assert_called_with(
            'configurations/ID/apply',
            json={'instance_ids': ['id1', 'id2']}
        )

        self.assertEqual(resp.body['configuration_id'], updated.id)
        self.assertEqual(resp.body['configuration_name'], updated.name)
        self.assertEqual(resp.body['apply_results'],
                         sot.apply_results)

    def test_create(self):
        sot = configuration.Configuration(id=IDENTIFIER)

        with mock.patch.object(resource.Resource, 'create') as res_mock:
            sot.create(self.sess)
            res_mock.assert_called_with(self.sess,
                                        prepend_key=False,
                                        base_path=None)

    def test_commit(self):
        sot = configuration.Configuration(id=IDENTIFIER)

        with mock.patch.object(resource.Resource, 'commit') as res_mock:
            sot.commit(self.sess)
            res_mock.assert_called_with(self.sess,
                                        prepend_key=False)
