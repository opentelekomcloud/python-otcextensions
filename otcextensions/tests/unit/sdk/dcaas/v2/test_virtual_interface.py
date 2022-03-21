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

from otcextensions.sdk.dcaas.v2 import virtual_interface


EXAMPLE = {
    "name": "test-vi",
    "tenant_id": "6fbe9263116a4b68818cf1edce16bc4f",
    "description": "Virtual interface description",
    "direct_connect_id": "456e9263116a4b68818cf1edce16bc4f",
    "vgw_id": "56d5745e-6af2-40e4-945d-fe449be00148",
    "type": "public",
    "service_type": "vpc",
    "vlan": 100,
    "bandwidth": 10,
    "local_gateway_v4_ip": "180.1.1.1/24",
    "remote_gateway_v4_ip": "180.1.1.2/24",
    "route_mode": "static",
    "bgp_asn": 5,
    "bgp_md5": "",
    "remote_ep_group_id": "8ube9263116a4b68818cf1edce16bc4f",
    "service_ep_group_id": "6fbe9263116a4b68818cf1edce16bc4f",
    "create_time": "2016-01-28T16:14:09.466Z",
    "delete_time": "2016-01-28T16:25:27.690Z",
    "admin_state_up": True,
    "rate_limit": False,
    "status": "PENDING_CREATE"
}


class TestVirtualInterface(base.TestCase):

    def setUp(self):
        super(TestVirtualInterface, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = virtual_interface.VirtualInterface()
        self.assertEqual('virtual_interface', sot.resource_key)
        self.assertEqual('virtual_interfaces', sot.resources_key)
        self.assertEqual('/dcaas/virtual-interfaces', sot.base_path)

        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):

        sot = virtual_interface.VirtualInterface(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['tenant_id'], sot.project_id)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['direct_connect_id'], sot.direct_connect_id)
        self.assertEqual(EXAMPLE['vgw_id'], sot.vgw_id)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['service_type'], sot.service_type)
        self.assertEqual(EXAMPLE['vlan'], sot.vlan)
        self.assertEqual(EXAMPLE['bandwidth'], sot.bandwidth)
        self.assertEqual(EXAMPLE['local_gateway_v4_ip'],
                         sot.local_gateway_v4_ip)
        self.assertEqual(EXAMPLE['remote_gateway_v4_ip'],
                         sot.remote_gateway_v4_ip)
        self.assertEqual(EXAMPLE['route_mode'], sot.route_mode)
        self.assertEqual(EXAMPLE['bgp_asn'], sot.bgp_asn)
        self.assertEqual(EXAMPLE['bgp_md5'], sot.bgp_md5)
        self.assertEqual(EXAMPLE['remote_ep_group_id'],
                         sot.remote_ep_group_id)
        self.assertEqual(EXAMPLE['service_ep_group_id'],
                         sot.service_ep_group_id)
        self.assertEqual(EXAMPLE['create_time'], sot.create_time)
        self.assertEqual(EXAMPLE['delete_time'], sot.delete_time)
        self.assertEqual(EXAMPLE['admin_state_up'],
                         sot.admin_state_up)
        self.assertEqual(EXAMPLE['rate_limit'], sot.rate_limit)
        self.assertEqual(EXAMPLE['status'], sot.status)
