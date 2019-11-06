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

from otcextensions.sdk.rds.v3 import _base


class TestBase(base.TestCase):
    def setUp(self):
        super(TestBase, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.delete = mock.Mock()
        self.sess.default_microversion = None
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self._translate_response = mock.Mock()

    def test_fetch(self):
        sot = _base.Resource.existing(id=1)
        sot._translate_response = mock.Mock()
        sot.allow_delete = True

        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {'job_id': 'fake'}
        response.headers = {}
        self.sess.delete.return_value = response

        # Restore from backup
        rt = sot.delete(self.sess)

        sot._translate_response.assert_called_with(response, has_body=True)
        self.assertIsInstance(rt, _base.Resource)
