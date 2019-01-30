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

from otcextensions.sdk.deh.v1 import host_type


FAKE_ID = '68d5745e-6af2-40e4-945d-fe449be00148'
EXAMPLE = {
    'host_type': 'general',
    'host_type_name': 'general computing'
}


class TestHost(base.TestCase):

    def test_basic(self):
        sot = host_type.HostType()

        self.assertEqual('/availability-zone/%(availability_zone)s/'
                         'dedicated-host-types',
                         sot.base_path)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_update)

    def test_make_it(self):

        sot = host_type.HostType(**EXAMPLE)
        self.assertEqual(EXAMPLE['host_type'], sot.host_type)
        self.assertEqual(EXAMPLE['host_type_name'], sot.host_type_name)
