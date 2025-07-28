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
from otcextensions.sdk.apig.v2 import error_response

EXAMPLE_DATA = {
    'status': 403,
    'body': '{"error": "Access Denied"}',
    'headers': [{'key': 'Content-Type', 'value': 'application/json'}],
    'ACCESS_DENIED': 'Custom access denied message',
}


class TestErrorResponse(base.TestCase):

    def test_make_it(self):
        sot = error_response.ErrorResponse(**EXAMPLE_DATA)
        self.assertEqual(403, sot.status)
        self.assertEqual('{"error": "Access Denied"}', sot.body)
        self.assertEqual('Custom access denied message', sot.access_denied)
        self.assertEqual(1, len(sot.headers))
        self.assertEqual('Content-Type', sot.headers[0].key)
        self.assertEqual('application/json', sot.headers[0].value)
