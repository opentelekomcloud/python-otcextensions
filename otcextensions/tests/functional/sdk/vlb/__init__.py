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
    additional_listener = None
    pool = None
    member = None
    health_monitor = None
    certificate = None
    l7policy = None
    server = None
    keypair = None

    _private_key = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDFPN9ojPndxSC4E1pqWQVKGHCFlXAAGBOxbGfSzXqzsoyacotu
eqMqXQbxrPSQFATeVmhZPNVEMdvcAMjYsV/mymtAwVqVA6q/OFdX/b3UHO+b/VqL
o3J5SrM86Veqnjzwu4oCSabuEDiN+tga1syQmEG4OFM6NSmAYSxcZdE6LwIDAQAB
AoGBAJvLzJCyIsCJcKHWL6onbSUtDtyFwPViD1QrVAtQYabF14g8CGUZG/9fgheu
TXPtTDcvu7cZdUArvgYW3I9F9IBb2lmF3a44xfiAKdDhzr4DK/vQhvHPuuTeZA41
r2zp8Cu+Bp40pSxmoAOK3B0/peZAka01Ju7c7ZChDWrxleHZAkEA/6dcaWHotfGS
eW5YLbSms3f0m0GH38nRl7oxyCW6yMIDkFHURVMBKW1OhrcuGo8u0nTMi5IH9gRg
5bH8XcujlQJBAMWBQgzCHyoSeryD3TFieXIFzgDBw6Ve5hyMjUtjvgdVKoxRPvpO
kclc39QHP6Dm2wrXXHEej+9RILxBZCVQNbMCQQC42i+Ut0nHvPuXN/UkXzomDHde
h1ySsOAO4H+8Y6OSI87l3HUrByCQ7stX1z3L0HofjHqV9Koy9emGTFLZEzSdAkB7
Ei6cUKKmztkYe3rr+RcATEmwAw3tEJOHmrW5ErApVZKr2TzLMQZ7WZpIPzQRCYnY
2ZZLDuZWFFG3vW+wKKktAkAaQ5GNzbwkRLpXF1FZFuNF7erxypzstbUmU/31b7tS
i5LmxTGKL/xRYtZEHjya4Ikkkgt40q1MrUsgIYbFYMf2
-----END RSA PRIVATE KEY-----"""

    _certificate = """-----BEGIN CERTIFICATE-----
MIIDIjCCAougAwIBAgIJALV96mEtVF4EMA0GCSqGSIb3DQEBBQUAMGoxCzAJBgNV
BAYTAnh4MQswCQYDVQQIEwJ4eDELMAkGA1UEBxMCeHgxCzAJBgNVBAoTAnh4MQsw
CQYDVQQLEwJ4eDELMAkGA1UEAxMCeHgxGjAYBgkqhkiG9w0BCQEWC3h4eEAxNjMu
Y29tMB4XDTE3MTExMzAyMjYxM1oXDTIwMTExMjAyMjYxM1owajELMAkGA1UEBhMC
eHgxCzAJBgNVBAgTAnh4MQswCQYDVQQHEwJ4eDELMAkGA1UEChMCeHgxCzAJBgNV
BAsTAnh4MQswCQYDVQQDEwJ4eDEaMBgGCSqGSIb3DQEJARYLeHh4QDE2My5jb20w
gZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMU832iM+d3FILgTWmpZBUoYcIWV
cAAYE7FsZ9LNerOyjJpyi256oypdBvGs9JAUBN5WaFk81UQx29wAyNixX+bKa0DB
WpUDqr84V1f9vdQc75v9WoujcnlKszzpV6qePPC7igJJpu4QOI362BrWzJCYQbg4
Uzo1KYBhLFxl0TovAgMBAAGjgc8wgcwwHQYDVR0OBBYEFMbTvDyvE2KsRy9zPq/J
WOjovG+WMIGcBgNVHSMEgZQwgZGAFMbTvDyvE2KsRy9zPq/JWOjovG+WoW6kbDBq
MQswCQYDVQQGEwJ4eDELMAkGA1UECBMCeHgxCzAJBgNVBAcTAnh4MQswCQYDVQQK
EwJ4eDELMAkGA1UECxMCeHgxCzAJBgNVBAMTAnh4MRowGAYJKoZIhvcNAQkBFgt4
eHhAMTYzLmNvbYIJALV96mEtVF4EMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEF
BQADgYEAASkC/1iwiALa2RU3YCxqZFEEsZZvQxikrDkDbFeoa6Tk49Fnb1f7FCW6
PTtY3HPWl5ygsMsSy0Fi3xp3jmuIwzJhcQ3tcK5gC99HWp6Kw37RL8WoB8GWFU0Q
4tHLOjBIxkZROPRhH+zMIrqUexv6fsb3NWKhnlfh1Mj5wQE4Ldo=
-----END CERTIFICATE-----"""

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
            additional=False,
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
        if additional and not TestVlb.additional_listener:
            TestVlb.additional_listener = self.client.create_listener(**attrs)

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

    def create_certificate(
            self,
            private_key=_private_key,
            certificate=_certificate,
            name='sdk-vlb-test-cert-' + uuid_v4,
            **kwargs
    ):
        if not TestVlb.certificate:
            TestVlb.certificate = self.client.create_certificate(
                private_key=private_key,
                certificate=certificate,
                name=name,
                **kwargs
            )

    def create_l7policy(
            self,
            redirect_listener_id,
            action='REDIRECT_TO_LISTENER',
            name='sdk-vlb-test-l7p-' + uuid_v4,
            **kwargs
    ):
        attrs = {
            'action': action,
            'name': name,
            'redirect_listener_id': redirect_listener_id,
            **kwargs
        }
        if not TestVlb.listener:
            raise exceptions.SDKException
        attrs['listener_id'] = TestVlb.listener.id
        if TestVlb.listener and not TestVlb.l7policy:
            TestVlb.l7policy = self.client.create_l7_policy(**attrs)

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
