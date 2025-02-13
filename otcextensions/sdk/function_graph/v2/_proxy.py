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
from openstack import proxy

from otcextensions.common.utils import extract_url_parts
from otcextensions.sdk.function_graph.v2 import function as _function
from otcextensions.sdk.function_graph.v2 import function_invocation as _fi
from otcextensions.sdk.function_graph.v2 import quota as _quota
from otcextensions.sdk.function_graph.v2 import dependency as _d
from otcextensions.sdk.function_graph.v2 import event as _event
from otcextensions.sdk.function_graph.v2 import alias as _alias
from otcextensions.sdk.function_graph.v2 import version as _version
from otcextensions.sdk.function_graph.v2 import metric as _metric
from otcextensions.sdk.function_graph.v2 import log as _log
from otcextensions.sdk.function_graph.v2 import template as _t
from otcextensions.sdk.function_graph.v2 import reserved_instance as _r
from otcextensions.sdk.function_graph.v2 import export_function as _export
from otcextensions.sdk.function_graph.v2 import import_function as _import
from otcextensions.sdk.function_graph.v2 import trigger as _trigger
from otcextensions.sdk.function_graph.v2 import async_notification as _async


class Proxy(proxy.Proxy):
    skip_discovery = True

    def _extract_name(self, url, service_type=None, project_id=None):
        return extract_url_parts(url, project_id)

    # ======== Function Methods ========

    def create_function(self, **attrs):
        """Create a new function from attributes.

        :param dict attrs: Keyword arguments to create a Function.
        :returns: The created Function instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        return self._create(_function.Function, **attrs)

    def delete_function(self, function, ignore_missing=True):
        """Delete a function.

        :param ignore_missing:
        :param function: The instance of the Function to delete.
        :returns: ``None``
        """
        function = self._get_resource(_function.Function, function)
        return function._delete_function(self, function)

    def functions(self, **query):
        """List all functions with optional filters.

        :param dict query: Query parameters to filter the function list.
        :returns: A generator of Function instances.
        """
        return self._list(_function.Function, **query)

    def get_function_code(self, function):
        """Get details of a function code.

        :param function: The URN or instance of the Function to retrieve.
        :returns: The Function instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        function = self._get_resource(_function.Function, function)
        return function._get_function_code(self, function)

    def get_function_metadata(self, function):
        """Get details of a function metadata.

        :param function: The URN or instance of the Function to retrieve.
        :returns: The Function instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        function = self._get_resource(_function.Function, function)
        return function._get_function_metadata(self, function)

    def get_resource_tags(self, function):
        """Get a function resource tags.

        :param function: The URN or instance of the Function to retrieve.
        :returns: The Function instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        function = self._get_resource(_function.Function, function)
        return function._get_resource_tags(self, function)

    def create_resource_tags(self, function, tags):
        """Create function resource tags.

        :param tags: list of tags
        :param function: The URN or instance of the Function to create tags.
        :returns: ``None``
        """
        function = self._get_resource(_function.Function, function)
        return function._create_resource_tags(self, function, tags)

    def delete_resource_tags(self, function, tags):
        """Delete function resource tags.

        :param tags: list of tags
        :param function: The URN or instance of the Function
               from which need to delete tags.
        :returns: ``None``
        """
        function = self._get_resource(_function.Function, function)
        return function._delete_resource_tags(self, function, tags)

    def update_pin_status(self, function):
        """Update a function's pin status.

        :param function: The URN or instance of the Function to update.
        :returns: The updated Function pin status.
        :returns: ``None``
        """
        function = self._get_resource(_function.Function, function)
        return function._update_pin_status(self, function)

    def update_function_code(self, function, **attrs):
        """Update a function code.

        :param function: The URN or instance of the Function to update.
        :param attrs: Attributes for updating the function code. These include:
               code_type: Function code type. Options:
               * `inline`: Inline code.
               * `zip`: ZIP file.
               * `obs`: Function code stored in an OBS bucket.
               * `jar`: JAR file (mainly for Java functions).

               code_url: If `code_type` is set to `obs`, enter the OBS URL
               of the function code package. Leave this parameter blank if
               `code_type` is not `obs`.

               code_filename: Name of the function file. This parameter
               is mandatory only when `code_type` is set to `jar` or `zip`.

               func_code: Response body of the `FuncCode` struct.

               depend_version_list: Dependency version IDs.

        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        function = self._get_resource(_function.Function, function)
        return function._update_function_code(self, function, **attrs)

    def update_function_metadata(self, function, **attrs):
        """Update a function metadata.

        :param function: The URN or instance of the Function to update.
        :returns: The updated Function pin status.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        function = self._get_resource(_function.Function, function)
        return function._update_function_metadata(self, function, **attrs)

    def update_max_instances(self, function, instances):
        """Update a function max instances number.

        :param instances: Maximum number of instances.
        :param function: The URN or instance of the Function to update.
        :returns: The updated Function pin status.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        function = self._get_resource(_function.Function, function)
        return function._update_max_instances(self, function, instances)

    # ======== Function Invocations Methods ========

    def executing_function_synchronously(self, func_urn, **attrs):
        """Execute a function synchronously.

        :param func_urn: The URN of the Function to run
        :param attrs: The request parameter as a key pair ("k":"v")
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.
            function_invocation.FunctionInvocation`
        """
        fi = self._get_resource(
            _fi.FunctionInvocation, func_urn,
            func_urn=func_urn.rpartition(":")[0]
        )
        return fi._invocation(self, 'invocations', **attrs)

    def executing_function_asynchronously(self, func_urn, **attrs):
        """Execute a function asynchronously.

        :param func_urn: The URN of the Function to run
        :param attrs: The request parameter as a key pair ("k":"v")
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.
            function_invocation.FunctionInvocation`
        """
        fi = self._get_resource(
            _fi.FunctionInvocation, func_urn,
            func_urn=func_urn.rpartition(":")[0]
        )
        return fi._invocation(self, 'invocations-async', **attrs)

    # ======== Function Quotas Methods ========

    def quotas(self):
        """List all quotas.

        :returns: A generator of Quota instances.
        """
        return self._list(_quota.Quota)

    # ======== Function Dependencies Methods ========

    def dependencies(self, **query):
        """List all dependencies.

        :param dict query: Query parameters to filter the dependencies list.
        :returns: A generator of Dependency instances.
        """
        return self._list(_d.Dependency, **query)

    def create_dependency_version(self, **attrs):
        """Create a new dependency from attributes.

        :param dict attrs: Keyword arguments to create a Function.
        :returns: The created Dependency instance.
        :rtype:
            :class:`~otcextensions.sdk.function_graph.v2.dependency.Dependency`
        """
        base_path = "/fgs/dependencies/version"
        return self._create(_d.Dependency, **attrs, base_path=base_path)

    def delete_dependency_version(self, dependency, ignore_missing=True):
        """Delete a dependency.

        :param ignore_missing:
        :param dependency: The instance of the Dependency to delete.
        :returns: ``None``
        """
        dep = self._get_resource(_d.Dependency, dependency)
        return dep._delete_version(self, dependency)

    def dependency_versions(self, dependency, **query):
        """List all dependency versions.

        :param dependency: Dependency instance
        :param dict query: Query parameters to filter the versions list.
        :returns: A generator of Dependency instances.
        """
        base_path = f"/fgs/dependencies/{dependency.dep_id}/version"
        return self._list(_d.Dependency, **query, base_path=base_path)

    def get_dependency_version(self, dependency):
        """List all dependency versions.

        :param dependency: Dependency instance
        :returns: A generator of Dependency instances.
        """
        base_path = (f"/fgs/dependencies/{dependency.dep_id}"
                     f"/version/{dependency.version}")
        return self._get(_d.Dependency, base_path=base_path, requires_id=False)

    # ======== Test Events Methods ========

    def create_event(self, function, **attrs):
        """Create a new event from attributes.

        :param function: The URN or instance of the Function to create
            event in.
        :param dict attrs: Keyword arguments to create an Event.
        :returns: The created Event instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.event.Event`
        """
        function = self._get_resource(_function.Function, function)
        function_urn = function.func_urn.rpartition(":")[0]
        return self._create(
            _event.Event, function_urn=function_urn, **attrs
        )

    def delete_event(self, function, event, ignore_missing=True):
        """Delete an event.

        :param function: The URN or instance of the Function to delete
            event from.
        :param ignore_missing: When False,
            `openstack.exceptions.ResourceNotFound`
            will be raised when the tag does not exist.
            When True, no exception will be set when attempting
            to delete a nonexistent event.
        :param event: The instance of the Event to delete.
        :returns: ``None``
        """
        function = self._get_resource(_function.Function, function)
        function_urn = function.func_urn.rpartition(":")[0]
        return self._delete(
            _event.Event, event,
            function_urn=function_urn, ignore_missing=ignore_missing
        )

    def events(self, func_urn):
        """List all events.

        :param func_urn: The URN of the Function to fetch
            events from.
        :returns: A generator of Event instances.
        """
        function_urn = func_urn.rpartition(":")[0]
        return self._list(_event.Event, function_urn=function_urn)

    def get_event(self, function, event):
        """Get one event by ID.

        :param event: key id or an instance of
            :class:`~otcextensions.sdk.function_graph.v2.event.Event`
        :param function: The value can be the ID of a function or
            a :class:`~otcextensions.sdk.function_graph.v2.function.Function`
            instance.
        :returns: instance of
            :class:`~otcextensions.sdk.function_graph.v2.event.Event`
        """
        function = self._get_resource(_function.Function, function)
        return self._get(
            _event.Event, event,
            function_urn=function.func_urn
        )

    def update_event(self, function, event, **attrs):
        """Update an event from attributes.

        :param event: key id or an instance of
            :class:`~otcextensions.sdk.function_graph.v2.event.Event`
        :param function: The URN or instance of the Function to update
            event in.
        :param dict attrs: Keyword arguments to update an Event.
        :returns: The updated Event instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.event.Event`
        """
        function = self._get_resource(_function.Function, function)
        function_urn = function.func_urn.rpartition(":")[0]
        return self._update(
            _event.Event, event, function_urn=function_urn, **attrs
        )

    # ======== Versions Methods ========
    def versions(self, func_urn):
        """List all published versions.

        :param func_urn: The URN of the Function to fetch
            events from.
        :returns: A generator of Version instances.
        """
        function_urn = func_urn.rpartition(":")[0]
        return self._list(_version.Version, function_urn=function_urn)

    def publish_version(self, function, **attrs):
        """Publish a new version from attributes.

        :param function: The URN or instance of the Function to create
            event in.
        :param dict attrs: Keyword arguments to publish a Version.
        :returns: The created Version instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.version.Version`
        """
        function = self._get_resource(_function.Function, function)
        function_urn = function.func_urn.rpartition(":")[0]
        return self._create(
            _version.Version, function_urn=function_urn, **attrs
        )

    # ======== Aliases Methods ========

    def aliases(self, func_urn):
        """List all aliases.

        :param func_urn: The URN of the Function to fetch
            events from.
        :returns: A generator of Alias instances.
        """
        function_urn = func_urn.rpartition(":")[0]
        return self._list(_alias.Alias, function_urn=function_urn)

    def create_alias(self, function, **attrs):
        """Create a new alias from attributes.

        :param function: The URN or instance of the Function to create
            event in.
        :param dict attrs: Keyword arguments to create an Alias.
        :returns: The created Event instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.alias.Alias`
        """
        function = self._get_resource(_function.Function, function)
        function_urn = function.id.rpartition(":")[0]
        return self._create(
            _alias.Alias, function_urn=function_urn, **attrs
        )

    def delete_alias(self, function, alias, ignore_missing=True):
        """Delete an alias.

        :param function: The URN or instance of the Function to delete
            alias from.
        :param ignore_missing: When False,
            `openstack.exceptions.ResourceNotFound`
            will be raised when the tag does not exist.
            When True, no exception will be set when attempting
            to delete a nonexistent event.
        :param alias: The instance of the Alias to delete.
        :returns: ``None``
        """
        function = self._get_resource(_function.Function, function)
        function_urn = function.func_urn.rpartition(":")[0]
        return self._delete(
            _alias.Alias, alias,
            function_urn=function_urn, ignore_missing=ignore_missing
        )

    def update_alias(self, function, alias, **attrs):
        """Update an alias from attributes.

        :param alias: key id or an instance of
            :class:`~otcextensions.sdk.function_graph.v2.alias.Alias`
        :param function: The URN or instance of the Function to update
            alias in.
        :param dict attrs: Keyword arguments to update an Alias.
        :returns: The updated Alias instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.alias.Alias`
        """
        function = self._get_resource(_function.Function, function)
        a = self._get_resource(_alias.Alias, alias)
        return a._update_alias(self, function, alias, **attrs)

    def get_alias(self, function, alias):
        """Get one alias by ID.

        :param alias: key id or an instance of
            :class:`~otcextensions.sdk.function_graph.v2.alias.Alias`
        :param function: The value can be the ID of a function or
            a :class:`~otcextensions.sdk.function_graph.v2.function.Function`
            instance.
        :returns: instance of
            :class:`~otcextensions.sdk.function_graph.v2.alias.Alias`
        """
        function = self._get_resource(_function.Function, function)
        return self._get(
            _alias.Alias, alias,
            function_urn=function.func_urn
        )

    # ======== Metric Methods ========

    def metrics(self, **query):
        """List all tenant-level function statistics.

        :returns: A generator of Metric instances.
        """
        return self._list(_metric.Metric, **query)

    def function_metrics(self, function, period):
        """List all metrics of a function in a specified period.

        :returns: A generator of Metric instances.
        """
        function = self._get_resource(_function.Function, function)
        func_urn = function.func_urn.rpartition(":")[0]
        base_path = f'/fgs/functions/{func_urn}/statistics/{period}'
        return self._list(_metric.Metric, base_path=base_path)

    # ======== Log Methods ========

    def get_lts_log_settings(self, function):
        """Get log group and stream settings of a function.

        :param function: The value can be the ID of a function or
            a :class:`~otcextensions.sdk.function_graph.v2.function.Function`
            instance.
        :returns: instance of
            :class:`~otcextensions.sdk.function_graph.v2.log.Log`
        """
        func = self._get_resource(_function.Function, function)
        function_urn = func.func_urn.rpartition(":")[0]
        return self._get(
            _log.Log,
            function_urn=function_urn,
            requires_id=False
        )

    def enable_lts_log(self):
        """Enable log reporting to LTS.

        :returns: The created Log instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.log.Log`
        """
        base_path = '/fgs/functions/enable-lts-logs'
        return self._create(
            _log.Log, base_path=base_path
        )

    # ======== Templates Methods ========

    def get_template(self, template_id):
        """Get one template by ID.

        :param template_id: id of template
        :returns: instance of
            :class:`~otcextensions.sdk.function_graph.v2.template.Template`
        """
        return self._get(
            _t.Template,
            template_id=template_id,
            requires_id=False
        )

    # ======== Reserved Instances Methods ========

    def update_instances_number(self, function, **attrs):
        """Update a number of reserved instances from attributes.

        :param function: The URN or instance of the Function to update
            event in.
        :param dict attrs: Keyword arguments to update a reserved instances.
        :returns: The updated ReservedInstance instance.
        """
        function = self._get_resource(_function.Function, function)
        function_urn = function.func_urn.rpartition(":")[0]
        return self._update(
            _r.ReservedInstance, function_urn=function_urn, **attrs
        )

    def reserved_instances_config(self, **query):
        """List all reserved instances of a function.

        :returns: A generator of ReservedInstance instances.
        """
        base_path = "/fgs/functions/reservedinstanceconfigs"
        return self._list(_r.ReservedInstance, base_path=base_path, **query)

    def reserved_instances(self, **query):
        """List all query the number of instances reserved for a function.

        :returns: A generator of ReservedInstance instances.
        """
        base_path = "/fgs/functions/reservedinstances"
        return self._list(_r.ReservedInstance, base_path=base_path, **query)

    # ======== Import/Export Methods ========

    def export_function(self, function, **query):
        """Export a function.

        :param function: The URN or instance of the Function to export.
        :returns: instance of :class:
            `~otcextensions.sdk.function_graph.v2.export_function.Export`
        """
        function = self._get_resource(_function.Function, function)
        export = self._get_resource(_export.Export, "")
        return export._export(self, function, **query)

    def import_function(self, **attrs):
        """Import a function.

        :param dict attrs: Keyword arguments to import Function.
        :returns: The Import instance.
        """
        return self._create(
            _import.Import, **attrs
        )

    # ======== Trigger Methods ========

    def create_trigger(self, function, **attrs):
        """Create a new function trigger from attributes.

        :param dict attrs: Keyword arguments to create a Function.
        :returns: The created Trigger instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.trigger.Trigger`
        """
        function = self._get_resource(_function.Function, function)
        function_urn = function.func_urn.rpartition(":")[0]
        base_path = f'/fgs/triggers/{function_urn}'
        return self._create(_trigger.Trigger, base_path=base_path, **attrs)

    def delete_trigger(
            self, function_urn, trigger_type_code, trigger_id,
            ignore_missing=True
    ):
        """Delete a function trigger.

        :param trigger_id: Trigger ID.
        :param trigger_type_code: Trigger type code.
        :param function_urn: Function URN
        :param ignore_missing:
        :returns: ``None``
        """
        trigger = self._get_resource(_trigger.Trigger, "")
        return trigger._delete_trigger(
            self, function_urn, trigger_type_code, trigger_id
        )

    def delete_all_triggers(self, function_urn, ignore_missing=True):
        """Delete all function triggers.

        :param function_urn: Function URN
        :param ignore_missing:
        :returns: ``None``
        """
        function_urn = function_urn.rpartition(":")[0]
        trigger = self._get_resource(_trigger.Trigger, "")
        return trigger._delete_triggers(self, function_urn)

    def triggers(self, function_urn):
        """List all triggers of a function.

        :param function_urn: Function URN
        :returns: A generator of Trigger instances.
        """
        function_urn = function_urn.rpartition(":")[0]
        return self._list(_trigger.Trigger, function_urn=function_urn)

    def get_trigger(self, function_urn, trigger_type_code, trigger_id):
        """Get one trigger.

        :param trigger_id: Trigger ID.
        :param trigger_type_code: Trigger type code.
        :param function_urn: Function URN.
        :returns: instance of
            :class:`~otcextensions.sdk.function_graph.v2.trigger.Trigger`
        """
        function_urn = function_urn.rpartition(":")[0]
        base_path = (f'/fgs/triggers/{function_urn}'
                     f'/{trigger_type_code}'
                     f'/{trigger_id}')
        return self._get(
            _trigger.Trigger,
            base_path=base_path,
            requires_id=False
        )

    def update_trigger(
            self, function_urn, trigger_type_code, trigger_id, **attrs
    ):
        """Update a number of reserved instances from attributes.

        :param function_urn: Function URN.
        :param trigger_id: Trigger ID.
        :param trigger_type_code: Trigger type code.
        :param dict attrs: Keyword arguments to update a trigger.
        :returns: The updated Trigger instance.
        """
        function_urn = function_urn.rpartition(":")[0]
        base_path = (f'/fgs/triggers/{function_urn}/{trigger_type_code}'
                     f'/{trigger_id}')
        return self._update(
            _trigger.Trigger, base_path=base_path, **attrs
        )

    # ======== Asynchronous Invocation Methods ========

    def async_notifications(self, function):
        """List asynchronous invocation setting of a function version.

        :param function: Function instance or function URN
        :returns: A generator of Notification instances.
        """
        function = self._get_resource(_function.Function, function)
        if function.id is not None:
            function_urn = function.id.rpartition(":")[0]
        else:
            function_urn = function.func_urn.rpartition(":")[0]
        return self._list(_async.Notification, function_urn=function_urn)

    def configure_async_notification(
            self, function, **attrs
    ):
        """Configure asynchronous execution notification for a function.

        :param function: Function instance or function URN
        :param dict attrs: Keyword arguments to update a notifications
            settings.
        :returns: The updated Notification instance.
        """
        function = self._get_resource(_function.Function, function)
        if function.id is not None:
            function_urn = function.id.rpartition(":")[0]
        else:
            function_urn = function.func_urn.rpartition(":")[0]
        return self._create(
            _async.Notification, function_urn=function_urn, **attrs
        )

    def delete_async_notification(self, function, ignore_missing=True):
        """Delete asynchronous execution notification for a function.

        :param function: The URN or instance of the Function to delete
            alias from.
        :param ignore_missing: When False,
            `openstack.exceptions.ResourceNotFound`
            will be raised when the tag does not exist.
            When True, no exception will be set when attempting
            to delete a nonexistent event.
        :returns: ``None``
        """
        function = self._get_resource(_function.Function, function)
        if function.id is not None:
            function_urn = function.id.rpartition(":")[0]
        else:
            function_urn = function.func_urn.rpartition(":")[0]
        return self._delete(
            _async.Notification,
            function_urn=function_urn, ignore_missing=ignore_missing,
        )

    def all_versions_async_notifications(self, function, **query):
        """List asynchronous invocation setting of all function versions.

        :param function: Function instance or function URN
        :returns: A generator of Notification instances.
        """
        function = self._get_resource(_function.Function, function)
        if function.id is not None:
            function_urn = function.id
        else:
            function_urn = function.func_urn
        return self._list(
            _async.Notification,
            function_urn=function_urn,
            **query)

    def async_invocation_requests(self, function, **query):
        """Get asynchronous invocation requests of a function.

        :param function: Function instance or function URN
        :returns: instance of Requests
        """
        function = self._get_resource(_function.Function, function)
        if function.id is not None:
            function_urn = function.id.rpartition(":")[0]
        else:
            function_urn = function.func_urn.rpartition(":")[0]
        return self._list(
            _async.Requests,
            function_urn=function_urn,
            **query
        )

    def stop_async_invocation_request(self, function, **attrs):
        """Stop asynchronous invocation request of a function.

        :param function: Function instance or function URN
        :returns: instance of Requests
        """
        function = self._get_resource(_function.Function, function)
        stop = self._get_resource(_async.Requests, "")
        if function.id is not None:
            function_urn = function.id.rpartition(":")[0]
        else:
            function_urn = function.func_urn.rpartition(":")[0]
        return stop._stop(self, function_urn=function_urn, **attrs)
