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
            'otcextensions.sdk.function_graph.v2.function.Function._delete_function',
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
            'otcextensions.sdk.function_graph.v2.function.Function._get_function_code',
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
            'otcextensions.sdk.function_graph.v2.function.Function._get_function_metadata',
            self.proxy.get_function_metadata,
            method_args=[function],
            expected_args=[self.proxy, function]
        )

    def test_get_resource_tags(self):
        function = _function.Function(id='test_function')
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.Function._get_resource_tags',
            self.proxy.get_resource_tags,
            method_args=[function],
            expected_args=[self.proxy, function]
        )

    def test_create_resource_tags(self):
        function = _function.Function(id='test_function')
        tags = [{'key': 'tag1', 'value': 'value1'}]
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.Function._create_resource_tags',
            self.proxy.create_resource_tags,
            method_args=[function, tags],
            expected_args=[self.proxy, function, tags]
        )

    def test_delete_resource_tags(self):
        function = _function.Function(id='test_function')
        tags = [{'key': 'tag1'}]
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.Function._delete_resource_tags',
            self.proxy.delete_resource_tags,
            method_args=[function, tags],
            expected_args=[self.proxy, function, tags]
        )

    def test_update_pin_status(self):
        function = _function.Function(id='test_function')
        self._verify(
            'otcextensions.sdk.function_graph.v2.function.Function._update_pin_status',
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
            'otcextensions.sdk.function_graph.v2.function.Function._update_function_code',
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
            'otcextensions.sdk.function_graph.v2.function.Function._update_function_metadata',
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
            'otcextensions.sdk.function_graph.v2.function.Function._update_max_instances',
            self.proxy.update_max_instances,
            method_args=[function, instances],
            expected_args=[self.proxy, function, 10],
        )
