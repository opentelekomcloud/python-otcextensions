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

import mock
import copy
from unittest.mock import MagicMock

from osc_lib import utils as _osc_lib_utils

from openstackclient.tests.unit import utils
from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.modelartsv1.v1 import devenv
from otcextensions.sdk.modelartsv1.v1 import model
from otcextensions.tests.unit.sdk.modelartsv1.v1 import examples


def gen_data(obj, columns, formatters=None):
    """Fill expected data tuple based on columns list
    """
    return _osc_lib_utils.get_item_properties(
        obj, columns, formatters=formatters
    )


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestModelarts(utils.TestCommand):
    def setUp(self):
        super(TestModelarts, self).setUp()

        self.app.client_manager.modelartsv1 = mock.Mock()

        self.client = self.app.client_manager.modelartsv1


class FakeDevenv(test_base.Fake):
    """Fake one or more Modelarts devenv."""
    @classmethod
    def generate(cls):
        """Create a fake Modelarts devenv.

        :return:
            A FakeResource object, with id, name and so on
        """
        return devenv.Devenv(**examples.EXAMPLE_DEVENV)


class FakeModel(test_base.Fake):
    """Fake one or more Modelarts model."""
    @classmethod
    def generate(cls):
        """Create a fake Modelarts model.

        :return:
            A FakeResource object, with id, name and so on
        """
        EXAMPLE2 = copy.deepcopy(examples.EXAMPLE_MODEL)
        sot = model.Model()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = EXAMPLE2
        sot._translate_response(mock_response)

        return sot  # model.Model(**examples.EXAMPLE_MODEL)
