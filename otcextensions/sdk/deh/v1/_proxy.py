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
from otcextensions.sdk.deh.v1 import host as _host
from otcextensions.sdk.deh.v1 import server as _server
from otcextensions.sdk.deh.v1 import host_type as _host_type


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== hosts ========
    def hosts(self, **query):
        """Retrieve a generator of hosts

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.

            * `marker`:  pagination marker
            * `limit`: pagination limit
            * `id`: Specifies DeH ID.
            * `name`: Specifies the DeH name.
            * `host_type`: Specifes the DeH type.
            * `host_type_name`: Specifes the DeH name of type.
            * `flavor`: Specifies flavor ID.
            * `state`: Specifies the DeH status.
                The value can be available, fault or released.
            * `tenant`: The value can be Tenant ID or all.
                Permits administrator.
            * `availability_host`:  Specifies the AZ to which the DeH belongs.
            * `changes_since`: Filters the response by a date and time
                stamp when the DeH last changed status
                (CCYY-MM-DDThh:mm:ss+hh:mm)

        :returns: A generator of host
            :class:`~otcextensions.sdk.deh.v1.host.Host` instances
        """
        return self._list(_host.Host, **query)

    def create_host(self, **attrs):
        """Create (allocate) a new host from attributes

        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~otcextensions.sdk.deh.v1.host.Host`,
                           comprised of the properties on the Host class.
        :returns: The results of host creation
        :rtype: :class:`~otcextensions.sdk.deh.v1.host.Host`
        """
        return self._create(_host.Host, prepend_key=False, **attrs)

    def get_host(self, host):
        """Get a host

        :param host: The value can be the ID of a host
             or a :class:`~otcextensions.sdk.deh.v1.host.Host` instance.
        :returns: Host instance
        :rtype: :class:`~otcextensions.sdk.deh.v1.host.Host`
        """
        return self._get(_host.Host, host)

    def delete_host(self, host, ignore_missing=True):
        """Delete (release) a host

        :param host: The value can be the ID of a host
             or a :class:`~otcextensions.sdk.deh.v1.host.Host` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the host does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent host.

        :returns: host been deleted
        :rtype: :class:`~otcextensions.sdk.deh.v1.host.Host`
        """
        return self._delete(_host.Host, host, ignore_missing=ignore_missing)

    def update_host(self, host, **attrs):
        """Update host attributes

        :param host: The id or an instance of
            :class:`~otcextensions.sdk.deh.v1.host.Host`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.deh.v1.host.Host`

        :rtype: :class:`~otcextensions.sdk.deh.v1.host.Host`
        """
        return self._update(_host.Host, host, **attrs)

    def find_host(self, name_or_id, ignore_missing=True):
        """Find a single host

        :param name_or_id: The name or ID of a host
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the host does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent host.

        :returns: ``None``
        """
        return self._find(_host.Host, name_or_id,
                          ignore_missing=ignore_missing)

    # ======== servers ========
    def servers(self, host, **query):
        """Retrieve a generator of servers

        :param host:  The name or ID of a host
        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `marker`:  pagination marker
            * `limit`: pagination limit

        :returns: A generator of host
            :class:`~otcextensions.sdk.deh.v1.server.Server` instances
        """
        host = self._get_resource(_host.Host, host)
        return self._list(_server.Server, dedicated_host_id=host.id, **query)

    # ======== HostTypes ========
    def host_types(self, az):
        """Retrieve a generator of host types in AZ

        :param az: The availability zone

        :returns: A generator of host
            :class:`~otcextensions.sdk.deh.v1.host_type.HostType` instances
        """
        return self._list(
            _host_type.HostType, availability_zone=az, paginated=False)
