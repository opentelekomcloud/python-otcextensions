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

from otcextensions.sdk.sdrs.v1 import protection_group as _protection_group


EXAMPLE = {
    'id': uuid.uuid4(),
    'name': uuid.uuid4(),
    'description': uuid.uuid4(),
    'source_availability_zone': uuid.uuid4(),
    'target_availability_zone': uuid.uuid4(),
    'domain_id': uuid.uuid4(),
    'domain_name': uuid.uuid4(),
    'status': 'available',
    'protected_status': None,
    'replication_status': None,
    'health_status': None,
    'progress': 0,
    'priority_station': 'source',
    'protected_instance_num': 0,
    'replication_num': 0,
    'disaster_recovery_drill_num': 0,
    'source_vpc_id': uuid.uuid4(),
    'target_vpc_id': uuid.uuid4(),
    'test_vpc_id': None,
    'dr_type': 'migration',
    'created_at': '2022-02-26 20:39:30.718',
    'updated_at': '2022-02-26 21:02:45.507',
    'protection_type': 'replication-pair',
    'replication_model': None
}


class TestJob(base.TestCase):

    def setUp(self):
        super(TestJob, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _protection_group.ProtectionGroup()

    def test_basic(self):
        sot = _protection_group.ProtectionGroup()
        self.assertEqual('server_group', sot.resource_key)
        self.assertEqual('server_groups', sot.resources_key)
        self.assertEqual('/server-groups',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertDictEqual({
            'availability_zone': 'availability_zone',
            'limit': 'limit',
            'marker': 'marker',
            'name': 'name',
            'offset': 'offset',
            'query_type': 'query_type',
            'status': 'status'
        }, sot._query_mapping._mapping)

    def test_make_it(self):
        test_protection_group = _protection_group.ProtectionGroup(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['id'],
            test_protection_group.id)
        self.assertEqual(
            EXAMPLE['description'],
            test_protection_group.description)
        self.assertEqual(
            EXAMPLE['source_availability_zone'],
            test_protection_group.source_availability_zone)
        self.assertEqual(
            EXAMPLE['target_availability_zone'],
            test_protection_group.target_availability_zone)
        self.assertEqual(
            EXAMPLE['domain_id'],
            test_protection_group.domain_id)
        self.assertEqual(
            EXAMPLE['domain_name'],
            test_protection_group.domain_name)
        self.assertEqual(
            EXAMPLE['status'],
            test_protection_group.status)
        self.assertEqual(
            EXAMPLE['protected_status'],
            test_protection_group.protected_status)
        self.assertEqual(
            EXAMPLE['replication_status'],
            test_protection_group.replication_status)
        self.assertEqual(
            EXAMPLE['health_status'],
            test_protection_group.health_status)
        self.assertEqual(
            EXAMPLE['progress'],
            test_protection_group.progress)
        self.assertEqual(
            EXAMPLE['priority_station'],
            test_protection_group.priority_station)
        self.assertEqual(
            EXAMPLE['protected_instance_num'],
            test_protection_group.protected_instance_num)
        self.assertEqual(
            EXAMPLE['replication_num'],
            test_protection_group.replication_num)
        self.assertEqual(
            EXAMPLE['disaster_recovery_drill_num'],
            test_protection_group.disaster_recovery_drill_num)
        self.assertEqual(
            EXAMPLE['source_vpc_id'],
            test_protection_group.source_vpc_id)
        self.assertEqual(
            EXAMPLE['target_vpc_id'],
            test_protection_group.target_vpc_id)
        self.assertEqual(
            EXAMPLE['test_vpc_id'],
            test_protection_group.test_vpc_id)
        self.assertEqual(
            EXAMPLE['dr_type'],
            test_protection_group.dr_type)
        self.assertEqual(
            EXAMPLE['created_at'],
            test_protection_group.created_at)
        self.assertEqual(
            EXAMPLE['updated_at'],
            test_protection_group.updated_at)
        self.assertEqual(
            EXAMPLE['protection_type'],
            test_protection_group.protection_type)
        self.assertEqual(
            EXAMPLE['replication_model'],
            test_protection_group.replication_model)
