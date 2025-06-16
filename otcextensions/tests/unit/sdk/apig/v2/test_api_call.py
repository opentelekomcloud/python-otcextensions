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
from otcextensions.sdk.apig.v2 import api_call

EXAMPLE_STAT = {
    'max_latency': 500,
    'avg_latency': 123.45,
    'req_count': 1000,
    'req_count_2xx': 800,
    'req_count_4xx': 150,
    'req_count_5xx': 50,
    'req_count_error': 200,
    'max_inner_latency': 300,
    'avg_inner_latency': 120.5,
    'max_backend_latency': 450,
    'avg_backend_latency': 200.0,
    'output_throughput': 1.23,
    'input_throughput': 0.89,
    'current_minute': 5,
    'cycle': '5m',
    'api_id': 'api-123',
    'group_id': 'group-456',
    'provider': 'custom',
    'req_time': '2025-01-01T12:00:00Z',
    'register_time': '2025-01-01T11:00:00Z',
    'status': 1
}

EXAMPLE_RESULT = {
    'code': '200',
    'msg': 'OK',
    'start_time': '2025-01-01T12:00:00Z',
    'end_time': '2025-01-01T12:05:00Z',
    'list': [EXAMPLE_STAT]
}


class TestApiCallResult(base.TestCase):

    def test_basic(self):
        sot = api_call.ApiCallResult()
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = api_call.ApiCallResult(**EXAMPLE_RESULT)
        self.assertEqual('200', sot.code)
        self.assertEqual('OK', sot.msg)
        self.assertEqual('2025-01-01T12:00:00Z', sot.start_time)
        self.assertEqual(1, len(sot.api_list))
        stat = sot.api_list[0]
        self.assertEqual(500, stat.max_latency)
        self.assertEqual('api-123', stat.api_id)
        self.assertEqual('group-456', stat.group_id)
