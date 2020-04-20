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
# import datetime
import random
import uuid
import time

import mock

from openstackclient.tests.unit import utils
from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.cts.v1 import trace
from otcextensions.sdk.cts.v1 import tracker


class TestCTS(utils.TestCommand):

    def setUp(self):
        super(TestCTS, self).setUp()

        self.app.client_manager.cts = mock.Mock()
        self.client = self.app.client_manager.cts

        self.client.traces = mock.Mock()


class FakeTrace(test_base.Fake):
    """Fake one or more Trace"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': uuid.uuid4().hex,
            'level': uuid.uuid4().hex,
            'type': uuid.uuid4().hex,
            'time': time.clock() * 1000,
            'user': uuid.uuid4().hex,
            'code': random.randint(1, 600),
            'service_type': uuid.uuid4().hex,
            'resource_type': uuid.uuid4().hex,
            'resource_name': uuid.uuid4().hex,
            'resource_id': uuid.uuid4().hex,
            'source_ip': uuid.uuid4().hex,
            'record_time': time.clock() * 1000,
            'request': uuid.uuid4().hex,
            'response': uuid.uuid4().hex,
        }
        obj = trace.Trace.existing(**object_info)
        return obj


class FakeTracker(test_base.Fake):
    """Fake one or more Tracker"""

    @classmethod
    def generate(cls):
        object_info = {
            'name': uuid.uuid4().hex,
            'bucket_name': uuid.uuid4().hex,
            'file_prefix_name': uuid.uuid4().hex,
            'status': uuid.uuid4().hex,
            'details': uuid.uuid4().hex,
            'smn': {
                'enabled': True,
                'topic_id': uuid.uuid4().hex,
                'is_send_all_key_operation': True,
                'need_notify_user_list': [uuid.uuid4().hex, uuid.uuid4().hex],
                'operations': [uuid.uuid4().hex, uuid.uuid4().hex]
            }
        }
        obj = tracker.Tracker.existing(**object_info)
        return obj
