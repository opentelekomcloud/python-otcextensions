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
import mock

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.dcs.v1 import config

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
FAKE_INSTANCE_ID = "some_fake_id"
EXAMPLE = {
    "description": "some description",
    "param_id": FAKE_ID,
    "param_name": "maxmemory-policy",
    "param_value": "noeviction",
    "default_value": "noeviction",
    "value_type": "Enum",
    "value_range": "volatile-lru,allkeys-lru,volatile-random,"
}


class TestConfig(base.TestCase):

    def setUp(self):
        super(TestConfig, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = config.Config()

        self.assertEqual('/instances/%(instance_id)s/configs', sot.base_path)

        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = config.Config(instance_id=FAKE_INSTANCE_ID, **EXAMPLE)
        self.assertEqual(FAKE_INSTANCE_ID, sot.instance_id)
        self.assertEqual(EXAMPLE['param_id'], sot.id)
        self.assertEqual(EXAMPLE['param_name'], sot.name)
        self.assertEqual(EXAMPLE['param_value'], sot.value)
        self.assertEqual(EXAMPLE['default_value'], sot.default_value)
        self.assertEqual(EXAMPLE['value_type'], sot.value_type)
        self.assertEqual(EXAMPLE['value_range'], sot.value_range)

    def test_construct_param_for_update(self):
        sot = config.Config(instance_id=FAKE_INSTANCE_ID)
        sot_dirty = {
            'param_name': 'name',
            'param_value': 'val',
            'param_id': 'id',
            'dummy': 'dummy'
        }
        sot_expected = {
            'param_name': 'name',
            'param_value': 'val',
            'param_id': 'id',
        }

        res = sot._construct_dict_for_update(sot_dirty)
        self.assertDictEqual(sot_expected, res)

    def test_update(self):

        sot = config.Config(instance_id=FAKE_INSTANCE_ID)
        sot2 = {
            'param_name': 'name',
            'param_value': 'val',
            'param_id': 'id',
        }

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {}

        self.sess.put.return_value = mock_response

        sot._update(
            self.sess, [sot2]
        )

        self.sess.put.assert_called_once_with(
            '/instances/%s/configs' % FAKE_INSTANCE_ID,
            json={
                'redis_config': [sot2]}
        )
