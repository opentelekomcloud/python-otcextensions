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
from otcextensions.sdk.modelartsv1.v1 import service_cluster

EXAMPLE = {
    "cluster_id": "cluster-uuid",
    "cluster_name": "pool-a1cf",
    "tenant": "tenant-uuid",
    "project": "project-uuid",
    "owner": "owner-uuid",
    "created_at": 1658743383618,
    "status": "running",
    "allocatable_cpu_cores": 7.06,
    "allocatable_memory": 27307.0,
    "allocatable_gpus": 0.0,
    "charging_mode": "postpaid",
    "max_node_count": 50,
    "nodes": {
        "specification": "modelarts.vm.cpu.8ud",
        "count": 1,
        "available_count": 1,
    },
    "services_count": {"realtime_count": 0, "batch_count": 0},
}


class TestServiceCluster(base.TestCase):
    def setUp(self):
        super(TestServiceCluster, self).setUp()

    def test_basic(self):
        sot = service_cluster.ServiceCluster()

        self.assertEqual("/clusters", sot.base_path)
        self.assertEqual("clusters", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual(
            {
                "project_id": "project_id",
                "name": "name",
                "cluster_name": "name",
                "status": "status",
                "marker": "marker",
                "offset": "marker",
                "limit": "limit",
                "sort_by": "sort_by",
                "order": "order",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = service_cluster.ServiceCluster(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key != "nodes":
                self.assertEqual(getattr(sot, key), value)

        sot_nodes = service_cluster.NodeSpec(**EXAMPLE["nodes"])
        for key, value in EXAMPLE["nodes"].items():
            self.assertEqual(getattr(sot_nodes, key), value)
