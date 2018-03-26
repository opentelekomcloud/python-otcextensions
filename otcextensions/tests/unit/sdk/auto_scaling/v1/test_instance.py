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
import mock

from keystoneauth1 import adapter

from openstack.tests.unit import base

from openstack import exceptions

from otcextensions.sdk.auto_scaling.v1 import instance

# EXAMPLE = {
#     'scaling_instance_id': 'fd7d63ce-8f5c-443e-b9a0-bef9386b23b3',
#     'scaling_group_id': 'e5d27f5c-dd76-4a61-b4bc-a67c5686719a',
#     'scaling_instance_name': 'schedule1',
#     'scaling_instance_type': 'SCHEDULED',
#     'scheduled_instance': {
#         'launch_time': '2015-07-24T01:21Z'
#     },
#     'cool_down_time': 300,
#     'scaling_instance_action': {
#         'operation': 'REMOVE',
#         'instance_number': 1
#     },
#     'instance_status': 'INSERVICE',
#     'create_time': '2015-07-24T01:09:30Z'
# }

EXAMPLE_LIST = {
    'limit': 10,
    'total_number': 1,
    'start_number': 0,
    'scaling_group_instances': [
        {
            'instance_id': 'b25c1589-c96c-465b-9fef-d06540d1945c',
            'scaling_group_id': 'e5d27f5c-dd76-4a61-b4bc-a67c5686719a',
            'scaling_group_name': 'discuz',
            'life_cycle_state': 'INSERVICE',
            'health_status': 'NORMAL',
            'scaling_configuration_name': 'discuz',
            'scaling_configuration_id': 'ca3dcd84-d197-4c4f-af2a-cf8ba39696ac',
            'create_time': '2015-07-23T06:47:33Z',
            'instance_name': 'discuz_3D210808'
        }
    ]
}


class TestInstance(base.TestCase):

    def setUp(self):
        super(TestInstance, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sot = instance.Instance()

    def test_basic(self):
        sot = instance.Instance()
        self.assertEqual('scaling_group_instance', sot.resource_key)
        self.assertEqual('scaling_group_instances', sot.resources_key)
        self.assertEqual('/scaling_group_instance', sot.base_path)
        self.assertEqual(
            '/scaling_group_instance/%(scaling_group_id)s/list', sot.list_path)
        self.assertEqual('as', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        obj = EXAMPLE_LIST['scaling_group_instances'][0].copy()
        sot = instance.Instance.existing(**obj)
        self.assertEqual(obj['instance_id'], sot.id)
        self.assertEqual(obj['instance_name'], sot.name)
        self.assertEqual(obj['scaling_group_name'], sot.scaling_group_name)
        self.assertEqual(obj['life_cycle_state'], sot.lifecycle_state)
        self.assertEqual(obj['health_status'], sot.health_status)
        self.assertEqual(obj['scaling_configuration_name'],
                         sot.scaling_configuration_name)
        self.assertEqual(obj['scaling_configuration_id'],
                         sot.scaling_configuration_id)
        self.assertEqual(obj['create_time'], sot.create_time)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST)

        self.sess.get.return_value = mock_response

        result = list(
            self.sot.list(
                self.sess,
                scaling_group_id='grp_id',
                limit=3,
                marker=4,
                life_cycle_state='t1',
                health_status='t2',
            )
        )

        self.sess.get.assert_called_once_with(
            '/scaling_group_instance/grp_id/list',
            params={
                'limit': 3,
                'start_number': 4,
                'life_cycle_state': 't1',
                'health_status': 't2',
            },
        )

        expected_list = [
            instance.Instance.existing(
                **EXAMPLE_LIST['scaling_group_instances'][0]),
        ]

        self.assertEqual(expected_list, result)

    def test_batch_add(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.post.return_value = mock_response

        sot = instance.Instance.existing(scaling_group_id='grp_id')

        obj_list = ['i1', 'i2']

        sot.batch_add(self.sess, obj_list)

        self.sess.post.assert_called_once_with(
            'scaling_group_instance/grp_id/action',
            json={'action': 'ADD', 'instances_id': obj_list}
        )

    def test_batch_remove(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.post.return_value = mock_response

        sot = instance.Instance.existing(scaling_group_id='grp_id')

        obj_list = ['i1', 'i2']

        sot.batch_remove(self.sess, obj_list, delete_instance=True)

        self.sess.post.assert_called_once_with(
            'scaling_group_instance/grp_id/action',
            json={
                'action': 'REMOVE',
                'instances_id': obj_list,
                'instance_delete': 'yes'
            }
        )

    def test_batch_action_act_check(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.post.return_value = mock_response

        sot = instance.Instance.existing(scaling_group_id='grp_id')

        obj_list = ['i1', 'i2']

        self.assertRaises(
            exceptions.SDKException, sot.batch_action,
            session=self.sess, instances=obj_list, action='f')

    def test_batch_action_add(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.post.return_value = mock_response

        sot = instance.Instance.existing(scaling_group_id='grp_id')

        obj_list = ['i1', 'i2']

        sot.batch_action(self.sess, obj_list, 'ADD')

        self.sess.post.assert_called_once_with(
            'scaling_group_instance/grp_id/action',
            json={
                'action': 'ADD',
                'instances_id': obj_list,
            }
        )

    def test_batch_action_remove(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.post.return_value = mock_response

        sot = instance.Instance.existing(scaling_group_id='grp_id')

        obj_list = ['i1', 'i2']

        sot.batch_action(self.sess, obj_list, 'REMOVE', delete_instance=True)

        self.sess.post.assert_called_once_with(
            'scaling_group_instance/grp_id/action',
            json={
                'action': 'REMOVE',
                'instances_id': obj_list,
                'instance_delete': 'yes'
            }
        )

    def test_batch_action_protect(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.post.return_value = mock_response

        sot = instance.Instance.existing(scaling_group_id='grp_id')

        obj_list = ['i1', 'i2']

        sot.batch_action(self.sess, obj_list, 'PROTECT')

        self.sess.post.assert_called_once_with(
            'scaling_group_instance/grp_id/action',
            json={
                'action': 'PROTECT',
                'instances_id': obj_list,
            }
        )

    def test_batch_action_unprotect(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.post.return_value = mock_response

        sot = instance.Instance.existing(scaling_group_id='grp_id')

        obj_list = ['i1', 'i2']

        sot.batch_action(self.sess, obj_list, 'UNPROTECT')

        self.sess.post.assert_called_once_with(
            'scaling_group_instance/grp_id/action',
            json={
                'action': 'UNPROTECT',
                'instances_id': obj_list,
            }
        )

    def test_batch_action_delete_instance_not_expected(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.post.return_value = mock_response

        sot = instance.Instance.existing(scaling_group_id='grp_id')

        obj_list = ['i1', 'i2']

        self.assertRaises(
            exceptions.SDKException, sot.batch_action,
            session=self.sess, instances=obj_list,
            action='PROTECT', delete_instance=True)

    def test_remove(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.delete.return_value = mock_response

        sot = instance.Instance.existing(id='id1', scaling_group_id='grp_id')

        sot.remove(self.sess, delete_instance=True)

        self.sess.delete.assert_called_once_with(
            'scaling_group_instance/%s' % sot.id,
            params={
                'instance_delete': 'yes'
            }
        )

    def test_remove_default(self):
        mock_response = mock.Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None

        self.sess.delete.return_value = mock_response

        sot = instance.Instance.existing(id='id1', scaling_group_id='grp_id')

        sot.remove(self.sess)

        self.sess.delete.assert_called_once_with(
            'scaling_group_instance/%s' % sot.id,
            params={
                'instance_delete': 'no'
            }
        )
