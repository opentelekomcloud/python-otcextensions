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

from otcextensions.sdk.dns.v2 import nameserver


FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "priority": 1,
    "address": "fake.ip",
    "hostname": "fake.hostname",
}


class TestNS(base.TestCase):

    def test_basic(self):
        sot = nameserver.NameServer()

        self.assertEqual('/zones/%(zone_id)s/nameservers', sot.base_path)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_update)

    def test_make_it(self):

        sot = nameserver.NameServer(**EXAMPLE)
        self.assertEqual(EXAMPLE['priority'], sot.priority)
        self.assertEqual(EXAMPLE['address'], sot.address)
        self.assertEqual(EXAMPLE['hostname'], sot.hostname)
