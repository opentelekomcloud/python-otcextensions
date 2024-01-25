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
#
from openstack.tests.unit import base
from otcextensions.sdk.modelartsv1.v1 import service

EXAMPLE = {
    "occur_time": 1562597251764,
    "event_type": "normal",
    "event_info": "start to deploy service",
}


class TestEvent(base.TestCase):
    def setUp(self):
        super(TestEvent, self).setUp()

    def test_basic(self):
        sot = service.Event()

        self.assertEqual("/services/%(service_id)s/events", sot.base_path)
        self.assertEqual("events", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual(
            {
                "event_type": "event_type",
                "start_time": "start_time",
                "end_time": "end_time",
                "marker": "marker",
                "offset": "offset",
                "limit": "limit",
                "sort_by": "sort_by",
                "order": "order",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        updated_sot_attrs = ()
        sot = service.Event(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
