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

from openstack.tests.unit import base

from otcextensions.sdk.function_graph.v2 import trigger

EXAMPLE = {
    "trigger_id": "9a14fae1-78cf-4185-ac7a-429eb6dc41fb",
    "trigger_type_code": "TIMER",
    "trigger_status": "ACTIVE",
    "event_data": {
        "name": "Timer-cpg3",
        "schedule": "3m",
        "schedule_type": "Rate"
    },
    "updated_at": "2022-11-09 16:37:24",
    "created_at": "2022-11-09 16:37:24"
}


class TestFunctionTrigger(base.TestCase):

    def test_basic(self):
        sot = trigger.Trigger()
        path = '/fgs/triggers/%(function_urn)s'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = trigger.Trigger(**EXAMPLE)
        self.assertEqual(EXAMPLE['trigger_id'], sot.trigger_id)
        self.assertEqual(EXAMPLE['trigger_type_code'], sot.trigger_type_code)
        self.assertEqual(EXAMPLE['trigger_status'], sot.trigger_status)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.created_at)
        self.assertEqual(EXAMPLE['event_data']['name'], sot.event_data.name)
        self.assertEqual(
            EXAMPLE['event_data']['schedule'],
            sot.event_data.schedule
        )
        self.assertEqual(
            EXAMPLE['event_data']['schedule_type'],
            sot.event_data.schedule_type
        )
