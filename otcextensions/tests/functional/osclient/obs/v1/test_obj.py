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
import filecmp
import os
import uuid

import fixtures

from openstackclient.tests.functional import base


CONTAINER_CREATE_COMMAND = 'obs container create %(name)s -f json'
OBJECT_CREATE_COMMAND = 'obs object create %(container)s %(name)s -f json'

CONTAINER_DELETE_COMMAND = 'obs container delete %(name)s'
OBJECT_DELETE_COMMAND = 'obs object delete %(container)s %(name)s'


class ObsObjectTests(base.TestCase):
    """Functional tests for vbs. """

    CONTAINER_NAME = uuid.uuid4().hex
    OBJECT_NAME = uuid.uuid4().hex + '.tmp'

    OBJECT_CONTENT = uuid.uuid4().hex

    @classmethod
    def setUpClass(cls):
        super(ObsObjectTests, cls).setUpClass()
        json_output = json.loads(cls.openstack(
            CONTAINER_CREATE_COMMAND % {'name': cls.CONTAINER_NAME}
        ))
        cls.container_id = json_output["id"]
        cls.assertOutput(cls.CONTAINER_NAME, json_output['name'])
        with open(cls.OBJECT_NAME, 'w') as file:
            file.write(cls.OBJECT_CONTENT)
        json_output = json.loads(cls.openstack(
            OBJECT_CREATE_COMMAND % {
                'name': cls.OBJECT_NAME,
                'container': cls.CONTAINER_NAME
            }
        ))
        cls.object_id = json_output["id"]
        cls.assertOutput(cls.OBJECT_NAME, json_output['name'])

    @classmethod
    def tearDownClass(cls):
        try:
            cls.openstack(
                OBJECT_DELETE_COMMAND % {
                    'name': cls.OBJECT_NAME,
                    'container': cls.CONTAINER_NAME
                }
            )
            cls.openstack(
                CONTAINER_DELETE_COMMAND % {'name': cls.CONTAINER_NAME}
            )
            os.remove(cls.OBJECT_NAME)
        finally:
            super(ObsObjectTests, cls).tearDownClass()

    def setUp(self):
        super(ObsObjectTests, self).setUp()
        ver_fixture = fixtures.EnvironmentVariable(
            'OS_OBS_API_VERSION', '1'
        )
        self.useFixture(ver_fixture)

    def test_object_list(self):
        json_output = json.loads(self.openstack(
            'obs object list %(container)s -f json ' % {
                'container': self.CONTAINER_NAME
            }
        ))
        self.assertIn(
            self.OBJECT_NAME,
            [cont['name'] for cont in json_output]
        )

    def test_object_save(self):
        download_name = self.OBJECT_NAME + '_output'
        self.openstack(
            'obs object save %(container)s %(name)s --file %(output)s' % {
                'container': self.CONTAINER_NAME,
                'name': self.OBJECT_NAME,
                'output': download_name
            }
        )
        self.assertTrue(filecmp.cmp(self.OBJECT_NAME, download_name))
        os.remove(download_name)
