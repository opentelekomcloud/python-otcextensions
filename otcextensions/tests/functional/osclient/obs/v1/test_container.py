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
import uuid

import fixtures

from openstackclient.tests.functional import base


CREATE_COMMAND = 'obs container create %(name)s -f json'

DELETE_COMMAND = 'obs container delete %(name)s'


class ObsContainerTests(base.TestCase):
    """Functional tests for vbs. """

    NAME = uuid.uuid4().hex
    OTHER_NAME = uuid.uuid4().hex

    def tearDown(self):
        try:
            self.openstack(
                DELETE_COMMAND % {'name': self.NAME}
            )
        finally:
            super(ObsContainerTests, self).tearDown()

    def setUp(self):
        super(ObsContainerTests, self).setUp()
        json_output = json.loads(self.openstack(
            CREATE_COMMAND % {'name': self.NAME}
        ))
        self.container_id = json_output["id"]
        self.assertOutput(self.NAME, json_output['name'])

        ver_fixture = fixtures.EnvironmentVariable(
            'OS_OBS_API_VERSION', '1'
        )
        self.useFixture(ver_fixture)

    def test_container_list(self):
        json_output = json.loads(self.openstack(
            'obs container list -f json '
        ))
        self.assertIn(
            self.NAME,
            [cont['name'] for cont in json_output]
        )
