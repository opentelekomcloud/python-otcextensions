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

class TestGroup(base.BaseASTest):

    UUID = uuid.uuid4().hex[:9]
    AS_GROUP_NAME = "test-as-group-" + UUID
    AS_CONFIG_NAME = "test-as-config-" + UUID
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

    def _create_as_group(self, router_id, network_id, min_instance_number=0,
                         max_instance_number=1, desire_instance_number=0,
                         as_config=None):
        group_attrs = {
            "scaling_group_name": self.AS_GROUP_NAME,
            "min_instance_number": min_instance_number,
            "desire_instance_number": desire_instance_number,
            "max_instance_number": max_instance_number,
            "vpc_id": router_id,
            "networks": [{
                "id": network_id
            }]
        }
        if as_config:
            group_attrs["scaling_configuration_id"] = as_config.id
        as_group = self.conn.auto_scaling.create_group(**group_attrs)
        if as_config:
            self.conn.auto_scaling.resume_group(as_group)
        return as_group

    def _delete_as_group(self, as_group, force_delete=False):
        self.conn.auto_scaling.delete_group(
            group=as_group,
            force_delete=force_delete
        )
        return self.conn.auto_scaling.wait_for_delete_group(as_group)

    def _wait_for_instances(self, as_group, desire_instance_number=0):
        timeout = int(os.environ.get('OS_TEST_TIMEOUT'))
        for count in utils.iterate_timeout(
                timeout=timeout,
                message="Timeout waiting for instance"
        ):
            instances = list(self.conn.auto_scaling.instances(
                group=as_group
            ))
            if (len(instances) == desire_instance_number and
                    [instance.id for instance in instances if instance.id]):
                for instance in instances:
                    self.conn.auto_scaling.wait_for_instance(instance)
                return

    def _delete_instance(self, instance):
        timeout = int(os.environ.get('OS_TEST_TIMEOUT'))
        self.conn.auto_scaling.remove_instance(
            instance=instance,
            delete_instance=True
        )
        self.conn.auto_scaling.wait_for_delete_instance(
            instance=instance,
            wait=timeout
        )

    def _delete_instances(self, as_group):
        instances = list(self.conn.auto_scaling.instances(
            group=as_group
        ))
        for instance in instances:
            self._delete_instance(instance)

    def _deinitialize_as_group(self):
        if self.as_group:
            instances = list(self.conn.auto_scaling.instances(
                group=self.as_group)
            )
            force_delete = False
            if len(instances) > 0:
                force_delete = True
            self._delete_as_group(self.as_group, force_delete)
        if self.as_config:
            self._delete_as_config(self.as_config)

    def setUp(self):
        super(TestGroup, self).setUp()

    def tearDown(self):
        try:
            self._deinitialize_as_group()
        except exceptions.SDKException as e:
            _logger.warning('Got exception during clearing '
                                         'resources %s'
                            % e.message)
        finally:
            super(TestGroup, self).tearDown()

    #def test_01_create_as_group(self):
    #    router = self.conn.network.get_router(self.infra.get("router_id"))
    #    network = self.conn.network.get_network(self.infra.get("network_id"))
    #    self.as_group = self._create_as_group(router.id, network.id)
    #    self.assertIsNotNone(self.as_group)
    #    self.assertEqual(self.as_group.name, self.AS_GROUP_NAME)

    def test_02_create_as_group_with_instance(self):
        self.as_config = self._create_as_config(self._get_image_id(),
                                                self.infra.get(
                                                    "sec_group_id"
                                                ))
        self.as_group = self._create_as_group(router_id=self.infra.get("router_id"),
                                              network_id=self.infra.get("network_id"),
                                              min_instance_number=0,
                                              desire_instance_number=1,
                                              max_instance_number=1,
                                              as_config=self.as_config)
        self.conn.auto_scaling.resume_group(self.as_group)
        self._wait_for_instances(self.as_group, desire_instance_number=1)
        self.assertIsNotNone(self.as_group)
        self.assertEqual(self.as_group.name, self.AS_GROUP_NAME)
