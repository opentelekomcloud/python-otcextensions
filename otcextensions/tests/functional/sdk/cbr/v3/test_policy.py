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

import uuid

from openstack import _log
from otcextensions.sdk.cbr.v3 import policy
from otcextensions.tests.functional import base

_logger = _log.setup_logging("openstack")


class TestPolicy(base.BaseFunctionalTest):

    def setUp(self):
        super(TestPolicy, self).setUp()
        self.cbr = self.conn.cbr
        self.NAME = "sdk-test-cbr-policy-" + uuid.uuid4().hex[:8]
        self.UPDATE_NAME = self.NAME + "-upd"
        self.attrs = {
            "enabled": True,
            "name": self.NAME,
            "operation_definition": {
                "timezone": "UTC+03:00",
            },
            "operation_type": "backup",
            "trigger": {
                "properties": {
                    "pattern": [
                        "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=14;BYMINUTE=00"
                    ]
                }
            },
        }

        self.policy = self.cbr.create_policy(**self.attrs)
        assert isinstance(self.policy, policy.Policy)
        self.ID = self.policy.id
        self.addCleanup(self.cbr.delete_policy, self.policy, ignore_missing=True)

    def test_policies(self):
        policies = list(self.cbr.policies(operation_type="backup"))
        self.assertIn(self.ID, [item.id for item in policies])

    def test_get_policy(self):
        found = self.cbr.get_policy(self.policy)
        self.assertEqual(self.ID, found.id)
        self.assertEqual(self.NAME, found.name)
        self.assertEqual(self.attrs["operation_type"], found.operation_type)

    def test_find_policy(self):
        found = self.cbr.find_policy(self.NAME, ignore_missing=False)
        self.assertEqual(self.ID, found.id)

    def test_update_policy(self):
        updated = self.cbr.update_policy(
            self.policy,
            name=self.UPDATE_NAME,
            enabled=False,
        )
        self.assertEqual(self.ID, updated.id)
        self.assertEqual(self.UPDATE_NAME, updated.name)
        self.assertFalse(updated.enabled)
