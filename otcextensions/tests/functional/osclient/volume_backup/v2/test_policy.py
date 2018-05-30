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


CREATE_COMMAND = 'vbs policy create -f json %(name)s --start_time "10:00" ' \
    '--frequency 14 --rentention_num 2 --enable'


class VolumeBackupPolicyTests(base.TestCase):
    """Functional tests for vbs. """

    NAME = uuid.uuid4().hex
    OTHER_NAME = uuid.uuid4().hex

    @classmethod
    def setUpClass(cls):
        super(VolumeBackupPolicyTests, cls).setUpClass()
        json_output = json.loads(cls.openstack(
            CREATE_COMMAND % {'name': cls.NAME}
        ))
        cls.policy_id = json_output["id"]
        cls.assertOutput(cls.NAME, json_output['name'])

    @classmethod
    def tearDownClass(cls):
        try:
            cls.openstack(
                '--os-image-api-version 2 '
                'vbs policy delete ' +
                cls.policy_id
            )
        finally:
            super(VolumeBackupPolicyTests, cls).tearDownClass()

    def setUp(self):
        super(VolumeBackupPolicyTests, self).setUp()
        ver_fixture = fixtures.EnvironmentVariable(
            'OS_VBS_API_VERSION', '2'
        )
        self.useFixture(ver_fixture)

    def test_policy_list(self):
        json_output = json.loads(self.openstack(
            'vbs policy list -f json '
        ))
        self.assertIn(
            self.NAME,
            [img['name'] for img in json_output]
        )

    def test_policy_set_rename(self):
        name = uuid.uuid4().hex
        json_output = json.loads(self.openstack(
            CREATE_COMMAND % {'name': name}
        ))
        policy_id = json_output["id"]
        self.assertEqual(
            name,
            json_output["name"],
        )
        self.openstack(
            'vbs policy update ' +
            '--name ' + name + 'xx ' +
            policy_id
        )
        json_output = json.loads(self.openstack(
            'vbs policy show -f json ' +
            name + 'xx'
        ))
        self.assertEqual(
            name + 'xx',
            json_output["name"],
        )

    def test_policy_execute(self):
        self.openstack(
            'vbs policy execute ' +
            self.policy_id
        )
