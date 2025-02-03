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
        return self._list(_d.Dependency, query)

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
        return self._list(_d.Dependency, query, base_path=base_path)

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
