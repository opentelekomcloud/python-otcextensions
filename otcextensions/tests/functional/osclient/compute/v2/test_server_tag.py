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


class TestCce(base.TestCase):
    """Functional tests for Compute Instance. """
    SERVER_ID = "d420440b-834d-4af2-92a2-e7eb03119123"

    def test_01_server_get(self):
        cmd = (
            f'server show {self.SERVER_ID} -f json '
        )
        json_output = json.loads(self.openstack(cmd))
        self.assertIsNotNone(json_output['id'])

    def test_02_create_server_tag(self):
        cmd = (
            f'server set {self.SERVER_ID} '
            f'--tag test=tag'
        )

        json_output = json.loads(self.openstack(cmd))
        print(json_output)
