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
from unittest import mock

from otcextensions.sdk.function_graph.v2 import _proxy
from otcextensions.sdk.function_graph.v2 import function as _function
from otcextensions.sdk.function_graph.v2 import function_invocation as _fi
from otcextensions.sdk.function_graph.v2 import dependency as _d
from otcextensions.sdk.function_graph.v2 import quota as _q
from openstack.tests.unit import test_proxy_base


class TestFgProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestFgProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestFgFunctions(TestFgProxy):

    def test_functions(self):
        self.verify_list(self.proxy.functions, _function.Function)

    def test_create_function(self):
        self.verify_create(self.proxy.create_function,
                           _function.Function,
                           method_kwargs={'name': 'test_function'},
                           expected_kwargs={'name': 'test_function'})

    def test_delete_function(self):
        function = _function.Function(
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default'
                     ':access-mysql-js-1213-1737554083545:latest')
        self.proxy._get_resource = mock.Mock(return_value=function)
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._delete_function',
            self.proxy.delete_function,
            method_args=[function],
            expected_args=[self.proxy, function],
        )

    def test_get_function_code(self):
        function = _function.Function(
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default'
                     ':access-mysql-js-1213-1737554083545:latest')
        self.proxy._get_resource = mock.Mock(return_value=function)
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._get_function_code',
            self.proxy.get_function_code,
            method_args=[function],
            expected_args=[self.proxy, function],
        )

    def test_get_function_metadata(self):
        function = _function.Function(
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default'
                     ':access-mysql-js-1213-1737554083545:latest')
        self.proxy._get_resource = mock.Mock(return_value=function)
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._get_function_metadata',
            self.proxy.get_function_metadata,
            method_args=[function],
            expected_args=[self.proxy, function]
        )

    def test_get_resource_tags(self):
        function = _function.Function(id='test_function')
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._get_resource_tags',
            self.proxy.get_resource_tags,
            method_args=[function],
            expected_args=[self.proxy, function]
        )

    def test_create_resource_tags(self):
        function = _function.Function(id='test_function')
        tags = [{'key': 'tag1', 'value': 'value1'}]
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._create_resource_tags',
            self.proxy.create_resource_tags,
            method_args=[function, tags],
            expected_args=[self.proxy, function, tags]
        )

    def test_delete_resource_tags(self):
        function = _function.Function(id='test_function')
        tags = [{'key': 'tag1'}]
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._delete_resource_tags',
            self.proxy.delete_resource_tags,
            method_args=[function, tags],
            expected_args=[self.proxy, function, tags]
        )

    def test_update_pin_status(self):
        function = _function.Function(id='test_function')
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._update_pin_status',
            self.proxy.update_pin_status,
            method_args=[function],
            expected_args=[self.proxy, function]
        )

    def test_update_function_code(self):
        function = _function.Function(id='test_function')
        attrs = {
            'code_type': 'zip',
            'code_url': 'https://example.com/code.zip',
            'code_filename': 'code.zip',
            'func_code': {'file': 'content'}
        }
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._update_function_code',
            self.proxy.update_function_code,
            method_args=[function],
            method_kwargs=attrs,
            expected_args=[self.proxy, function],
            expected_kwargs=attrs
        )

    def test_update_function_metadata(self):
        function = _function.Function(id='test_function')
        attrs = {'description': 'Updated metadata'}
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._update_function_metadata',
            self.proxy.update_function_metadata,
            method_args=[function],
            method_kwargs=attrs,
            expected_args=[self.proxy, function],
            expected_kwargs=attrs
        )

    def test_update_max_instances(self):
        function = _function.Function(id='test_function')
        instances = 10
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.'
            'Function._update_max_instances',
            self.proxy.update_max_instances,
            method_args=[function, instances],
            expected_args=[self.proxy, function, 10],
        )

    def test_invocation_async(self):
        fi = _fi.FunctionInvocation(
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default'
                     ':access-mysql-js-1213-1737554083545:latest',
            attrs={'a': 'b'}
        )
        self.proxy._get_resource = mock.Mock(return_value=fi)
        self._verify(
            'otcextensions.sdk.function_graph.v2.function_invocation.'
            'FunctionInvocation._invocation',
            self.proxy.executing_function_asynchronously,
            method_args=[fi.func_urn],
            method_kwargs={'a': 'b'},
            expected_args=[self.proxy, 'invocations-async'],
            expected_kwargs={'a': 'b'}
        )

    def test_invocation_sync(self):
        fi = _fi.FunctionInvocation(
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default'
                     ':access-mysql-js-1213-1737554083545:latest',
            attrs={'a': 'b'}
        )
        self.proxy._get_resource = mock.Mock(return_value=fi)
        self._verify(
            'otcextensions.sdk.function_graph.v2.function_invocation.'
            'FunctionInvocation._invocation',
            self.proxy.executing_function_synchronously,
            method_args=[fi.func_urn],
            method_kwargs={'a': 'b'},
            expected_args=[self.proxy, 'invocations'],
            expected_kwargs={'a': 'b'}
        )


class TestFgQuotas(TestFgProxy):
    def test_quotas(self):
        self.verify_list(self.proxy.quotas, _q.Quota)


class TestFgDependencies(TestFgProxy):
    def test_dependencies(self):
        self.verify_list(
            self.proxy.dependencies,
            _d.Dependency,
            expected_args=[{}],
        )

    def test_create_dependency_version(self):
        self.verify_create(
            self.proxy.create_dependency_version,
            _d.Dependency
        )

    def test_delete_dependency_version(self):
        dep = _d.Dependency(
            version=1,
            dep_id='edbd67fa-f107-40b3-af75-a85f0577ad61'
        )
        self.proxy._get_resource = mock.Mock(return_value=dep)
        self._verify(
            'otcextensions.sdk.function_graph.v2.dependency.'
            'Dependency._delete_version',
            self.proxy.delete_dependency_version,
            method_args=[dep],
            expected_args=[self.proxy, dep],
        )

    def test_dependency_versions(self):
        dep = _d.Dependency(
            version=1,
            dep_id='edbd67fa-f107-40b3-af75-a85f0577ad61'
        )
        self.verify_list(
            self.proxy.dependency_versions,
            _d.Dependency,
            method_args=[dep],
            expected_args=[{}],
        )

    def test_get_dependency_version(self):
        dep = _d.Dependency(
            version=1,
            dep_id='edbd67fa-f107-40b3-af75-a85f0577ad61'
        )
        self.verify_get(
            self.proxy.get_dependency_version,
            _d.Dependency,
            method_args=[dep],
            expected_args=[],
            expected_kwargs={"requires_id": False}
        )
