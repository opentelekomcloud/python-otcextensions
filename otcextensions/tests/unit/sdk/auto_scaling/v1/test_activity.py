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

from otcextensions.sdk.auto_scaling.v1 import activity

EXAMPLE_LIST = {
    'limit': 20,
    'scaling_activity_log': [
        {
            'id': 'a8924393-1024-4c24-8ac6-e4d481360884',
            'status': 'SUCCESS',
            'description': '{\'reason\':[{\'change_reason\':\'SCHEDULED\','
                           '\'old_value\':1,\'change_time\':\''
                           '2015-07-24T01:21:00Z\',\'new_value\':0}]}',
            'instance_value': 1,
            'desire_value': 0,
            'start_time': '2015-07-24T01:21:02Z',
            'end_time': '2015-07-24T01:23:31Z',
            'instance_added_list': 'as-config-TEO_XQF2JJSI',
            'instance_removed_list': 'as-config-TEO_XQF2JJSI',
            'instance_deleted_list': 'as-config-TEO_XQF2JJSI',
            'scaling_value': '0',
        },
        {
            'id': '423bbb2d-043c-4afe-8754-03e418a6ac42',
            'status': 'SUCCESS',
            'description': '{\'reason\':[{\'change_reason\':\'DIFF\','
                           '\'old_value\':0,\'change_time\':\''
                           '2015-07-23T15:11:52Z\',\'new_value\':1}]}',
            'instance_value': 0,
            'desire_value': 1,
            'start_time': '2015-07-23T15:11:52Z',
            'end_time': '2015-07-23T15:16:30Z',
            'instance_added_list': 'as-config-TEO_XQF2JJSI'
        }
    ],
    'total_number': 2,
    'start_number': 0
}


class TestActivity(base.TestCase):

    def setUp(self):
        super(TestActivity, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()

        self.sot = activity.Activity()

    def test_basic(self):
        sot = activity.Activity()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('scaling_activity_log', sot.resources_key)
        self.assertEqual('/scaling_activity_log/%(scaling_group_id)s',
                         sot.base_path)
        self.assertEqual('as', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        obj = EXAMPLE_LIST['scaling_activity_log'][0]
        sot = activity.Activity.existing(**obj)
        self.assertEqual(obj['id'], sot.id)
        self.assertEqual(obj['status'], sot.status)
        self.assertEqual(obj['instance_value'], sot.instance_value)
        self.assertEqual(obj['scaling_value'], sot.scaling_value)
        self.assertEqual(obj['desire_value'], sot.desire_value)
        self.assertEqual(obj['start_time'], sot.start_time)
        self.assertEqual(obj['end_time'], sot.end_time)
        self.assertEqual(obj['instance_added_list'],
                         sot.instance_added_list)
        self.assertEqual(obj['instance_removed_list'],
                         sot.instance_removed_list)
        self.assertEqual(obj['instance_deleted_list'],
                         sot.instance_deleted_list)
        self.assertEqual(obj['description'], sot.description)

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
                start_time='a',
                end_time='b'
            )
        )

        self.sess.get.assert_called_once_with(
            '/scaling_activity_log/grp_id',
            params={
                'limit': 3,
                'start_number': 4,
                'start_time': 'a',
                'end_time': 'b'
            },
        )

        expected_list = [
            activity.Activity.existing(
                **EXAMPLE_LIST['scaling_activity_log'][0]),
            activity.Activity.existing(
                **EXAMPLE_LIST['scaling_activity_log'][1]),
        ]

        self.assertEqual(expected_list, result)
