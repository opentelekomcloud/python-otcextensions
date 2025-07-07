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
from otcextensions.sdk.apig.v2 import metric_data

EXAMPLE_METRIC = {
    'average': 123,
    'max': 200,
    'min': 100,
    'sum': 1234,
    'variance': 12,
    'timestamp': '2025-01-01T12:00:00Z',
    'unit': 'ms'
}

EXAMPLE_RESPONSE = {
    'datapoints': [EXAMPLE_METRIC]
}


class TestMetricData(base.TestCase):

    def test_basic(self):
        sot = metric_data.MetricData()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/metric-data',
            sot.base_path
        )
        self.assertEqual('datapoints', sot.resources_key)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = metric_data.MetricData(**EXAMPLE_METRIC)
        self.assertEqual(123, sot.average)
        self.assertEqual(200, sot.max)
        self.assertEqual(100, sot.min)
        self.assertEqual(1234, sot.sum)
        self.assertEqual(12, sot.variance)
        self.assertEqual('2025-01-01T12:00:00Z', sot.timestamp)
        self.assertEqual('ms', sot.unit)
