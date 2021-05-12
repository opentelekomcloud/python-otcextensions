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
import os

import fixtures
import openstack

from openstack import utils
from openstack import _log

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestInstance(base.BaseFunctionalTest):
    UUID = uuid.uuid4().hex[:9]
    NETWORK_NAME = "test-network-" + UUID
    SUBNET_NAME = "test-subnet-" + UUID
    ROUTER_NAME = "test-router-" + UUID
    AS_GROUP_NAME = "test-as-group-" + UUID
    AS_CONFIG_NAME = "test-as-config-" + UUID
    SG_NAME = "test-sec-group-" + UUID
    KP_NAME = "test-kp-" + UUID
    IP_VERSION = 4
    CIDR = "192.168.0.0/16"
    DESIRE_INSTANCE_NUMBER = 1
    MIN_INSTANCE_NUMBER = 0
    MAX_INSTANCE_NUMBER = 1
    FLAVOR = "s3.medium.1"
    IMAGE_NAME = "Standard_Ubuntu_18.04_latest"
    DISK_SIZE = 4
    DISK_VOL_TYPE = "SATA"
    DISK_TYPE = "SYS"

    def _create_keypair(self):
        return self.conn.compute.create_keypair(
            name=self.KP_NAME
        )

    def _delete_keypair(self, key_pair):
        return self.conn.compute.delete_keypair(
            keypair=key_pair
        )

    def _create_sec_group(self):
        return self.conn.network.create_security_group(
            name=self.SG_NAME
        )

    def _delete_sec_group(self, sec_group):
        return self.conn.network.delete_security_group(
            security_group=sec_group
        )

    def _create_network(self):
        return self.conn.network.create_network(
            name=self.NETWORK_NAME
        )

    def _delete_network(self, network):
        return self.conn.network.delete_network(
            network=network
        )

    def _create_subnet(self, network_id):
        return self.conn.network.create_subnet(
            name=self.SUBNET_NAME,
            network_id=network_id,
            ip_version=self.IP_VERSION,
            cidr=self.CIDR
        )

    def _delete_subnet(self, subnet):
        return self.conn.network.delete_subnet(
            subnet=subnet
        )

    def _create_router(self, subnet_id):
        rtr = self.conn.network.create_router(
            name=self.ROUTER_NAME
        )
        return self.conn.network.add_interface_to_router(
            router=rtr,
            subnet_id=subnet_id
        )

    def _delete_router(self, router, subnet_id):
        self.conn.network.remove_interface_from_router(
            router=router,
            subnet_id=subnet_id
        )
        return self.conn.network.delete_router(
            router=router
        )

    def _get_image_id(self):
        image = self.conn.compute.find_image(
            name_or_id=self.IMAGE_NAME
        )
        if image:
            return image.id

    def _create_as_config(self, image_id, sec_group_id):
        config_attrs = {
            "name": self.AS_CONFIG_NAME,
            "instance_config": {
                "flavorRef": self.FLAVOR,
                "imageRef": image_id,
                "disk": [{
                    'size': self.DISK_SIZE,
                    'volume_type': self.DISK_VOL_TYPE,
                    'disk_type': self.DISK_TYPE
                }],
                "key_name": self.KP_NAME,
                "security_groups": [{
                    "id": sec_group_id
                }]
            }
        }
        return self.conn.auto_scaling.create_config(**config_attrs)

    def _delete_as_config(self, as_config):
        return self.conn.auto_scaling.delete_config(
            config=as_config
        )

    def _create_as_group(self, as_config_id, router_id, network_id):
        group_attrs = {
            "scaling_group_name": self.AS_GROUP_NAME,
            "scaling_configuration_id": as_config_id,
            "desire_instance_number": self.DESIRE_INSTANCE_NUMBER,
            "min_instance_number": self.MIN_INSTANCE_NUMBER,
            "max_instance_number": self.MAX_INSTANCE_NUMBER,
            "vpc_id": router_id,
            "networks": [{
                "id": network_id
            }]
        }
        as_group = self.conn.auto_scaling.create_group(**group_attrs)
        self.conn.auto_scaling.resume_group(as_group)
        return self.conn.auto_scaling.wait_for_group(as_group)

    def _delete_as_group(self, as_group):
        self.conn.auto_scaling.pause_group(as_group)
        self.conn.auto_scaling.delete_group(
            group=as_group
        )
        self.conn.auto_scaling.wait_for_delete_group(as_group)

    def _wait_for_instance(self, as_group):
        timeout = int(os.environ.get('OS_TEST_TIMEOUT'))
        for count in utils.iterate_timeout(
                timeout=timeout,
                message="Timeout waiting for instance"
        ):
            instances = list(self.conn.auto_scaling.instances(
                group=as_group
            ))
            if len(instances) == self.MAX_INSTANCE_NUMBER and instances[0].id:
                return self.conn.auto_scaling.wait_for_instance(instances[0])

    def _delete_instance(self, instance, as_group):
        timeout = int(os.environ.get('OS_TEST_TIMEOUT'))
        self.conn.auto_scaling.remove_instance(
            instance=instance,
            delete_instance=True
        )
        self.conn.auto_scaling.wait_for_delete_instance(
            instance=instance,
            wait=timeout
        )

    def _initialize_as_group_with_instance(self):
        self.key_pair = self._create_keypair()
        self.sec_group = self._create_sec_group()
        self.network = self._create_network()
        self.subnet = self._create_subnet(self.network.id)
        self.router = self._create_router(self.subnet.id)
        self.as_config = self._create_as_config(
            self._get_image_id(), self.sec_group.id
        )
        self.as_group = self._create_as_group(
            self.as_config.id, self.router['id'], self.network.id
        )
        self.instance = self._wait_for_instance(
            self.as_group
        )

    def _deinitialize_as_group_with_instance(self):
        if self.instance:
            self._delete_instance(self.instance, self.as_group)
        if self.as_group:
            self._delete_as_group(self.as_group)
        if self.as_config:
            self._delete_as_config(self.as_config)
        if self.router:
            self._delete_router(self.router, self.subnet.id)
        if self.subnet:
            self._delete_subnet(self.subnet)
        if self.network:
            self._delete_network(self.network)
        if self.sec_group:
            self._delete_sec_group(self.sec_group)
        if self.key_pair:
            self._delete_keypair(self.key_pair)

    def setUp(self):
        test_timeout = 3 * int(os.environ.get('OS_TEST_TIMEOUT'))
        try:
            self.useFixture(
                fixtures.EnvironmentVariable(
                    'OS_TEST_TIMEOUT', str(test_timeout)))
        except ValueError:
            pass
        super(TestInstance, self).setUp()
        self._initialize_as_group_with_instance()

    def tearDown(self):
        super(TestInstance, self).tearDown()
        try:
            self._deinitialize_as_group_with_instance()
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_find_instance_by_id(self):
        result = self.conn.auto_scaling.find_instance(
            name_or_id=self.instance.id,
            group=self.as_group
        )
        self.assertIsNotNone(result)
        self.assertEqual(self.instance.id, result.id)

    def test_find_instance_by_name(self):
        result = self.conn.auto_scaling.find_instance(
            name_or_id=self.instance.name,
            group=self.as_group
        )
        self.assertIsNotNone(result)
        self.assertEqual(self.instance.name, result.name)
