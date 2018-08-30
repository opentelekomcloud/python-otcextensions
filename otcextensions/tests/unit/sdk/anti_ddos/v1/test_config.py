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

from otcextensions.sdk.anti_ddos.v1 import config

EXAMPLE = {
    "traffic_limited_list": [
        {
            "traffic_pos_id": 1,
            "traffic_per_second": 10,
            "packet_per_second": 2000
        }
    ],
    "http_limited_list": [
        {
            "http_request_pos_id": 1,
            "http_packet_per_second": 100
        }
    ],
    "connection_limited_list": [
        {
            "cleaning_access_pos_id": 1,
            "new_connection_limited": 10,
            "total_connection_limited": 30
        }
    ],
    "extend_ddos_config": [
        {
            "new_connection_limited": 80,
            "total_connection_limited": 700,
            "http_packet_per_second": 500000,
            "traffic_per_second": 1000,
            "packet_per_second": 200000,
            "setID": 33
        },
    ]

}


class TestConfig(base.TestCase):

    def setUp(self):
        super(TestConfig, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = config.Config()

        self.assertEqual('/antiddos/query_config_list', sot.base_path)

        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = config.Config(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['traffic_limited_list'],
            sot.traffic_limited_list)
        self.assertEqual(
            EXAMPLE['http_limited_list'],
            sot.http_limited_list)
        self.assertEqual(
            EXAMPLE['connection_limited_list'],
            sot.connection_limited_list)
        self.assertEqual(
            EXAMPLE['extend_ddos_config'],
            sot.extend_ddos_config)
