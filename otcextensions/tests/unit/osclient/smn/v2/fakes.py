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
#
import uuid
from datetime import datetime

import mock

from openstackclient.tests.unit import utils

from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.smn.v2 import topic
from otcextensions.sdk.smn.v2 import template
from otcextensions.sdk.smn.v2 import subscription


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestSmn(utils.TestCommand):
    def setUp(self):
        super(TestSmn, self).setUp()

        self.app.client_manager.smn = mock.Mock()

        self.client = self.app.client_manager.smn


class FakeTopic(test_base.Fake):
    """Fake one or more Topics."""
    @classmethod
    def generate(cls):
        """Create a fake Topic..

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "push_policy": 0,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "name": "name-" + uuid.uuid4().hex,
            "topic_urn": "id-" + uuid.uuid4().hex,
            "display_name": "display-name-" + uuid.uuid4().hex,
            "request_id": "request-" + uuid.uuid4().hex
        }

        return topic.Topic(**object_info)


class FakeTemplate(test_base.Fake):
    """Fake one or more Templates."""
    @classmethod
    def generate(cls):
        """Create a fake Templates.

        :return:
            A FakeResource object, with id, status and so on
        """
        # Set default attributes.
        object_info = {
            "message_template_id": "id-" + uuid.uuid4().hex,
            "message_template_name": "name-" + uuid.uuid4().hex,
            "protocol": "https",
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "request_id": "request-" + uuid.uuid4().hex,
            "tag_names": [
                "topic_id_id4"
            ],
            "content": "Test Content"
        }

        return template.Template.existing(**object_info)


class FakeSubscription(test_base.Fake):
    """Fake one or more subscriptions"""
    @classmethod
    def generate(cls):
        """Create a fake subscription.

        :return:
            A FakeResource object, with id, status and so on
        """
        # Set default attributes.
        object_info = {
            "topic_urn": "topic-id" + uuid.uuid4().hex,
            "protocol": "sms",
            "subscription_urn": "id-" + uuid.uuid4().hex,
            "owner": "owner-" + uuid.uuid4().hex,
            "endpoint": "xxxxxxxxxx",
            "remark": "",
            "status": 0
        }

        obj = subscription.Subscription.existing(**object_info)
        return obj
