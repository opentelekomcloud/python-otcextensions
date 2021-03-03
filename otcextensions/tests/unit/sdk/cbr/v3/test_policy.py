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
import mock
from openstack.tests.unit import base

from otcextensions.sdk.cbr.v3 import policy as _policy


EXAMPLE = {
    'enabled': True,
    'name': 'my_policy',
    'operation_definition': {
        'day_backups': 0,
        'month_backups': 0,
        'max_backups': 1,
        'timezone': 'UTC+08:00',
        'week_backups': 0,
        'year_backups': 0
    },
    'operation_type': 'backup',
    'trigger': {
        'properties': {
            'pattern': [
                'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=14;BYMINUTE=00'
            ]
        }
    }
}


class TestPolicy(base.TestCase):

    def setUp(self):
        super(TestPolicy, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.list = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _policy.Policy()
        self.sot_expected = _policy.Policy(**EXAMPLE)

    def test_basic(self):
        sot = _policy.Policy()
        self.assertEqual('policy', sot.resource_key)
        self.assertEqual('policies', sot.resources_key)
        self.assertEqual('/policies',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        test_policy = _policy.Policy(**EXAMPLE)
        self.assertTrue(test_policy.enabled)
        self.assertEqual(
            EXAMPLE['name'],
            test_policy.name)
        self.assertEqual(
            EXAMPLE['operation_type'],
            test_policy.operation_type)
        self.assertEqual(
            EXAMPLE['operation_definition']['day_backups'],
            test_policy.operation_definition.day_backups)
        self.assertEqual(
            EXAMPLE['operation_definition']['month_backups'],
            test_policy.operation_definition.month_backups)
        self.assertEqual(
            EXAMPLE['operation_definition']['max_backups'],
            test_policy.operation_definition.max_backups)
        self.assertEqual(
            EXAMPLE['operation_definition']['timezone'],
            test_policy.operation_definition.timezone)
        self.assertEqual(
            EXAMPLE['operation_definition']['week_backups'],
            test_policy.operation_definition.week_backups)
        self.assertEqual(
            EXAMPLE['operation_definition']['year_backups'],
            test_policy.operation_definition.year_backups)
        self.assertEqual(
            EXAMPLE['trigger']['properties']['pattern'][0],
            test_policy.trigger.properties.pattern[0])
