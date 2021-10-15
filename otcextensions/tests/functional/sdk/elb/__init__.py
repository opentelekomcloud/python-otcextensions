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

from openstack import exceptions

from otcextensions.tests.functional import base


class TestElb(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    network = None
    load_balancer = None
    listener = None

    def setUp(self):
        super(TestElb, self).setUp()
        self.client = self.conn.elb
        self.network_client = self.conn.network

    def create_load_balancer(
            self,
            name='sdk-elb-test-lb-' + uuid_v4,
            description='test',
            **kwargs
    ):
        attrs = {
            'name': name,
            'description': description,
            'vip_subnet_id': TestElb.network['subnet_id'],
            **kwargs
        }
        if TestElb.network and not TestElb.load_balancer:
            TestElb.load_balancer = self.client.create_load_balancer(**attrs)

    def create_listener(
            self,
            name='sdk-vlb-test-lis-' + uuid_v4,
            protocol_port=80,
            protocol='TCP',
            **kwargs
    ):
        attrs = {
            'protocol_port': protocol_port,
            'protocol': protocol,
            'name': name,
            **kwargs
        }
        if not TestElb.load_balancer:
            raise exceptions.SDKException
        attrs['loadbalancer_id'] = TestElb.load_balancer.id
        if TestElb.network and TestElb.load_balancer \
                and not TestElb.listener:
            TestElb.listener = self.client.create_listener(**attrs)

    def create_network(
            self,
            cidr='192.168.0.0/16',
            ip_version=4,
            router_name='sdk-elb-test-router-',
            net_name='sdk-elb-test-net-',
            subnet_name='sdk-elb-test-subnet-'
    ):
        uuid_v4 = uuid.uuid4().hex[:8]
        router_name += uuid_v4
        net_name += uuid_v4
        subnet_name += uuid_v4
        if not TestElb.network:
            network = self.conn.network.create_network(name=net_name)
            self.assertEqual(net_name, network.name)
            net_id = network.id
            subnet = self.conn.network.create_subnet(
                name=subnet_name,
                ip_version=ip_version,
                network_id=net_id,
                cidr=cidr
            )
            self.assertEqual(subnet_name, subnet.name)
            subnet_id = subnet.id

            router = self.conn.network.create_router(name=router_name)
            self.assertEqual(router_name, router.name)
            router_id = router.id
            interface = router.add_interface(
                self.conn.network,
                subnet_id=subnet_id
            )
            self.assertEqual(interface['subnet_id'], subnet_id)
            self.assertIn('port_id', interface)
            TestElb.network = {
                'router_id': router_id,
                'subnet_id': subnet_id,
                'network_id': net_id
            }
        return

    def destroy_network(self, params: dict):
        router_id = params.get('router_id')
        subnet_id = params.get('subnet_id')
        network_id = params.get('network_id')
        router = self.conn.network.get_router(router_id)

        interface = router.remove_interface(
            self.conn.network,
            subnet_id=subnet_id
        )
        self.assertEqual(interface['subnet_id'], subnet_id)
        self.assertIn('port_id', interface)
        sot = self.conn.network.delete_router(
            router_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.conn.network.delete_subnet(
            subnet_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.conn.network.delete_network(
            network_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        self.network = None
