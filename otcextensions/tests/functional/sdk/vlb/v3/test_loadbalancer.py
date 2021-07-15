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
import uuid

from otcextensions.tests.functional.sdk.vlb import TestVlb


class TestLoadbalancer(TestVlb):
    uuid_v4 = uuid.uuid4().hex[:8]
    az = 'eu-nl-01'
    network_id = '1391c40a-8ab3-4249-96e4-cede1b3145cd'
    vpc_id = '7cbf60cd-0300-498e-bb6a-3e25e7631e20'
    subnet_id = 'dcedcde7-347d-4b04-bce8-4b926b6ca034'

    lb_attrs = {
        "name": "test-lbv3",
        "description": "testing1",
        "admin_state_up": True,
        "publicip": {
            "network_type": "5_bgp",
            "billing_info": "",
            "bandwidth": {
                "size": 2,
                "share_type": "PER",
                "charge_mode": "traffic",
                "name": "elbv3_eip_traffic"
            }
        },
        "tags": [
            {
                "key": "test",
                "value": "api"
            }
        ],
        "l7_flavor_id": "d39af422-1fa5-48d8-bd41-8457716564ab",
        "vip_subnet_cidr_id": subnet_id,
        "vpc_id": vpc_id,
        "guaranteed": True,
        "availability_zone_list": [az],
        "provider": "vlb",
        "elb_virsubnet_ids": [network_id]
    }

    lb_attrs_eip = {
        "vpc_id": vpc_id,
        "availability_zone_list": [az],
        "admin_state_up": True,
        "vip_subnet_cidr_id": subnet_id,
        "elb_virsubnet_ids": [network_id],
        "name": "elb-ipv4-public",
        "publicip": {
            "network_type": "5_bgp",
            "bandwidth": {
                "size": 2,
                "share_type": "PER",
                "charge_mode": "traffic",
                "name": "elb_eip_traffic"
            }
        }
    }


    def setUp(self):
        super(TestLoadbalancer, self).setUp()

        # self.vlb_name = 'sdk-vlb-test-lb-' + self.uuid_v4
        # self.vlb = self.client.create_load_balancer(
        #     name=self.vlb_name
        # )
        #
        # self.addCleanup(self.conn.vlb.delete_load_balancer, self.vlb)


    def test_create_loadbalancer(self):
        # neutron_subnet_id = self.net_client.subnets()
        elb = self.client.create_load_balancer(**self.lb_attrs_eip)
        self.assertIsNotNone(elb)
