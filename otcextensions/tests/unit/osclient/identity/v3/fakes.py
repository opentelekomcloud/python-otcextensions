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

from otcextensions.sdk.identity.v3 import credential
from otcextensions.tests.unit.osclient import test_base


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestIdentity(utils.TestCommand):
    def setUp(self):
        super(TestIdentity, self).setUp()

        self.app.client_manager.iam = mock.Mock()

        self.client = self.app.client_manager.iam


class FakeIdentityCredential(test_base.Fake):
    """Fake one or more identity credentials."""
    @classmethod
    def generate(cls):
        """Create a fake identity credential.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.

        access = "id-" + uuid.uuid4().hex

        object_info = {
            "access": access,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "description": "my credential",
            "status": "active",
            "user_id": "user-id-" + uuid.uuid4().hex,
        }

        return credential.Credential(**object_info)
