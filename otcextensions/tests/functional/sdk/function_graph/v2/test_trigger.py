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
from otcextensions.sdk.function_graph.v2 import function
from otcextensions.sdk.function_graph.v2 import trigger

from openstack import _log

from otcextensions.tests.functional.sdk.function_graph import TestFg

_logger = _log.setup_logging('openstack')


class TestFunctionTrigger(TestFg):
    ID = None
    uuid = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestFunctionTrigger, self).setUp()
        self.function = self.client.create_function(**TestFg.function_attrs)
        assert isinstance(self.function, function.Function)

        self.trigger_attrs = {
            "trigger_type_code": "TIMER",
            "trigger_status": "ACTIVE",
            "event_data": {
                "name": "Timer-l8v2",
                "schedule": "3m",
                "schedule_type": "Rate"
            }
        }

        self.trigger = self.client.create_trigger(
            self.function, **self.trigger_attrs
        )
        assert isinstance(self.trigger, trigger.Trigger)

        self.addCleanup(
            self.client.delete_function,
            self.function
        )
        self.addCleanup(
            self.client.delete_trigger,
            self.function.func_urn,
            self.trigger_attrs["trigger_type_code"],
            self.trigger.trigger_id
        )

    def test_triggers(self):
        elist = list(self.client.triggers(
            function_urn=self.function.func_urn))
        self.assertIn(self.trigger["id"], elist[0].id)
        self.assertIn(
            self.trigger_attrs["event_data"]["schedule"],
            elist[0].event_data.schedule
        )

    def test_get_trigger(self):
        tr = self.client.get_trigger(
            self.function.func_urn,
            self.trigger_attrs["trigger_type_code"],
            self.trigger.trigger_id)
        self.assertIn(self.trigger.trigger_id, tr.trigger_id)

    def test_update_trigger(self):
        attrs = {
            "trigger_status": "DISABLED",
        }
        updated = self.client.update_trigger(
            self.function.func_urn,
            self.trigger_attrs["trigger_type_code"],
            self.trigger.trigger_id,
            **attrs
        )
        self.assertIn(
            attrs['trigger_status'],
            updated.trigger_status
        )

    # def test_delete_all_triggers(self):
    #     deleted = self.client.delete_all_triggers(
    #         self.function.func_urn,
    #     )
    #     self.assertIsNone(deleted)
