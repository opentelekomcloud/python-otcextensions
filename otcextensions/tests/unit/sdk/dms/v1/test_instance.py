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

from unittest import mock

from openstack.tests.unit import base

from otcextensions.sdk.dms.v1 import instance


JSON_DATA = {
    "name": "kafka-test",
    "description": "",
    "engine": "kafka",
    "engine_version": "2.3.0",
    "storage_space": 600,
    "access_user": "",
    "password": "",
    "vpc_id": "1e93f86e-13af-46c8-97d6-d40fa62b76c2",
    "security_group_id": "0aaa0033-bf7f-4c41-a6c2-18cd04cad2c8",
    "subnet_id": "b5fa806c-35e7-4299-b659-b39398dd4718",
    "available_zones": ["d573142f24894ef3bd3664de068b44b0"],
    "product_id": "00300-30308-0--0",
    "maintain_begin": "22:00",
    "maintain_end": "02:00",
    "ssl_enable": False,
    "enable_publicip": False,
    "publicip_id": "",
    "specification": "100MB",
    "partition_num": "300",
    "retention_policy": "produce_reject",
    "connector_enable": False,
    "storage_spec_code": "dms.physical.storage.ultra"
}


class TestInstance(base.TestCase):

    def setUp(self):
        super(TestInstance, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

    def test_basic(self):
        sot = instance.Instance()

        self.assertEqual('/instances', sot.base_path)
        self.assertEqual('instances', sot.resources_key)

        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

        self.assertDictEqual({
            'engine_name': 'engine',
            'exact_match_name': 'exactMatchName',
            'include_failure': 'includeFailure',
            'limit': 'limit',
            'marker': 'marker',
            'name': 'name',
            'status': 'status'},
            sot._query_mapping._mapping
        )

    def test_make_it(self):
        sot = instance.Instance(**JSON_DATA)
        self.assertEqual(JSON_DATA['name'], sot.name)
        self.assertEqual(JSON_DATA['access_user'], sot.access_user)
        self.assertEqual(JSON_DATA['available_zones'], sot.availability_zones)
        self.assertEqual(JSON_DATA.get('charging_mode', None),
                         sot.charging_mode)
        self.assertEqual(JSON_DATA.get('connect_address', None),
                         sot.connect_address)
        self.assertEqual(JSON_DATA.get('created_at', None),
                         sot.created_at)
        self.assertEqual(JSON_DATA.get('description', None),
                         sot.description)
        self.assertEqual(JSON_DATA.get('engine', None),
                         sot.engine_name)
        self.assertEqual(JSON_DATA.get('engine_version', None),
                         sot.engine_version)
        self.assertEqual(JSON_DATA.get('instance_id', None),
                         sot.id)
        self.assertEqual(JSON_DATA.get('enable_publicip', False),
                         sot.is_public)
        self.assertEqual(JSON_DATA.get('ssl_enable', None),
                         sot.is_ssl)
        self.assertEqual(JSON_DATA.get('kafka_public_status', None),
                         sot.kafka_public_status)
        self.assertEqual(JSON_DATA.get('maintain_end', None),
                         sot.maintenance_end)
        self.assertEqual(JSON_DATA.get('maintain_begin', None),
                         sot.maintenance_start)
        self.assertEqual(int(JSON_DATA.get('partition_num', None)),
                         sot.max_partitions)
        self.assertEqual(JSON_DATA.get('password', None),
                         sot.password)
        self.assertEqual(JSON_DATA.get('port', None),
                         sot.port)
        self.assertEqual(JSON_DATA.get('product_id', None),
                         sot.product_id)
        self.assertEqual(JSON_DATA.get('public_bandwidth', None),
                         sot.public_bandwidth)
        self.assertEqual(JSON_DATA.get('retention_policy', None),
                         sot.retention_policy)
        self.assertEqual(JSON_DATA.get('vpc_id', None),
                         sot.router_id)
        self.assertEqual(JSON_DATA.get('vpc_name', None),
                         sot.router_name)
        self.assertEqual(JSON_DATA.get('security_group_id', None),
                         sot.security_group_id)
        self.assertEqual(JSON_DATA.get('security_group_name', None),
                         sot.security_group_name)
        self.assertEqual(JSON_DATA.get('service_type', None),
                         sot.service_type)
        self.assertEqual(JSON_DATA.get('specification', None),
                         sot.spec)
        self.assertEqual(JSON_DATA.get('resource_spec_code', None),
                         sot.spec_code)
        self.assertEqual(JSON_DATA.get('status', None),
                         sot.status)
        self.assertEqual(JSON_DATA.get('storage_resource_id', None),
                         sot.storage_resource_id)
        self.assertEqual(JSON_DATA.get('storage_spec_code', None),
                         sot.storage_spec_code)
        self.assertEqual(JSON_DATA.get('storage_type', None),
                         sot.storage_type)
        self.assertEqual(JSON_DATA.get('storage_space', None),
                         sot.storage)
        self.assertEqual(JSON_DATA.get('subnet_id', None),
                         sot.network_id)
        self.assertEqual(JSON_DATA.get('total_storage_space', None),
                         sot.total_storage)
        self.assertEqual(JSON_DATA.get('type', None),
                         sot.type)
        self.assertEqual(JSON_DATA.get('used_storage_space', None),
                         sot.storage_type)
        self.assertEqual(JSON_DATA.get('user_id', None),
                         sot.user_id)
        self.assertEqual(JSON_DATA.get('user_name', None),
                         sot.user_name)

    def test_restart(self):
        sot = instance.Instance(id='1')
        response = mock.Mock()
        response.status_code = 200

        self.sess.post.return_value = response

        sot.restart(self.sess)

        self.sess.post.assert_called_with(
            '/instances/action',
            json={'action': 'restart', 'instances': ['1']}
        )

        sot.restart_batch(self.sess, ['1', '2'])

        self.sess.post.assert_called_with(
            '/instances/action',
            json={'action': 'restart', 'instances': ['1', '2']}
        )

    def test_delete(self):
        sot = instance.Instance()
        response = mock.Mock()
        response.status_code = 200

        self.sess.post.return_value = response

        sot.delete_batch(self.sess, ['1', '2'])

        self.sess.post.assert_called_with(
            '/instances/action',
            json={'action': 'delete', 'instances': ['1', '2']}
        )

        sot.delete_failed(self.sess)

        self.sess.post.assert_called_with(
            '/instances/action',
            json={'action': 'delete', 'allFailure': 'kafka'}
        )
