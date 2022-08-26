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
import os
import uuid

import fixtures
from openstack import _log
from openstack import exceptions
from openstack import utils

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestAs(base.BaseFunctionalTest):
    TIMEOUT = int(os.environ.get('OS_TEST_TIMEOUT'))
    UUID_V4 = uuid.uuid4().hex[:8]
    AS_GROUP = None
    AS_CONFIG = None
    AS_INSTANCE = None
    MAX_INST_NUMBER = 1
    IMAGE_NAME = "Standard_Debian_10_latest"
    DISK_SIZE = 4
    KP_NAME = None
    AS_GROUP_NAME = None
    network = None
    keypair = None

    def setUp(self):
        test_timeout = 3 * TestAs.TIMEOUT
        try:
            self.useFixture(
                fixtures.EnvironmentVariable(
                    'OS_TEST_TIMEOUT', str(test_timeout)))
        except ValueError:
            pass
        super(TestAs, self).setUp()
        self.client = self.conn.auto_scaling
        self.client_net = self.conn.network

    def create_network(
            self,
            cidr='192.168.0.0/16',
            ip_version=4,
            router_name='sdk-as-test-router-',
            net_name='sdk-as-test-net-',
            subnet_name='sdk-as-test-subnet-',
            kp_name='sdk-as-test-kp-'
    ):
        router_name += TestAs.UUID_V4
        net_name += TestAs.UUID_V4
        subnet_name += TestAs.UUID_V4
        kp_name += TestAs.UUID_V4
        if not TestAs.network:
            network = self.client_net.create_network(name=net_name)
            self.assertEqual(net_name, network.name)
            net_id = network.id
            subnet = self.client_net.create_subnet(
                name=subnet_name,
                ip_version=ip_version,
                network_id=net_id,
                cidr=cidr
            )
            self.assertEqual(subnet_name, subnet.name)
            subnet_id = subnet.id

            router = self.client_net.create_router(name=router_name)
            self.assertEqual(router_name, router.name)
            router_id = router.id
            interface = router.add_interface(
                self.conn.network,
                subnet_id=subnet_id
            )
            self.assertEqual(interface['subnet_id'], subnet_id)
            self.assertIn('port_id', interface)
            TestAs.network = {
                'router_id': router_id,
                'subnet_id': subnet_id,
                'network_id': net_id
            }
            if not TestAs.keypair:
                keypair = self.conn.compute.create_keypair(
                    name=kp_name
                )
                self.assertIsNotNone(keypair)
                TestAs.keypair = keypair
                TestAs.KP_NAME = kp_name
        return

    def destroy_network(self, params: dict, kp_name: str):
        router_id = params.get('router_id')
        subnet_id = params.get('subnet_id')
        network_id = params.get('network_id')

        keypair = self.conn.compute.delete_keypair(keypair=kp_name)
        self.assertIsNone(keypair)
        TestAs.keypair = None

        router = self.client_net.get_router(router_id)
        interface = router.remove_interface(
            self.conn.network,
            subnet_id=subnet_id
        )
        self.assertEqual(interface['subnet_id'], subnet_id)
        self.assertIn('port_id', interface)
        sot = self.client_net.delete_router(
            router_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.client_net.delete_subnet(
            subnet_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.client_net.delete_network(
            network_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)

    def get_image_id(self):
        image = self.conn.compute.find_image(
            name_or_id=self.IMAGE_NAME
        )
        if image:
            return image.id

    def get_default_sec_group(self):
        sec_group = self.client_net.find_security_group(
            name_or_id="default"
        )
        if sec_group:
            return sec_group.id

    def create_as_config(self, config_name='sdk-as-test-config-',
                         disk_vol_type="SATA", flavor="s3.medium.1",
                         disk_type="SYS", disk_size=4):
        if not TestAs.AS_CONFIG:
            config_name += TestAs.UUID_V4

            image_id = self.get_image_id()
            sec_group_id = self.get_default_sec_group()
            config_attrs = {
                "name": config_name,
                "instance_config": {
                    "flavorRef": flavor,
                    "imageRef": image_id,
                    "disk": [{
                        'size': disk_size,
                        'volume_type': disk_vol_type,
                        'disk_type': disk_type
                    }],
                    "key_name": TestAs.KP_NAME,
                    "security_groups": [{
                        "id": sec_group_id
                    }]
                }
            }
            as_config = self.client.create_config(**config_attrs)
            TestAs.AS_CONFIG = as_config

    def delete_as_config(self):
        if TestAs.AS_CONFIG:
            self.client.delete_config(config=TestAs.AS_CONFIG)
            TestAs.AS_CONFIG = None

    def create_as_group(self, group_name='test-as-group-',
                        desire_instances_number=1,
                        min_instances_number=0,
                        max_instances_number=MAX_INST_NUMBER):
        if not TestAs.AS_GROUP:
            group_name += TestAs.UUID_V4
            group_attrs = {
                "scaling_group_name": group_name,
                "scaling_configuration_id": TestAs.AS_CONFIG.id,
                "desire_instance_number": desire_instances_number,
                "min_instance_number": min_instances_number,
                "max_instance_number": max_instances_number,
                "vpc_id": TestAs.network.get('router_id'),
                "networks": [{
                    "id": TestAs.network.get('network_id')
                }]
            }
            as_group = self.client.create_group(**group_attrs)
            self.client.resume_group(as_group)
            as_group = self.client.wait_for_group(as_group)
            TestAs.AS_GROUP = as_group
            TestAs.AS_GROUP_NAME = group_name
            TestAs.MAX_INST_NUMBER = max_instances_number

    def delete_as_group(self, force_delete=False):
        if TestAs.AS_GROUP:
            as_group = TestAs.AS_GROUP
            self.client.pause_group(as_group)
            if not force_delete:
                self.delete_instances(as_group=as_group, timeout=self.TIMEOUT)
            self.client.delete_group(
                group=as_group,
                force_delete=force_delete
            )
            self.client.wait_for_delete_group(
                group=as_group,
                interval=5,
                wait=self.TIMEOUT
            )
            TestAs.AS_GROUP = None

    def delete_instances(self, as_group, timeout):
        try:
            instances = list(self.client.instances(group=as_group))
            if instances:
                for instance in instances:
                    self.client.remove_instance(
                        instance=instance,
                        delete_instance=True
                    )
                    self.client.wait_for_delete_instance(
                        instance=instance, wait=timeout
                    )
                return
        except exceptions.SDKException as e:
            _logger.warning(
                'Got exception during getting as instances %s' % e.message
            )

    def wait_for_instance(self):
        timeout = int(os.environ.get('OS_TEST_TIMEOUT'))
        for count in utils.iterate_timeout(
                timeout=timeout,
                message="Timeout waiting for instance"
        ):
            instances = list(self.client.instances(
                group=TestAs.AS_GROUP
            ))
            if len(instances) == TestAs.MAX_INST_NUMBER and instances[0].id:
                return self.client.wait_for_instance(instances[0])

    def delete_instance(self):
        if TestAs.AS_INSTANCE:
            self.client.remove_instance(
                instance=TestAs.AS_INSTANCE,
                delete_instance=True
            )
            self.client.wait_for_delete_instance(
                instance=TestAs.AS_INSTANCE,
                wait=self.TIMEOUT
            )

    def initialize_as_group_with_instance(self):
        self.create_as_config()
        self.create_as_group()
        TestAs.AS_INSTANCE = self.wait_for_instance()

    def deinitialize_as_group_with_instance(self):
        self.delete_instance()
        self.delete_as_group()
        self.delete_as_config()
