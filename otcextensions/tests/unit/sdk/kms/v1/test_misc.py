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

from otcextensions.sdk.kms.v1 import misc

EXAMPLE = {
    'random_data': 'fd7d63ce-8f5c-443e-b9a0-bef9386b23b3',
    'random_data_length': 200,
}


class TestRandom(base.TestCase):

    def setUp(self):
        super(TestRandom, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        # self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sot = misc.Random()

    def test_basic(self):
        sot = misc.Random()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)
        self.assertEqual(
            '/kms/gen-random', sot.create_path)
        self.assertFalse(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = misc.Random.existing(**EXAMPLE)
        self.assertEqual(EXAMPLE['random_data'], sot.random_data)
        self.assertEqual(EXAMPLE['random_data_length'], sot.random_data_length)

    def test_create(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'random_data': EXAMPLE['random_data']
        }

        self.sess.post.return_value = mock_response

        sot = misc.Random.new(random_data_length=200)
        result = sot.create(self.sess, prepend_key=False)

        call_args = self.sess.post.call_args_list[0]

        self.assertEqual('/kms/gen-random', call_args[0][0])
        self.assertDictEqual({'random_data_length': 200}, call_args[1]['json'])

        self.sess.post.assert_called_once()

        self.assertEqual(sot, result)
        self.assertEqual(EXAMPLE['random_data'], result.random_data)
        self.assertEqual(EXAMPLE['random_data_length'],
                         result.random_data_length)


class TestInstanceNum(base.TestCase):

    def setUp(self):
        super(TestInstanceNum, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        # self.sess.get = mock.Mock()
        self.sess.get = mock.Mock()
        self.sot = misc.InstanceNumber()

    def test_get(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'instance_num': 5
        }

        self.sess.get.return_value = mock_response

        sot = misc.InstanceNumber()
        result = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            'kms/user-instances'
        )

        self.assertEqual(sot, result)
        self.assertEqual(5, result.instance_num)


class TestQuota(base.TestCase):

    def setUp(self):
        super(TestQuota, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            'quotas': {
                'resources': [{
                    'type': 'CMK',
                    'used': 15,
                    'quota': 20
                }, {
                    'type': 'grant_per_CMK',
                    'used': 15,
                    'quota': 100
                }]
            }
        }

        self.sess.get.return_value = mock_response

        sot = misc.Quota()
        result = list(sot.list(self.sess))

        self.sess.get.assert_called_once_with(
            'kms/user-quotas'
        )

        self.assertIsNotNone(result)
        self.assertEqual(2, len(result))
