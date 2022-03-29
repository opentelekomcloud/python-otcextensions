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
import random
import uuid

import mock

from otcextensions.sdk.sdrs.v1 import active_domains
from otcextensions.tests.unit.osclient import test_base


class TestSDRS(test_base.TestCommand):

    def setUp(self):
        super(TestSDRS, self).setUp()

        self.app.client_manager.sdrs = mock.Mock()
        self.client = self.app.client_manager.sdrs


class FakeActiveDomain(test_base.Fake):
    """Fake one or more SDRS Active-active domains"""

    @classmethod
    def generate(cls):
        object_info = {
            'domains': [{
                'id': 'id-' + uuid.uuid4().hex,
                'name': 'name-' + uuid.uuid4().hex,
                'description': 'description-' + uuid.uuid4().hex,
                'sold_out': random.choice([True, False]),
                'local_replication_cluster': {
                    'availability_zone': random.choice(['eu-de-01',
                                                        'eu-de-02',
                                                        'eu-de-03'])
                },
                'remote_replication_cluster': {
                    'availability_zone': random.choice(['eu-de-01',
                                                        'eu-de-02',
                                                        'eu-de-03'])
                }
            }]
        }

        obj = active_domains.ActiveDomains.existing(**object_info)
        return obj
