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
        :rtype: :class:
            `~otcextensions.sdk.function_graph.v2.dependency.Dependency`
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
