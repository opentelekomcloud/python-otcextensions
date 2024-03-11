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
from otcextensions.sdk.modelartsv1.v1 import job_flavor
from otcextensions.tests.unit.sdk.modelartsv1.v1 import examples
from otcextensions.tests.unit.utils import assert_attributes_equal

EXAMPLE = examples.JOB_FLAVOR


class TestJobFlavor(base.TestCase):
    def setUp(self):
        super(TestJobFlavor, self).setUp()

    def test_basic(self):
        sot = job_flavor.JobFlavor()

        self.assertEqual("/job/resource-specs", sot.base_path)
        self.assertEqual("specs", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_patch)

    def test_make_it(self):
        sot = job_flavor.JobFlavor(**EXAMPLE)
        assert_attributes_equal(self, sot, EXAMPLE)
