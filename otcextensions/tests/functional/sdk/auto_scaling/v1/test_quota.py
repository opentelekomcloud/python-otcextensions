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

from otcextensions.tests.functional.sdk.auto_scaling.v1 import base

_logger = _log.setup_logging('openstack')


class TestQuota(base.TestAs):

    def setUp(self):
        super(TestQuota, self).setUp()
        self.auto_scaling = self.conn.auto_scaling

    def test_list(self):
        expected_types = ['scaling_Group', 'scaling_Config',
                          'scaling_Policy', 'scaling_Instance',
                          'bandwidth_scaling_policy']
        objects = list(self.auto_scaling.quotas())

        self.assertEqual(len(objects), 5)
        types = []

        for obj in objects:
            types.append(obj.get('type'))
            self.assertIsInstance(obj, dict)
            self.assertIn('type', obj.keys())
            self.assertIn('used', obj.keys())
            self.assertIn('max', obj.keys())
            self.assertIn('quota', obj.keys())

        self.assertListEqual(types, expected_types)
