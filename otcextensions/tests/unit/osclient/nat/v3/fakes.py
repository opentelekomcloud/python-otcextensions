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

import mock

from openstackclient.tests.unit import utils

from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.natv3.v3 import gateway


def gen_data(data, columns):
    return tuple(getattr(data, attr, '') for attr in columns)


class TestNat(utils.TestCommand):
    def setUp(self):
        super(TestNat, self).setUp()

        self.app.client_manager.nat = mock.Mock()

        self.client = self.app.client_manager.nat


class FakePrivateNatGateway(test_base.Fake):
    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'spec': 'Small',
            'status': 'ACTIVE',
            'project_id': 'project-' + uuid.uuid4().hex,
            'enterprise_project_id': 'ep-' + uuid.uuid4().hex,
        }

        return gateway.PrivateNatGateway(**object_info)
