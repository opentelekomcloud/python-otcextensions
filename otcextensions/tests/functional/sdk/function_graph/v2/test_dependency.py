# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import uuid
from otcextensions.sdk.function_graph.v2 import dependency
from otcextensions.tests.functional import base

from openstack import _log

_logger = _log.setup_logging('openstack')


class TestFunctionDependencies(base.BaseFunctionalTest):
    ID = None
    uuid = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestFunctionDependencies, self).setUp()
        u = 'https://fg-test-files.obs.eu-de.otc.t-systems.com/dependency.zip'
        self.attrs = {
            'depend_link': u,
            'depend_type': 'obs',
            'runtime': 'Python3.10',
            'name': 'test-dep-' + self.uuid
        }
        self.dep = self.conn.functiongraph.create_dependency_version(
            **self.attrs
        )
        assert isinstance(self.dep, dependency.Dependency)
        self.addCleanup(
            self.conn.functiongraph.delete_dependency_version,
            self.dep
        )

    def test_list_dependencies(self):
        dep = list(self.conn.functiongraph.dependencies())
        self.assertGreaterEqual(6, len(dep))

    def test_list_dependency_versions(self):
        v = list(self.conn.functiongraph.dependency_versions(self.dep))
        self.assertEqual(1, len(v[0].dependencies))

    def test_get_dependency_version(self):
        v = self.conn.functiongraph.get_dependency_version(self.dep)
        self.assertEqual(v.dep_id, self.dep.dep_id)
        self.assertEqual(v.version, 1)
