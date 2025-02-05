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

import uuid
from otcextensions.sdk.function_graph.v2 import function
from otcextensions.sdk.function_graph.v2 import version
from otcextensions.sdk.function_graph.v2 import alias

from openstack import _log

from otcextensions.tests.functional.sdk.function_graph import TestFg

_logger = _log.setup_logging('openstack')


class TestFunctionAlias(TestFg):
    ID = None
    uuid = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestFunctionAlias, self).setUp()
        self.function = self.client.create_function(**TestFg.function_attrs)
        assert isinstance(self.function, function.Function)

        self.publish_attrs = {
            'version': 'new-version',
            'description': 'otce',
        }

        self.publish = self.client.publish_version(
            self.function, **self.publish_attrs
        )
        assert isinstance(self.publish, version.Version)

        self.alias_attrs = {
            'name': 'a1',
            'version': 'new-version'
        }
        self.alias = self.client.create_alias(
            self.publish.func_urn, **self.alias_attrs
        )
        assert isinstance(self.alias, alias.Alias)
        self.ID = self.alias.name
        self.addCleanup(
            self.client.delete_function,
            self.function
        )
        self.addCleanup(
            self.client.delete_alias,
            self.function,
            self.alias
        )

    def test_function_aliases(self):
        elist = list(self.client.aliases(
            func_urn=self.function.func_urn))
        self.assertIn(self.alias_attrs['name'], elist[0].name)

    def test_function_published_versions(self):
        vlist = list(self.client.versions(
            func_urn=self.function.func_urn))
        self.assertIn(self.publish_attrs['version'], vlist[1].version)

    def test_get_function_alias(self):
        a = self.client.get_alias(
            self.function, self.alias)
        self.assertIn(self.ID, a.id)

    def test_update_function_alias(self):
        attrs = {
            'version': 'new-version',
            'description': 'new',
        }
        updated = self.client.update_alias(
            self.function, self.alias, **attrs)
        self.assertIn(attrs['version'], updated.version)
        self.assertIn(attrs['description'], updated.description)
