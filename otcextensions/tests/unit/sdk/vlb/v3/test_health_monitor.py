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

from openstack.tests.unit import base

from otcextensions.sdk.vlb.v3 import health_monitor

EXAMPLE = {
    'type': 'type',
    'timeout': 60,
    'delay': 5,
    'max_retries': 3,
    'admin_state_up': True,
    'monitor_port': 80,
}


class TestLoadBalancer(base.TestCase):

    def test_basic(self):
        sot = health_monitor.HealthMonitor()
        path = '/elb/healthmonitors'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = health_monitor.HealthMonitor(**EXAMPLE)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['delay'], sot.delay)
        self.assertEqual(EXAMPLE['max_retries'], sot.max_retries)
        self.assertEqual(EXAMPLE['monitor_port'], sot.monitor_port)
