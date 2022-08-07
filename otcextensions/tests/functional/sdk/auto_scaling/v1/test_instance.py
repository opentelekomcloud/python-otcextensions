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

    TIMEOUT = int(os.environ.get('OS_TEST_TIMEOUT'))
    UUID = uuid.uuid4().hex[:9]
    AS_GROUP_NAME = "test-as-group-" + UUID
    AS_CONFIG_NAME = "test-as-config-" + UUID
    AS_GROUP = None
    AS_CONFIG = None
    AS_INSTANCE = None
    DESIRE_INSTANCE_NUMBER = 1
    MIN_INSTANCE_NUMBER = 0
    MAX_INSTANCE_NUMBER = 1
    FLAVOR = "s3.medium.1"
    IMAGE_NAME = "Standard_Ubuntu_18.04_latest"
    DISK_SIZE = 4
    DISK_VOL_TYPE = "SATA"
    DISK_TYPE = "SYS"

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

    def _create_as_config(self):
        if not TestInstance.AS_CONFIG:
            image_id = self._get_image_id()
            sec_group_id = self._get_default_sec_group()
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
            as_config = self.conn.auto_scaling.create_config(**config_attrs)
            TestInstance.AS_CONFIG = as_config

    def _delete_as_config(self):
        if TestInstance.AS_CONFIG:
            self.conn.auto_scaling.delete_config(config=TestInstance.AS_CONFIG)
            TestInstance.AS_CONFIG = None

    def _create_as_group(self):
        if not TestInstance.AS_GROUP:
            group_attrs = {
                "scaling_group_name": self.AS_GROUP_NAME,
                "scaling_configuration_id": TestInstance.AS_CONFIG.id,
                "desire_instance_number": self.DESIRE_INSTANCE_NUMBER,
                "min_instance_number": self.MIN_INSTANCE_NUMBER,
                "max_instance_number": self.MAX_INSTANCE_NUMBER,
                "vpc_id": TestInstance.NETWORK.get('router_id'),
                "networks": [{
                    "id": TestInstance.NETWORK.get('network_id')
                }]
            }
            as_group = self.conn.auto_scaling.create_group(**group_attrs)
            self.conn.auto_scaling.resume_group(as_group)
            as_group = self.conn.auto_scaling.wait_for_group(as_group)
            TestInstance.AS_GROUP = as_group

    def _delete_as_group(self, force_delete=False):
        if TestInstance.AS_GROUP:
            as_group = TestInstance.AS_GROUP
            self.conn.auto_scaling.pause_group(as_group)
            if not force_delete:
                self._delete_instances(as_group=as_group, timeout=self.TIMEOUT)
            self.conn.auto_scaling.delete_group(
                group=as_group,
                force_delete=force_delete
            )
            self.conn.auto_scaling.wait_for_delete_group(
                group=as_group,
                interval=5,
                wait=self.TIMEOUT
            )
            TestInstance.AS_GROUP = None

    def _delete_instances(self, as_group, timeout):
        try:
            instances = list(self.conn.auto_scaling.instances(group=as_group))
            if instances:
                for instance in instances:
                    self.conn.auto_scaling.remove_instance(
                        instance=instance,
                        delete_instance=True
                    )
                    self.conn.auto_scaling.wait_for_delete_instance(
                        instance=instance, wait=timeout
                    )
                return
        except exceptions.SDKException as e:
            _logger.warning(
                'Got exception during getting as instances %s' % e.message
            )

    def _wait_for_instance(self):
        as_group = TestInstance.AS_GROUP
        for count in utils.iterate_timeout(
                timeout=self.TIMEOUT,
                message="Timeout waiting for instance"
        ):
            instances = list(self.conn.auto_scaling.instances(
                group=as_group
            ))
            if len(instances) == self.MAX_INSTANCE_NUMBER and instances[0].id:
                TestInstance.AS_INSTANCE =\
                    self.conn.auto_scaling.wait_for_instance(instances[0])

    def _delete_instance(self):
        if TestInstance.AS_INSTANCE:
            self.conn.auto_scaling.remove_instance(
                instance=TestInstance.AS_INSTANCE,
                delete_instance=True
            )
            self.conn.auto_scaling.wait_for_delete_instance(
                instance=TestInstance.AS_INSTANCE,
                wait=self.TIMEOUT
            )

    def _initialize_as_group_with_instance(self):
        self._create_as_config()
        self._create_as_group()
        # self._wait_for_instance()

    def _deinitialize_as_group_with_instance(self):
        self._delete_instance()
        self._delete_as_group()
        self._delete_as_config()

    def test_01_create_as_group(self):
        as_group = self.conn.auto_scaling.find_group(
            name_or_id=self.AS_GROUP_NAME)
        self.assertIsNotNone(as_group)
        self.assertEqual(as_group.name, self.AS_GROUP_NAME)

    def test_02_simple_delete_as_group(self):
        self._delete_as_group()
        as_group = self.conn.auto_scaling.find_group(
            name_or_id=self.AS_GROUP_NAME)
        self.assertIsNone(as_group)

    def test_03_list_as_groups(self):
        as_group_list = list(self.conn.auto_scaling.groups())
        self.assertIsNotNone(as_group_list)

    def test_04_update_as_group(self):
        new_name = self.AS_GROUP_NAME + "_new"
        as_group = self.conn.auto_scaling.update_group(
            group=TestInstance.AS_GROUP, name=new_name)
        self.assertIsNotNone(as_group)
        self.assertEqual(as_group.name, new_name)

    def test_05_find_as_group(self):
        find_as_group = self.conn.auto_scaling.find_group(
            name_or_id=self.AS_GROUP_NAME
        )
        self.assertEqual(TestInstance.AS_GROUP.id, find_as_group.id)
        self.assertEqual(TestInstance.AS_GROUP.name, find_as_group.name)

    # def test_06_find_instance_by_id(self):
    #     result = self.conn.auto_scaling.find_instance(
    #         name_or_id=TestInstance.AS_INSTANCE.id,
    #         group=TestInstance.AS_GROUP.id
    #     )
    #     self.assertIsNotNone(result)
    #     self.assertEqual(TestInstance.AS_INSTANCE.id, result.id)
    #
    # def test_07_find_instance_by_name(self):
    #     result = self.conn.auto_scaling.find_instance(
    #         name_or_id=TestInstance.AS_GROUP.name,
    #         group=TestInstance.AS_GROUP.id
    #     )
    #     self.assertIsNotNone(result)
    #     self.assertEqual(TestInstance.AS_INSTANCE.name, result.name)
