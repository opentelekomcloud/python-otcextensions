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

from otcextensions.sdk.sdrs.v1 import quota as _quota


EXAMPLE = {
    'resources': [
        {
            'type': 'server_groups',
            'used': 2,
            'quota': 10,
            'min': 0,
            'max': -1
        },
        {
            'type': 'replications',
            'used': 1,
            'quota': 100,
            'min': 0,
            'max': -1
        }
    ]
}


class TestQuota(base.TestCase):

    def setUp(self):
        super(TestQuota, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _quota.Quota()

    def test_basic(self):
        sot = _quota.Quota()
        self.assertEqual('quotas', sot.resources_key)
        self.assertEqual('/sdrs/quotas',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        test_quota = _quota.Quota(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['resources'],
            test_quota.resources)
