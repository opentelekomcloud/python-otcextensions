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

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestServiceSpecification(base.BaseFunctionalTest):

    def setUp(self):
        super(TestServiceSpecification, self).setUp()
        self.dcs = self.conn.dcs

    def test_service_specification(self):
        objects = list(self.dcs.service_specifications())

        self.assertEqual(len(objects), 3)

        for obj in objects:
            self.assertIsInstance(obj, dict)
            self.assertIn("details", obj.keys())
            self.assertIn("engine", obj.keys())
            self.assertIn("price", obj.keys())
            self.assertIn("currency", obj.keys())
            self.assertIn("flavors", obj.keys())
            self.assertIn("product_id", obj.keys())
            self.assertIn("spec_code", obj.keys())
            self.assertIn("cache_mode", obj.keys())
            self.assertIn("product_type", obj.keys())
            self.assertIn("cpu_type", obj.keys())
            self.assertIn("storage_type", obj.keys())
            self.assertIn("engine_versions", obj.keys())
            self.assertIn("spec_details", obj.keys())
            self.assertIn("spec_details2", obj.keys())
            self.assertIn("charging_type", obj.keys())
            self.assertIn("prod_type", obj.keys())
            self.assertIn("cloud_service_type_code", obj.keys())
            self.assertIn("cloud_resource_type_code", obj.keys())

    def test_service_specification_details(self):
        objects = list(self.dcs.service_specifications())
        details = []

        for obj in objects:
            details.append(obj["details"])

        for obj in details:
            self.assertIsInstance(obj, dict)
            self.assertIn("capacity", obj.keys())
            self.assertIn("max_bandwidth", obj.keys())
            self.assertIn("max_clients", obj.keys())
            self.assertIn("max_connections", obj.keys())
            self.assertIn("max_in_bandwidth", obj.keys())
            self.assertIn("max_memory", obj.keys())
            self.assertIn("tenant_ip_count", obj.keys())
            self.assertIn("sharding_num", obj.keys())
            self.assertIn("proxy_num", obj.keys())
            self.assertIn("db_number", obj.keys())

    def test_service_specification_flavors(self):
        objects = list(self.dcs.service_specifications())
        flavors = []

        for obj in objects:
            flavors.append(obj["flavors"])

        for obj in flavors:
            self.assertIsInstance(obj, list)
            for item in obj:
                self.assertIn("capacity", item.keys())
                self.assertIn("unit", item.keys())
                self.assertIn("available_zones", item.keys())
