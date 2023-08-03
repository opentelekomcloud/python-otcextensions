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
    'delay': 5,
    'domain_name': 'domain-name',
    'expected_codes': 'expected-codes',
    'http_method': 'http_method',
    'admin_state_up': True,
    'max_retries': 5,
    'max_retries_down': 5,
    'monitor_port': 80,
    'pool_id': 'pool-id',
    'pools': [{'id': 'uuid1'}, {'id': 'uuid2'}],
    'project_id': 'project-id',
    'timeout': 20,
    'type': 'type',
    'url_path': 'url-path',
    'created_at': 'created-at',
    'updated_at': 'updated-at',
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
        self.assertEqual(EXAMPLE['delay'], sot.delay)
        self.assertEqual(EXAMPLE['domain_name'], sot.domain_name)
        self.assertEqual(EXAMPLE['expected_codes'], sot.expected_codes)
        self.assertEqual(EXAMPLE['http_method'], sot.http_method)
        self.assertEqual(EXAMPLE['admin_state_up'], sot.is_admin_state_up)
        self.assertEqual(EXAMPLE['max_retries'], sot.max_retries)
        self.assertEqual(EXAMPLE['max_retries_down'], sot.max_retries_down)
        self.assertEqual(EXAMPLE['monitor_port'], sot.monitor_port)
        self.assertEqual(EXAMPLE['pool_id'], sot.pool_id)
        self.assertEqual(EXAMPLE['pools'], sot.pools)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['timeout'], sot.timeout)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['url_path'], sot.url_path)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
