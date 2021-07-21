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


class TestVlb(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    network = None
    load_balancer = None
    listener = None
    pool = None
    member = None
    health_monitor = None
    server = None
    keypair = None

    def setUp(self):
        super(TestVlb, self).setUp()
        self.client = self.conn.vlb
        self.net_client = self.conn.network
        self.ecs_client = self.conn.compute

    def create_load_balancer(
            self,
            az_list=None,
            publicip: dict = None,
            tags: list = None,
            name='sdk-vlb-test-lb-' + uuid_v4,
            description='test',
            admin_state_up=True,
            guaranteed=True,
            provider='vlb',
            ip_target_enable=True,
            **kwargs
    ):
        attrs = {
            'name': name,
            'description': description,
            'vip_subnet_cidr_id': TestVlb.network['subnet_id'],
            'vpc_id': TestVlb.network['router_id'],
            'elb_virsubnet_ids': [TestVlb.network['network_id']],
            'admin_state_up': admin_state_up,
            'guaranteed': guaranteed,
            'provider': provider,
            'availability_zone_list': az_list,
            'publicip': publicip,
            'ip_target_enable': ip_target_enable,
            'tags': tags,
            **kwargs
        }
        if not az_list:
            attrs['availability_zone_list'] = ['eu-nl-01']
        if not publicip:
            attrs['publicip'] = {
                "network_type": "5_bgp",
                "billing_info": "",
                "bandwidth": {
                    "size": 2,
                    "share_type": "PER",
                    "charge_mode": "traffic",
                    "name": "elbv3_eip_traffic"
                }
            }
        if not tags:
            attrs['tags'] = [{
                "key": "test",
                "value": "api"
            }]
        if TestVlb.network and not TestVlb.load_balancer:
            TestVlb.load_balancer = self.client.create_load_balancer(**attrs)

    def create_listener(
            self,
            admin_state_up=True,
            insert_headers: dict = None,
            name='sdk-vlb-test-lis-' + uuid_v4,
            protocol_port=80,
            protocol='TCP',
            tags: list = None,
            **kwargs
    ):
        attrs = {
            'protocol_port': protocol_port,
            'protocol': protocol,
            'insert_headers': insert_headers,
            'name': name,
            'admin_state_up': admin_state_up,
            'tags': tags,
            **kwargs
        }
        if not TestVlb.load_balancer:
            raise exceptions.SDKException
        attrs['loadbalancer_id'] = TestVlb.load_balancer.id
        if not insert_headers:
            attrs['insert_headers']: {'X-Forwarded-ELB-IP': True}
        if not tags:
            attrs['tags'] = [{
                "key": "test",
                "value": "api"
            }]
        if TestVlb.network and TestVlb.load_balancer \
                and not TestVlb.listener:
            TestVlb.listener = self.client.create_listener(**attrs)

    def create_pool(
            self,
            admin_state_up=True,
            description='Test',
            lb_algorithm='ROUND_ROBIN',
            name='sdk-vlb-test-pool-' + uuid_v4,
            protocol='TCP',
            **kwargs
    ):
        attrs = {
            'name': name,
            'description': description,
            'lb_algorithm': lb_algorithm,
            'protocol': protocol,
            'admin_state_up': admin_state_up,
            **kwargs
        }
        if not TestVlb.listener:
            raise exceptions.SDKException
        attrs['listener_id'] = TestVlb.listener.id
        if not TestVlb.load_balancer:
            raise exceptions.SDKException
        attrs['loadbalancer_id'] = TestVlb.load_balancer.id
        if TestVlb.network and TestVlb.listener and not TestVlb.pool:
            TestVlb.pool = self.client.create_pool(**attrs)

    def create_member(
            self,
            name='sdk-vlb-test-member-' + uuid_v4,
            protocol_port=8080,
            **kwargs
    ):
        attrs = {
            'protocol_port': protocol_port,
            'name': name,
            'address': TestVlb.server.addresses[self.network_name][0]['addr'],
            **kwargs
        }
        if TestVlb.pool and not TestVlb.member:
            TestVlb.member = self.client.create_member(
                TestVlb.pool, **attrs)

    def create_health_monitor(
            self,
            type='TCP',
            timeout=3,
            delay=5,
            max_retries=3,
            admin_state_up=True,
            monitor_port=8080,
            **kwargs
    ):
        attrs = {
            'type': type,
            'timeout': timeout,
            'delay': delay,
            'max_retries': max_retries,
            'admin_state_up': admin_state_up,
            'monitor_port': monitor_port,
            **kwargs
        }
        if not TestVlb.pool:
            raise exceptions.SDKException
        attrs['pool_id'] = TestVlb.pool.id
        if TestVlb.pool and not TestVlb.health_monitor:
            TestVlb.health_monitor = self.client.create_health_monitor(**attrs)

    def create_server(
            self,
            name='sdk-vlb-test-ecs-' + uuid_v4,
            kp_name='sdk-vlb-test-kp-' + uuid_v4,
            image_name='Standard_Fedora_34_latest',
            flavor_name='s3.medium.1'
    ):

        image = self.ecs_client.find_image(image_name)
        flavor = self.ecs_client.find_flavor(flavor_name)
        self.network_name = self.net_client.find_network(
            TestVlb.network['network_id']
        ).name

        if not TestVlb.keypair:
            TestVlb.keypair = self.ecs_client.create_keypair(name=kp_name)

        if not TestVlb.server:
            server = self.ecs_client.create_server(
                name=name,
                image_id=image.id,
                flavor_id=flavor.id,
                networks=[{"uuid": TestVlb.network['network_id']}],
                key_name=TestVlb.keypair.name
            )

            TestVlb.server = self.ecs_client.wait_for_server(server)

    def create_network(
            self,
            cidr='192.168.0.0/16',
            ip_version=4,
            router_name='sdk-vlb-test-router-',
            net_name='sdk-vlb-test-net-',
            subnet_name='sdk-vlb-test-subnet-'
    ):
        uuid_v4 = uuid.uuid4().hex[:8]
        router_name += uuid_v4
        net_name += uuid_v4
        subnet_name += uuid_v4
        if not TestVlb.network:
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
            TestVlb.network = {
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

    def delete_server(self):
        sot = self.ecs_client.delete_server(TestVlb.server.id)
        self.assertIsNone(sot)
        self.ecs_client.wait_for_delete(TestVlb.server)
