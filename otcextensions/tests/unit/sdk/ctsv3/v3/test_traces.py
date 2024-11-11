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
from otcextensions.sdk.ctsv3.v3 import trace

EXAMPLE = {
    "time": 1472148708232,
    "user": {
        "name": "xxx",
        "domain": {
            "name": "xxx",
            "id": "ded649d814464428ba89d04d7955c93e"
      }
    },
    "response": {
        "code": "VPC.0514",
        "message": "Update port fail."
    },
    "code": 200,
    "service_type": "VPC",
    "resource_type": "eip",
    "resource_name": "192.144.163.1",
    "resource_id": "d502809d-0d1d-41ce-9690-784282142ccc",
    "trace_name": "deleteEip",
    "trace_rating": "warning",
    "trace_type": "ConsoleAction",
    "api_version": "2.0",
    "record_time": 1481066128032,
    "trace_id": "e001ccb9-bc09-11e6-b00b-4b2a61338db6"
}


class TestTrace(base.TestCase):
    def test_basic(self):
        sot = trace.Trace()
        self.assertEqual('/traces', sot.base_path)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = trace.Trace(**EXAMPLE)
        self.assertEqual(EXAMPLE['time'], sot.time)
        self.assertEqual(EXAMPLE['user']['name'], sot.user.name)
