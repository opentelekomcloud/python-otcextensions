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
    "specification": "modelarts.vm.gpu.v100",
    "billing_spec": "modelarts.vm.gpu.v100",
    "is_open": True,
    "spec_status": "normal",
    "is_free": False,
    "over_quota": False,
    "extend_params": 1,
}


class TestSpecification(base.TestCase):
    def setUp(self):
        super(TestSpecification, self).setUp()

    def test_basic(self):
        sot = service.Specification()

        self.assertEqual("/services/specifications", sot.base_path)
        self.assertEqual("specifications", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual(
            {
                "is_personal_cluster": "is_personal_cluster",
                "infer_type": "infer_type",
                "limit": "limit",
                "marker": "marker",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        updated_sot_attrs = ()
        sot = service.Specification(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
