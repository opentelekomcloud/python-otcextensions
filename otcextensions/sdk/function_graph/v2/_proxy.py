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

        :param function: The instance of the Function to delete.
        :param bool ignore_missing: Whether to ignore if the function is missing.
        :returns: None
        """
        function = self._get_resource(_function.Function, function)
        return function._delete_function(self, function)

    def functions(self, **query):
        """List all functions with optional filters.

        :param dict query: Query parameters to filter the function list.
        :returns: A generator of Function instances.
        """
        return self._list(_function.Function, **query)

    def get_function(self, function):
        """Get details of a single function.

        :param function: The ID or instance of the Function to retrieve.
        :returns: The Function instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        return self._get(_function.Function, function)

    def update_function(self, function, **attrs):
        """Update a function's attributes.

        :param function: The ID or instance of the Function to update.
        :param dict attrs: Attributes to update on the function.
        :returns: The updated Function instance.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        return self._update(_function.Function, function, **attrs)

    def find_function(self, name_or_id, ignore_missing=False):
        """Find a function by name or ID.

        :param name_or_id: The name or ID of the Function.
        :param bool ignore_missing: Whether to ignore if the function is missing.
        :returns: The Function instance or None.
        :rtype: :class:`~otcextensions.sdk.function_graph.v2.function.Function`
        """
        return self._find(_function.Function, name_or_id,
                          ignore_missing=ignore_missing)
