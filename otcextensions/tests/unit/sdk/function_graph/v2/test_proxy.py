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
from otcextensions.sdk.function_graph.v2 import reserved_instance as _r
from otcextensions.sdk.function_graph.v2 import import_function as _import
from otcextensions.sdk.function_graph.v2 import trigger as _trigger
from otcextensions.sdk.function_graph.v2 import async_notification as _async
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
            expected_args=[],
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
            expected_args=[],
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


class TestFgReservedInstances(TestFgProxy):
    def test_update_event(self):
        func = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_update(
            self.proxy.update_instances_number,
            _r.ReservedInstance,
            method_args=[func],
            expected_args=[],
            expected_kwargs={
                'function_urn': func.func_urn.rpartition(":")[0],
                'x': 1,
                'y': 2,
                'z': 3
            }
        )

    def test_reserved_instances_config(self):
        self.verify_list(
            self.proxy.reserved_instances_config,
            _r.ReservedInstance,
            method_args=[],
            expected_args=[],
        )

    def test_reserved_instances(self):
        self.verify_list(
            self.proxy.reserved_instances,
            _r.ReservedInstance,
            method_args=[],
            expected_args=[],
        )


class TestFgImportExport(TestFgProxy):
    def test_import_function(self):
        attrs = {
            'func_name': 'test',
            'file_type': 'zip',
            'file_name': 'test.zip',
            'file_code': 'UEsDBBQAAAAIAPBbPFpOs3AMAgEAAEwCAAAGAAAAZGVwLnB5jVHB'
                         'asMwDL37K4R3iSGMMtglsNNW2HH0B4oXq9SjtY2shJbSf5/tpl5y'
                         'GFQX23qS3nuWPQZPDD/ROyGEwR3stTMHpAZHdNxC7x3jiVUnIAXT'
                         '+XbJ8QRfmiIC7xGsCwND6YHGaNaqlhVom3PwVoieD16beCNQYj6O'
                         'bGrP4wL50Ro0kNtqRch4IzfYox0nsJPtjGExboM8kAMNhDF4F7Fi'
                         '90QSdKnJHDKy5iG+e4Oyg5fVql3C396cE7CTH9kOTUI6uPxJuMra'
                         'cp0RFinFvRmOITZ3CZNiPPUYGNblsD6pjoDzr/4sawEk8hRrvjy3'
                         'D9p5/d/OOs9JNiKnxasHLSzJlfgFUEsBAhQDFAAAAAgA8Fs8Wk6z'
                         'cAwCAQAATAIAAAYAAAAAAAAAAAAAAKSBAAAAAGRlcC5weVBLBQYA'
                         'AAAAAQABADQAAAAmAQAAAAA='
        }
        self.verify_create(
            self.proxy.import_function,
            _import.Import,
            method_kwargs={**attrs}
        )

    def test_export(self):
        function = _function.Function(id='test_function')
        self._verify(
            'otcextensions.sdk.function_graph.v2.export_function.'
            'Export._export',
            self.proxy.export_function,
            method_args=[function],
            expected_args=[self.proxy, function]
        )


class TestFgTrigger(TestFgProxy):

    def test_triggers(self):
        function = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_list(
            self.proxy.triggers,
            _trigger.Trigger,
            method_kwargs={"function_urn": function.func_urn},
            expected_kwargs={
                "function_urn": function.func_urn.rpartition(":")[0]
            },
            expected_args=[]
        )

    def test_create_trigger(self):
        function = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_create(self.proxy.create_trigger,
                           _trigger.Trigger,
                           method_args=[function],
                           method_kwargs={
                               "trigger_type_code": "TIMER",
                               "trigger_status": "ACTIVE",
                               "event_data": {
                                   "name": "Timer-l8v2",
                                   "schedule": "3m",
                                   "schedule_type": "Rate"
                               }
                           },
                           expected_kwargs={
                               "trigger_type_code": "TIMER",
                               "trigger_status": "ACTIVE",
                               "event_data": {
                                   "name": "Timer-l8v2",
                                   "schedule": "3m",
                                   "schedule_type": "Rate"
                               }
                           },
                           expected_args=[]
                           )

    def test_update_trigger(self):
        function = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.update_trigger,
            method_args=[function.func_urn, 'TIMER', 'id'],
            method_kwargs={
                "trigger_status": "DISABLED",
            },
            expected_kwargs={
                "trigger_status": "DISABLED",
            },
            expected_args=[_trigger.Trigger]
        )

    def test_delete_trigger(self):
        function = _function.Function(
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default'
                     ':access-mysql-js-1213-1737554083545:latest')
        self._verify(
            'otcextensions.sdk.function_graph.v2.trigger.'
            'Trigger._delete_trigger',
            self.proxy.delete_trigger,
            method_args=[function, "TIMER", "id"],
            expected_args=[self.proxy, function, "TIMER", "id"],
        )

    def test_delete_triggers(self):
        function = _function.Function(
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default'
                     ':access-mysql-js-1213-1737554083545:latest')
        self._verify(
            'otcextensions.sdk.function_graph.v2.trigger.'
            'Trigger._delete_triggers',
            self.proxy.delete_all_triggers,
            method_args=[function.func_urn],
            expected_args=[self.proxy, function.func_urn.rpartition(":")[0]],
        )

    def test_get_trigger(self):
        self.verify_get(
            self.proxy.get_trigger,
            _trigger.Trigger,
            method_args=["urn", "code", "id"],
            expected_kwargs={
                "requires_id": False
            },
            expected_args=[]
        )


class TestFgAsyncNotifications(TestFgProxy):

    def test_async_notifications(self):
        function = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_list(
            self.proxy.async_notifications,
            _async.Notification,
            method_kwargs={"function": function.func_urn},
            expected_kwargs={
                "function_urn": function.func_urn.rpartition(":")[0]
            },
            expected_args=[]
        )

    def test_configure_async_notification(self):
        function = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_create(
            self.proxy.configure_async_notification,
            _async.Notification,
            method_args=[function],
            method_kwargs={
                "max_async_event_age_in_seconds": 1000,
            },
            expected_kwargs={
                "function_urn": function.func_urn.rpartition(":")[0],
                "max_async_event_age_in_seconds": 1000,
            },
            expected_args=[]
        )

    def test_delete_async_notification(self):
        function = _function.Function(
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default'
                     ':access-mysql-js-1213-1737554083545:latest')
        self.verify_delete(
            self.proxy.delete_async_notification,
            _async.Notification,
            method_args=[function],
            expected_args=[],
            expected_kwargs={
                'function_urn': function.func_urn.rpartition(":")[0]
            }
        )

    def test_all_versions_async_notifications(self):
        function = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_list(
            self.proxy.all_versions_async_notifications,
            _async.Notification,
            method_kwargs={"function": function.func_urn},
            expected_kwargs={
                "function_urn": function.func_urn
            },
            expected_args=[]
        )

    def test_async_invocation_requests(self):
        function = _function.Function(
            name='test',
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default:access-mysql-js-1213-1737554083545:'
                     'latest'
        )
        self.verify_list(
            self.proxy.async_invocation_requests,
            _async.Requests,
            method_kwargs={"function": function.func_urn},
            expected_kwargs={
                "function_urn": function.func_urn.rpartition(":")[0]
            },
            expected_args=[]
        )

    def test_stop_async_invocation_request(self):
        function = _function.Function(
            func_urn='urn:fss:eu-de:45c274f200d2498683982c8741fb76ac:'
                     'function:default'
                     ':access-mysql-js-1213-1737554083545:latest')
        self._verify(
            'otcextensions.sdk.function_graph.v2.async_notification.'
            'Requests._stop',
            self.proxy.stop_async_invocation_request,
            method_args=[function],
            method_kwargs={"request_id": "123"},
            expected_args=[self.proxy],
            expected_kwargs={
                "function_urn": function.func_urn.rpartition(":")[0],
                "request_id": "123"
            }
        )
