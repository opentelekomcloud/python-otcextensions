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
from otcextensions.sdk.modelartsv1.v1 import service_log

EXAMPLE = {
    "config": [
        {
            "model_id": "f565ac47-6239-4e8c-b2dc-0665dc52e302",
            "model_name": "model-demo",
            "model_version": "0.0.1",
            "specification": "modelarts.vm.cpu.2u",
            "custom_spec": {},
            "weight": 100,
            "instance_count": 1,
            "scaling": False,
            "envs": {},
            "cluster_id": "2c9080f86d37da64016d381fe5940002",
        }
    ],
    "extend_config": [],
    "update_time": 1586250930708,
    "result": "RUNNING",
    "cluster_id": "2c9080f86d37da64016d381fe5940002",
}


class TestLog(base.TestCase):
    def setUp(self):
        super(TestLog, self).setUp()

    def test_basic(self):
        sot = service_log.ServiceLog()

        self.assertEqual("/services/%(serviceId)s/logs", sot.base_path)
        self.assertEqual("logs", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual(
            {
                "update_time": "update_time",
                "limit": "limit",
                "marker": "marker",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = service_log.ServiceLog(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key != "config":
                self.assertEqual(getattr(sot, key), value)

        for config in EXAMPLE["config"]:
            sot_config = service_log.ConfigSpec(**config)
            for key, value in config.items():
                if key == "custom_spec":
                    self.assertEqual(
                        sot.config[0].custom_spec, sot_config.custom_spec
                    )
                else:
                    self.assertEqual(getattr(sot_config, key), value)
