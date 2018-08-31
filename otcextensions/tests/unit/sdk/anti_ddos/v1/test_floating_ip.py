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
import mock

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.anti_ddos.v1 import floating_ip

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "enable_L7": False,
    "traffic_pos_id": 2,
    "http_request_pos_id": 1,
    "cleaning_access_pos_id": 1,
    "app_type_id": 1,
    "floating_ip_id": FAKE_ID
}


class TestFloatingIP(base.TestCase):

    def setUp(self):
        super(TestFloatingIP, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = floating_ip.FloatingIP()

        self.assertEqual('/antiddos', sot.base_path)
        self.assertEqual('ddosStatus', sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_update)

    def test_make_it(self):

        sot = floating_ip.FloatingIP(**EXAMPLE)
        self.assertEqual(EXAMPLE['floating_ip_id'], sot.id)
        self.assertEqual(EXAMPLE['enable_L7'], sot.is_enable_l7)
        self.assertEqual(EXAMPLE['traffic_pos_id'], sot.traffic_pos_id)
        self.assertEqual(
            EXAMPLE['http_request_pos_id'],
            sot.http_request_pos_id)
        self.assertEqual(
            EXAMPLE['cleaning_access_pos_id'],
            sot.cleaning_access_pos_id)
        self.assertEqual(
            EXAMPLE['app_type_id'],
            sot.app_type_id)
