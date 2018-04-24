# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import copy

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.auto_scaling.v1 import config

EXAMPLE = {
    'tenant': 'ce061903a53545dcaddb300093b477d2',
    'scaling_configuration_id': '6afe46f9-7d3d-4046-8748-3b2a1085ad86',
    'scaling_configuration_name': 'config_name_1',
    'instance_config': {
        'disk': [
            {
                'size': 40,
                'volume_type': 'SATA',
                'disk_type': 'SYS'
            },
            {
                'size': 100,
                'volume_type': 'SATA',
                'disk_type': 'DATA'
            }
        ],
        'adminPass': '***',
        'personality': None,
        'instance_name': None,
        'instance_id': None,
        'flavorRef': '103',
        'imageRef': '37ca2b35-6fc7-47ab-93c7-900324809c5c',
        'key_name': 'keypair01',
        'public_ip': None,
        'user_data': None,
        'metadata': {}
    },
    'create_time': '2015-07-23T01:04:07Z'
}

EXAMPLE_LIST = {
    'limit': 20,
    'total_number': 2,
    'start_number': 0,
    'scaling_configurations': [
        {
            'tenant_id': 'ce061903a53545dcaddb300093b477d2',
            'status': 'STANDBY',
            'scaling_configuration_id': '6afe46f9-7d3d-4046-8748-3b2a1085ad86',
            'scaling_configuration_name': 'config_name_1',
            'instance_config': {
                'disk': [
                    {
                        'size': 40,
                        'volume_type': 'SATA',
                        'disk_type': 'SYS'
                    },
                    {
                        'size': 100,
                        'volume_type': 'SATA',
                        'disk_type': 'DATA'
                    }
                ],
                'adminPass': '***',
                'personality': None,
                'instance_name': None,
                'instance_id': None,
                'flavorRef': '103',
                'imageRef': '37ca2b35-6fc7-47ab-93c7-900324809c5c',
                'key_name': 'keypair02',
                'public_ip': None,
                'user_data': None,
                'metadate': {}
            },
            'create_time': '2015-07-23T01:04:07Z'
        },
        {
            'tenant_id': 'ce061903a53545dcaddb300093b477d2',
            'status': 'ACTIVE',
            'scaling_configuration_id': '24a8c5f3-c713-4aba-ac29-c17101009e5d',
            'scaling_configuration_name': 'config_name_2',
            'instance_config': {
                'disk': [
                    {
                        'size': 40,
                        'volume_type': 'SATA',
                        'disk_type': 'SYS'
                    }
                ],
                'adminPass': '***',
                'personality': None,
                'instance_name': None,
                'instance_id': None,
                'flavorRef': '103',
                'imageRef': '37ca2b35-6fc7-47ab-93c7-900324809c5c',
                'key_name': 'keypair01',
                'public_ip': None,
                'user_data': None,
                'metadata': {}
            },
            'create_time': '2015-07-22T01:08:41Z'
        }
    ]
}


class TestConfig(base.TestCase):

    def setUp(self):
        super(TestConfig, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.get_project_id = mock.Mock()
        self.sot = config.Config(**EXAMPLE)

    def test_basic(self):
        sot = config.Config()
        self.assertEqual('scaling_configuration', sot.resource_key)
        self.assertEqual('scaling_configurations', sot.resources_key)
        self.assertEqual('/scaling_configuration', sot.base_path)
        self.assertEqual('as', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = config.Config(**EXAMPLE)
        self.assertEqual(EXAMPLE['scaling_configuration_id'], sot.id)
        self.assertEqual(EXAMPLE['scaling_configuration_name'], sot.name)
        self.assertEqual(EXAMPLE['create_time'], sot.create_time)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST)

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess))

        self.sess.get.assert_called_once_with(
            '/scaling_configuration',
            params={},
        )

        expected_list = [
            config.Config.existing(
                **EXAMPLE_LIST['scaling_configurations'][0]),
            config.Config.existing(
                **EXAMPLE_LIST['scaling_configurations'][1])
        ]

        self.assertEqual(expected_list, result)

    def test_get(self):
        sot = config.Config.existing(
            id=EXAMPLE['scaling_configuration_id'])
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'scaling_configuration': EXAMPLE.copy()}

        self.sess.get.return_value = mock_response

        result = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            'scaling_configuration/%s' %
            EXAMPLE['scaling_configuration_id'],
        )

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['scaling_configuration_id'], result.id)
        self.assertEqual(EXAMPLE['scaling_configuration_name'], result.name)
