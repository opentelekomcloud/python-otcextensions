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
from otcextensions.tests.unit.sdk.modelartsv1.v1 import examples
from otcextensions.tests.unit.utils import assert_attributes_equal

EXAMPLE = examples.SERVICE


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
        sot = service.Service(**EXAMPLE)
        assert_attributes_equal(self, sot, EXAMPLE)

    def test_create_sot(self):
        sot = service.Service(**EXAMPLE_CREATE)
        assert_attributes_equal(self, sot, EXAMPLE_CREATE)
