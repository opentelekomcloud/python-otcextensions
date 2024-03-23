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
from otcextensions.sdk.modelartsv1.v1 import builtin_model
from otcextensions.tests.unit.sdk.modelartsv1.v1 import examples
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = examples.BUILT_IN_MODEL


class TestBuiltInModel(base.TestCase):
    def setUp(self):
        super(TestBuiltInModel, self).setUp()

    def test_basic(self):
        sot = builtin_model.BuiltInModel()

        self.assertEqual("/built-in-algorithms", sot.base_path)
        self.assertEqual("models", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_patch)

    def test_make_it(self):
        sot = builtin_model.BuiltInModel(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key == "create_time":
                self.assertEqual(sot.created_at, EXAMPLE[key])
            else:
                assert_attributes_equal(self, getattr(sot, key), value)
