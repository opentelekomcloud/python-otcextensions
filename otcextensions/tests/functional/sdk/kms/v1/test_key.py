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
from openstack import _log
from openstack import exceptions

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestKey(base.BaseFunctionalTest):
    KEY_ALIAS = 'sdk_test_key'
    cmks = []

    def setUp(self):
        super(TestKey, self).setUp()
        try:
            self.cmk = self.conn.kms.create_key(
                key_alias=TestKey.KEY_ALIAS
            )
        except exceptions.DuplicateResource:
            self.cmk = self.conn.kms.find_key(alias=TestKey.KEY_ALIAS)

        self.cmks.append(self.cmk)

    def tearDown(self):
        try:
            for key in self.cmks:
                if key.id:
                    self.conn.kms.schedule_key_deletion(key, 7)
        except exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)
        super(TestKey, self).tearDown()

    def test_list(self):
        self.keys = list(self.conn.kms.keys())
        self.assertGreaterEqual(len(self.keys), 0)
        if len(self.keys) > 0:
            key = self.keys[0]
            k = self.conn.kms.get_key(key=key.id)
            self.assertIsNotNone(k)
