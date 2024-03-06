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
    "access_address": "https://access_address",
    "additional_properties": {},
    "config": [
        {
            "model_id": "model-uuid",
            "model_name": "model-name",
            "model_version": "0.0.1",
            "source_type": "auto",
            "specification": "modelarts.vm.high.p3",
            "custom_spec": {},
            "status": "ready",
            "weight": 100,
            "instance_count": 1,
            "scaling": False,
            "envs": {},
            "additional_properties": {},
            "support_debug": False,
        }
    ],
    "description": "Created by Exeml project(name: exeML-aqi).",
    "failed_times": 3,
    "infer_type": "real-time",
    "invocation_times": 5,
    "is_free": False,
    "is_shared": False,
    "operation_time": 1705621491068,
    "owner": "owner-uuid",
    "progress": 100,
    "project": "project-uuid",
    "publish_at": 1691908601470,
    "service_id": "service-uuid",
    "service_name": "exeML-aqi_ExeML_1691908601350529540",
    "shared_count": 0,
    "status": "running",
    "tenant": "tenant-uuid",
    "transition_at": 1696333731658,
    "update_time": 1691908601470,
    "workspace_id": "0",
}

EXAMPLE_CREATE = {
    "config": [
        {
            "model_id": "xxxmodel-idxxx",
            "weight": 70,
            "specification": "modelarts.vm.cpu.2u",
            "instance_count": 1,
            "envs": {"model_name": "mxnet-model-1", "load_epoch": "0"},
        },
        {
            "model_id": "xxxxxx",
            "weight": 30,
            "specification": "modelarts.vm.cpu.2u",
            "instance_count": 1,
        },
    ],
    "description": "mnist service",
    "infer_type": "real-time",
    "service_name": "mnist",
}


class TestService(base.TestCase):
    def setUp(self):
        super(TestService, self).setUp()

    def test_basic(self):
        sot = service.Service()

        self.assertEqual("/services", sot.base_path)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual("services", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)
        self.assertDictEqual(
            {
                "limit": "limit",
                "marker": "marker",
                "cluster_id": "cluster_id",
                "infer_type": "infer_type",
                "model_id": "model_id",
                "name": "service_name",
                "offset": "offset",
                "order": "order",
                "service_id": "service_id",
                "sort_by": "sort_by",
                "status": "status",
                "workspace_id": "workspace_id",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        updated_sot_attrs = ("config",)
        sot = service.Service(**EXAMPLE)
        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

        config_spec = EXAMPLE["config"][0]
        sot_config = service.ConfigSpec(**config_spec)
        for key, value in config_spec.items():
            if key != "custom_spec":
                self.assertEqual(getattr(sot_config, key), value)

        custom_spec = EXAMPLE["config"][0]["custom_spec"]
        sot_custom_spec = service.CustomSpec(**custom_spec)
        for key, value in custom_spec.items():
            self.assertEqual(getattr(sot_custom_spec, key), value)

    def test_create_sot(self):
        sot = service.Service(**EXAMPLE_CREATE)

        for key, value in EXAMPLE_CREATE.items():
            if key != "config":
                self.assertEqual(getattr(sot, key), value)

        for config in EXAMPLE_CREATE["config"]:
            sot_config = service.ConfigSpec(**config)
            for key, value in config.items():
                if key != "custom_spec":
                    self.assertEqual(getattr(sot_config, key), value)
