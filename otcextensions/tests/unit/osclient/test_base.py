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
#
from cliff import columns as cliff_columns

from openstackclient.tests.unit import utils


class TestCommand(utils.TestCommand):
    """Test cliff command classes"""

    def assertListItemEqual(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for item_expected, item_actual in zip(expected, actual):
            self.assertItemEqual(item_expected, item_actual)

    def assertItemEqual(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for col_expected, col_actual in zip(expected, actual):
            if isinstance(col_expected, cliff_columns.FormattableColumn):
                self.assertIsInstance(col_actual, col_expected.__class__)
                self.assertEqual(col_expected.human_readable(),
                                 col_actual.human_readable())
            else:
                self.assertEqual(col_expected, col_actual)


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
