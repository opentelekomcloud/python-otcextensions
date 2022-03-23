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

import uuid
from keystoneauth1 import adapter
import mock
from openstack.tests.unit import base

from otcextensions.sdk.sdrs.v1 import dr_drill as _dr_drill


EXAMPLE = {
    'id': uuid.uuid4(),
    'name': 'Drill-8bcf',
    'status': 'available',
    'server_group_id': uuid.uuid4(),
    'drill_vpc_id': uuid.uuid4(),
    'created_at': '2022-03-06 19:30:34.91',
    'updated_at': '2022-03-06 19:31:16.354',
    'drill_servers': [
        {
            'protected_instance': uuid.uuid4(),
            'drill_server_id': uuid.uuid4()
        }
    ]
}


class TestDRDrill(base.TestCase):

    def setUp(self):
        super(TestDRDrill, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _dr_drill.DRDrill()

    def test_basic(self):
        sot = _dr_drill.DRDrill()
        self.assertEqual('disaster_recovery_drill', sot.resource_key)
        self.assertEqual('disaster_recovery_drills', sot.resources_key)
        self.assertEqual('/disaster-recovery-drills',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertDictEqual({
            'drill_vpc_id': 'drill_vpc_id',
            'limit': 'limit',
            'marker': 'marker',
            'name': 'name',
            'offset': 'offset',
            'server_group_id': 'server_group_id',
            'status': 'status'
        }, sot._query_mapping._mapping)

    def test_make_it(self):
        test_dr_drill = _dr_drill.DRDrill(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['id'],
            test_dr_drill.id)
        self.assertEqual(
            EXAMPLE['name'],
            test_dr_drill.name)
        self.assertEqual(
            EXAMPLE['status'],
            test_dr_drill.status)
        self.assertEqual(
            EXAMPLE['server_group_id'],
            test_dr_drill.server_group_id)
        self.assertEqual(
            EXAMPLE['drill_vpc_id'],
            test_dr_drill.drill_vpc_id)
        self.assertEqual(
            EXAMPLE['created_at'],
            test_dr_drill.created_at)
        self.assertEqual(
            EXAMPLE['updated_at'],
            test_dr_drill.updated_at)
        self.assertEqual(
            EXAMPLE['drill_servers'][0]['protected_instance'],
            test_dr_drill.drill_servers[0].protected_instance)
        self.assertEqual(
            EXAMPLE['drill_servers'][0]['drill_server_id'],
            test_dr_drill.drill_servers[0].drill_server_id)
