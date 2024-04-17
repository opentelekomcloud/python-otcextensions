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
from otcextensions.sdk.modelartsv1.v1 import service_monitor
from otcextensions.tests.unit.sdk.modelartsv1.v1 import examples

EXAMPLE = examples.SERVICE_MONITOR


class TestServiceMonitor(base.TestCase):
    def setUp(self):
        super(TestServiceMonitor, self).setUp()

    def test_basic(self):
        sot = service_monitor.ServiceMonitor()

        self.assertEqual("/services/%(service_id)s/monitor", sot.base_path)
        self.assertEqual("monitors", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual(
            {
                "node_id": "node_id",
                "limit": "limit",
                "marker": "marker",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = service_monitor.ServiceMonitor(**EXAMPLE)

        for key, value in EXAMPLE.items():
            self.assertEqual(getattr(sot, key), value)
