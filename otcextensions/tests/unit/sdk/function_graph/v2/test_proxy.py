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
from otcextensions.sdk.function_graph.v2 import event as _event
from otcextensions.sdk.function_graph.v2 import alias as _alias
from otcextensions.sdk.function_graph.v2 import version as _version
from otcextensions.sdk.function_graph.v2 import metric as _metric
from otcextensions.sdk.function_graph.v2 import log as _log
from otcextensions.sdk.function_graph.v2 import template as _t
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


class TestFgEvents(TestFgProxy):
    def test_events(self):
        func_urn = ('urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                    'function:default:access-mysql-js-1213-1737554083545:'
                    'latest')
        self.verify_list(
            self.proxy.events,
            _event.Event,
            method_args=[func_urn],
            expected_args=[],
            expected_kwargs={
                'function_urn': func_urn.rpartition(":")[0]
            },
        )

    def test_create_event(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_create(
            self.proxy.create_event,
            _event.Event,
            method_kwargs={
                'function': func,
                'name': 'test_event'
            },
            expected_kwargs={
                'function_urn': func.func_urn.rpartition(":")[0],
                'name': 'test_event'}
        )

    def test_delete_event(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        event = _event.Event(
            name='test',
        )
        self.verify_delete(
            self.proxy.delete_event,
            _event.Event,
            method_args=[func, event],
            expected_args=[event],
            expected_kwargs={'function_urn': func.func_urn.rpartition(":")[0]}
        )

    def test_update_event(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        event = _event.Event(name='test')
        self.verify_update(
            self.proxy.update_event,
            _event.Event,
            method_args=[func, event],
            expected_args=[event],
            expected_kwargs={
                'function_urn': func.func_urn.rpartition(":")[0],
                'x': 1,
                'y': 2,
                'z': 3
            }
        )

    def test_get_event(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        event = _event.Event(name='test')
        self.verify_get(
            self.proxy.get_event,
            _event.Event,
            method_args=[func, event],
            expected_args=[event],
            expected_kwargs={
                'function_urn': func.func_urn,
            }
        )


class TestFgAlias(TestFgProxy):
    def test_aliases(self):
        func_urn = ('urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                    'function:default:access-mysql-js-1213-1737554083545:'
                    'latest')
        self.verify_list(
            self.proxy.aliases,
            _alias.Alias,
            method_args=[func_urn],
            expected_args=[],
            expected_kwargs={
                'function_urn': func_urn.rpartition(":")[0]
            },
        )

    def test_create_alias(self):
        func = _function.Function(
            name='test',
            id='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
               'function:default:access-mysql-js-1213-1737554083545:'
               'latest'
        )
        self.verify_create(
            self.proxy.create_alias,
            _alias.Alias,
            method_kwargs={
                'function': func,
                'name': 'test_event'
            },
            expected_kwargs={
                'function_urn': func.id.rpartition(":")[0],
                'name': 'test_event'}
        )

    def test_delete_alias(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        a = _alias.Alias(
            name='test',
        )
        self.verify_delete(
            self.proxy.delete_alias,
            _alias.Alias,
            method_args=[func, a],
            expected_args=[a],
            expected_kwargs={'function_urn': func.func_urn.rpartition(":")[0]}
        )

    def test_update_event(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        a = _alias.Alias(name='test')
        attrs = {
            'version': 'new-version',
            'description': 'new',
        }
        self._verify(
            'otcextensions.sdk.function_graph.v2.alias.'
            'Alias._update_alias',
            self.proxy.update_alias,
            method_args=[func, a],
            method_kwargs=attrs,
            expected_args=[self.proxy, func, a],
            expected_kwargs=attrs
        )

    def test_get_event(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        a = _alias.Alias(name='test')
        self.verify_get(
            self.proxy.get_alias,
            _alias.Alias,
            method_args=[func, a],
            expected_args=[a],
            expected_kwargs={
                'function_urn': func.func_urn,
            }
        )


class TestFgVersion(TestFgProxy):
    def test_versions(self):
        func_urn = ('urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                    'function:default:access-mysql-js-1213-1737554083545:'
                    'latest')
        self.verify_list(
            self.proxy.versions,
            _version.Version,
            method_args=[func_urn],
            expected_args=[],
            expected_kwargs={
                'function_urn': func_urn.rpartition(":")[0]
            },
        )

    def test_publish_version(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_create(
            self.proxy.publish_version,
            _version.Version,
            method_kwargs={
                'function': func,
                'name': 'test_event'
            },
            expected_kwargs={
                'function_urn': func.func_urn.rpartition(":")[0],
                'name': 'test_event'}
        )


class TestFgMetric(TestFgProxy):
    def test_metrics(self):
        self.verify_list(
            self.proxy.metrics,
            _metric.Metric,
        )

    def test_function_metrics(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_list(
            self.proxy.function_metrics,
            _metric.Metric,
            method_args=[
                func,
                '1596686400000,1596686400000'
            ],
            expected_args=[],
        )


class TestFgLog(TestFgProxy):
    def test_get_lts_log_settings(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_get(
            self.proxy.get_lts_log_settings,
            _log.Log,
            method_args=[
                func,
            ],
            expected_args=[],
            expected_kwargs={'function_urn': func.func_urn.rpartition(":")[0],
                             'requires_id': False}
        )

    def test_enable_lts_log(self):
        self.verify_create(
            self.proxy.enable_lts_log,
            _log.Log,
            method_kwargs={},
        )


class TestFgTemplate(TestFgProxy):
    def test_get_template(self):
        self.verify_get(
            self.proxy.get_template,
            _t.Template,
            method_args=["41d5d9ca-cea3-4ba9-b866-e30c46f45f1f"],
            expected_kwargs={
                "template_id": "41d5d9ca-cea3-4ba9-b866-e30c46f45f1f",
                "requires_id": False
            },
            expected_args=[]
        )
