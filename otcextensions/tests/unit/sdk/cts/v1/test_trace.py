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

from otcextensions.common import format
from otcextensions.sdk.cts.v1 import trace

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "time": 1534748957969,
    "user": "{some crazy used struct}",
    "code": 302,
    "service_type": "IAM",
    "resource_type": "user",
    "resource_name": "username",
    "resource_id": "some_Resource_id",
    "source_ip": "8.8.8.8",
    "trace_name": "login",
    "trace_rating": "normal",
    "trace_type": "ConsoleAction",
    "record_time": 1534748957990,
    "trace_id": FAKE_ID
}


class TestTrace(base.TestCase):

    def test_basic(self):
        sot = trace.Trace()

        self.assertEqual('/%(tracker_name)s/trace', sot.base_path)

        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = trace.Trace(**EXAMPLE)
        self.assertEqual(EXAMPLE['trace_id'], sot.id)
        self.assertEqual(
            format.TimeTMsStr().deserialize(EXAMPLE['time']),
            sot.time),
        self.assertEqual(EXAMPLE['user'], sot.user)
        self.assertEqual(EXAMPLE['code'], sot.code)
        self.assertEqual(EXAMPLE['service_type'], sot.service_type)
        self.assertEqual(EXAMPLE['resource_type'], sot.resource_type)
        self.assertEqual(EXAMPLE['resource_name'], sot.resource_name)
        self.assertEqual(EXAMPLE['resource_id'], sot.resource_id)
        self.assertEqual(EXAMPLE['source_ip'], sot.source_ip)
        self.assertEqual(EXAMPLE['trace_name'], sot.name)
        self.assertEqual(EXAMPLE['trace_rating'], sot.level)
        self.assertEqual(EXAMPLE['trace_type'], sot.type)
        self.assertEqual(
            format.TimeTMsStr().deserialize(EXAMPLE['record_time']),
            sot.record_time)
