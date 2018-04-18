#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
import datetime
import random
import uuid

import mock

from openstackclient.tests.unit import utils

from otcextensions.sdk.auto_scaling.v1 import activity
from otcextensions.sdk.auto_scaling.v1 import config
from otcextensions.sdk.auto_scaling.v1 import group
from otcextensions.sdk.auto_scaling.v1 import instance
from otcextensions.sdk.auto_scaling.v1 import policy
from otcextensions.sdk.auto_scaling.v1 import quota


class TestAutoScaling(utils.TestCommand):

    def setUp(self):
        super(TestAutoScaling, self).setUp()

        self.app.client_manager.auto_scaling = mock.Mock()


class Fake(object):

    @classmethod
    def create_one(cls, attrs=None):
        """Create a fake resource.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param Dictionary methods:
            A dictionary with all methods
        :return:
            A FakeResource object, with id, name, metadata, and so on
        """
        attrs = attrs or {}

        resource = cls.generate()
        # new_attrs = cls.generate()

        resource.update(attrs)

        return resource

    @classmethod
    def create_multiple(cls, count=2, attrs=None):
        """Create multiple fake resources.

        :param Dictionary attrs:
            A dictionary with all attributes
        :param int count:
            The number of address scopes to fake
        :return:
            A list of FakeResource objects faking the address scopes
        """
        objects = []
        for i in range(0, count):
            objects.append(
                cls.create_one(attrs))

        return objects


class FakeGroup(Fake):
    """Fake one or more Group"""

    @classmethod
    def generate(cls):
        object_info = {
            'create_time': datetime.datetime(
                random.randint(2000, 2020),
                random.randint(1, 12),
                random.randint(1, 28)
            ),
            'name': 'group-' + uuid.uuid4().hex,
            'id': 'id-' + uuid.uuid4().hex,
            'status': 'SOME STATUS',
            'detail': 'detail-' + uuid.uuid4().hex,
            'network_id': 'id-vpc-' + uuid.uuid4().hex,
        }
        obj = group.Group.existing(**object_info)
        return obj


class FakeConfig(Fake):
    """Fake one or more AS Config"""

    @classmethod
    def generate(cls):
        object_info = {
            'create_time': datetime.datetime(
                random.randint(2000, 2020),
                random.randint(1, 12),
                random.randint(1, 28)
            ),
            'name': 'name-' + uuid.uuid4().hex,
            'id': 'id-' + uuid.uuid4().hex,
            'instance_config': {
                'instance_id': 'inst_id-' + uuid.uuid4().hex,
                'instance_name': 'inst-name-' + uuid.uuid4().hex,
                'flavor_id': 'flavor-' + uuid.uuid4().hex,
                'image_id': 'image-' + uuid.uuid4().hex,
                'disk': [
                    {
                        'size': random.randint(1, 200),
                        'volume_type': 'SSD',
                        'disk_type': 'SYS'
                    }
                ],
                'public_ip': None,
                'user_data': None,
                'metadata': {},
            }
        }
        obj = config.Config.existing(**object_info)
        return obj


class FakePolicy(Fake):
    """Fake one or more AS Policy"""

    @classmethod
    def generate(cls):
        object_info = {
            'create_time': datetime.datetime(
                random.randint(2000, 2020),
                random.randint(1, 12),
                random.randint(1, 28)
            ),
            'name': 'name-' + uuid.uuid4().hex,
            'id': 'id-' + uuid.uuid4().hex,
            'type': 'type-' + uuid.uuid4().hex,
            'scaling_group_id': 'sgid-' + uuid.uuid4().hex,
            'alarm_id': 'alarmid-' + uuid.uuid4().hex,
            'cool_down_time': random.randint(1, 10000),
            'status': 'status-' + uuid.uuid4().hex,
            'scheduled_policy': {
                'launch_time': 'launch_time-' + uuid.uuid4().hex,
                'recurrence_type': 'recurrence_type-' + uuid.uuid4().hex,
                'recurrence_value': 'recurrence_value-' + uuid.uuid4().hex,
                'start_time': 'start_time-' + uuid.uuid4().hex,
                'end_time': 'end_time-' + uuid.uuid4().hex,
            },
            'scaling_policy_action': {
                'operation': 'operation-' + uuid.uuid4().hex,
                'instance_number': random.randint(1, 100),
            }
        }
        obj = policy.Policy.existing(**object_info)
        return obj


class FakeActivity(Fake):
    """Fake one or more AS Activity"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'start_time': 'st-' + uuid.uuid4().hex,
            'end_time': 'et-' + uuid.uuid4().hex,
            'description': 'description-' + uuid.uuid4().hex,
            'status': 'status-' + uuid.uuid4().hex,
            'scaling_value': 'sv-' + uuid.uuid4().hex,
            'instance_value': random.randint(1, 10000),
            'desire_value': random.randint(1, 10000),
        }
        obj = activity.Activity.existing(**object_info)
        return obj


class FakeInstance(Fake):
    """Fake one or more AS Instance"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'scaling_group_name': 'sgn-' + uuid.uuid4().hex,
            'scaling_configuration_id': 'sci-' + uuid.uuid4().hex,
            'scaling_configuration_name': 'scn-' + uuid.uuid4().hex,
            'lifecycle_state': 'ls-' + uuid.uuid4().hex,
            'health_status': 'hs-' + uuid.uuid4().hex,
            'create_time': datetime.datetime(
                random.randint(2000, 2020),
                random.randint(1, 12),
                random.randint(1, 28)
            ),
        }
        obj = instance.Instance.existing(**object_info)
        return obj


class FakeQuota(Fake):
    """Fake one or more AS Quota"""

    @classmethod
    def generate(cls):
        object_info = {
            'type': 'id-' + uuid.uuid4().hex,
            'used': random.randint(1, 10000),
            'quota': random.randint(1, 10000),
            'max': random.randint(1, 10000),
        }
        obj = quota.Quota.existing(**object_info)
        return obj
