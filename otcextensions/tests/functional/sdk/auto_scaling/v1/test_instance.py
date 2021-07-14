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

from openstack import exceptions
from openstack import _log
from openstack import utils

from otcextensions.tests.functional.sdk.auto_scaling.v1 import base

_logger = _log.setup_logging('openstack')


class TestInstance(base.BaseASTest):

    UUID = uuid.uuid4().hex[:9]
    AS_GROUP_NAME = "test-as-group-" + UUID
    AS_CONFIG_NAME = "test-as-config-" + UUID
    DESIRE_INSTANCE_NUMBER = 1
    MIN_INSTANCE_NUMBER = 0
    MAX_INSTANCE_NUMBER = 1
    FLAVOR = "s3.medium.1"
    IMAGE_NAME = "Standard_Ubuntu_18.04_latest"
    DISK_SIZE = 4
    DISK_VOL_TYPE = "SATA"
    DISK_TYPE = "SYS"

    def _get_image_id(self):
        image = self.conn.compute.find_image(
            name_or_id=self.IMAGE_NAME
        )
        if image:
            return image.id

    def _get_default_sec_group(self):
        sec_group = self.conn.network.find_security_group(
            name_or_id="default"
        )
        if sec_group:
            return sec_group.id

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
        timeout = 2 * int(os.environ.get('OS_TEST_TIMEOUT'))
        self.conn.auto_scaling.pause_group(as_group)
        self.conn.auto_scaling.delete_group(
            group=as_group
        )
        self.conn.auto_scaling.wait_for_delete_group(
            group=as_group, wait=timeout)

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

    def _delete_instance(self, instance):
        timeout = 2 * int(os.environ.get('OS_TEST_TIMEOUT'))
        self.conn.auto_scaling.remove_instance(
            instance=instance,
            delete_instance=True
        )
        self.conn.auto_scaling.wait_for_delete_instance(
            instance=instance,
            wait=timeout
        )

    def _initialize_as_group_with_instance(self):
        self.as_config = self._create_as_config(
            self._get_image_id(), self._get_default_sec_group()
        )
        self.as_group = self._create_as_group(
            self.as_config.id, self.infra.get("router_id"),
            self.infra.get("network_id")
        )
        self.as_instance = self._wait_for_instance(
            self.as_group
        )

    def _deinitialize_as_group_with_instance(self):
        if self.as_instance:
            self._delete_instance(self.as_instance)
        if self.as_group:
            self._delete_as_group(self.as_group)
        if self.as_config:
            self._delete_as_config(self.as_config)

    def setUp(self):
        super(TestInstance, self).setUp()
        self._initialize_as_group_with_instance()

    def tearDown(self):
        try:
            self._deinitialize_as_group_with_instance()
        except exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)
        super(TestInstance, self).tearDown()

    def test_find_instance_by_id(self):
        result = self.conn.auto_scaling.find_instance(
            name_or_id=self.as_instance.id,
            group=self.as_group
        )
        self.assertIsNotNone(result)
        self.assertEqual(self.as_instance.id, result.id)

    def test_find_instance_by_name(self):
        result = self.conn.auto_scaling.find_instance(
            name_or_id=self.as_instance.name,
            group=self.as_group
        )
        self.assertIsNotNone(result)
        self.assertEqual(self.as_instance.name, result.name)
