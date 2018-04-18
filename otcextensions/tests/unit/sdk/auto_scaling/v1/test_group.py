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

from otcextensions.sdk.auto_scaling.v1 import group

EXAMPLE = {
    "networks": [
        {
            "id": " a8327883-6b07-4497-9c61-68d03ee193a "
        }
    ],
    "detail": None,
    "scaling_group_name": "healthCheck",
    "scaling_group_id": "77a7a397-7d2f-4e79-9da9-6a35e2709150",
    "scaling_group_status": "INSERVICE",
    "scaling_configuration_id": "1d281494-6085-4579-b817-c1f813be835f",
    "scaling_configuration_name": "healthCheck",
    "current_instance_number": 0,
    "desire_instance_number": 1,
    "min_instance_number": 0,
    "max_instance_number": 500,
    "cool_down_time": 300,
    "lb_listener_id": "f06c0112570743b51c0e8fbe1f235bab",
    "security_groups": [
        {
            "id": "8a4b1d5b-0054-419f-84b1-5c8a59ebc829"
        }
    ],
    "create_time": "2015-07-23T02:46:29Z",
    "vpc_id": "863ccae2-ee85-4d27-bc5b-3ba2a198a9e2",
    "health_periodic_audit_method": "ELB_AUDIT",
    "health_periodic_audit_time": "5",
    "instance_terminate_policy": "OLD_CONFIG_OLD_INSTANCE",
    "is_scaling": False,
    "delete_publicip": False,
    "notifications": [
        "EMAIL"
    ]
}


class TestGroup(base.TestCase):

    def setUp(self):
        super(TestGroup, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.get_project_id = mock.Mock()
        self.sot = group.Group(**EXAMPLE)

    def test_basic(self):
        sot = group.Group()
        self.assertEqual('scaling_group', sot.resource_key)
        self.assertEqual('scaling_groups', sot.resources_key)
        self.assertEqual('/scaling_group', sot.base_path)
        self.assertEqual('as', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = group.Group(**EXAMPLE)
        self.assertEqual(EXAMPLE['scaling_group_id'], sot.id)
        self.assertEqual(EXAMPLE['scaling_group_name'], sot.name)
        self.assertEqual(EXAMPLE['create_time'], sot.create_time)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'scaling_groups': [EXAMPLE]}

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess))

        self.sess.get.assert_called_once_with(
            '/scaling_group',
            params={},
        )

        self.assertEqual([group.Group(**EXAMPLE)], result)

    def test_get(self):
        sot = group.Group.existing(
            id=EXAMPLE['scaling_group_id'])
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = copy.deepcopy(EXAMPLE)

        self.sess.get.return_value = mock_response

        result = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            'scaling_group/%s' % EXAMPLE['scaling_group_id'],
        )

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['scaling_group_id'], result.id)
        self.assertEqual(EXAMPLE['scaling_group_name'], result.name)
