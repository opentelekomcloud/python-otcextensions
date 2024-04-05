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
from otcextensions.sdk.vpcep.v1 import quota
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = {
    'type': 'endpoint',
    'quota': 150,
    'used': 14,
}


class TestQuota(base.TestCase):
    def setUp(self):
        super(TestQuota, self).setUp()

    def test_basic(self):
        sot = quota.Quota()
        self.assertEqual(None, sot.resources_key)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('/quotas', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

        self.assertDictEqual(
            {
                'limit': 'limit',
                'marker': 'marker',
                'type': 'type',
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = quota.Quota(**EXAMPLE)
        assert_attributes_equal(self, sot, EXAMPLE)
