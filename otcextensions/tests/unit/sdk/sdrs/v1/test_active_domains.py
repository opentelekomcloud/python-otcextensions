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

from otcextensions.sdk.sdrs.v1 import active_domains as _active_domains


class TestActiveDomains(base.TestCase):

    def setUp(self):
        super(TestActiveDomains, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.list = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _active_domains.ActiveDomains()

    def test_basic(self):
        sot = _active_domains.ActiveDomains()
        self.assertEqual('/active-domains',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)
