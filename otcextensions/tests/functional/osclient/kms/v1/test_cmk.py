#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import json

from openstackclient.tests.functional import base


class TestCmk(base.TestCase):
    """Functional tests for CBR Task. """

    def test_cmk_list(self):
        json_output = json.loads(self.openstack(
            'kms cmk list -f json',
            cloud='terraform')
        )
        self.assertGreater(len(json_output), 0)
        name = json_output[0]['key_alias']
        self.openstack(f'kms cmk show {name}', cloud='terraform')

