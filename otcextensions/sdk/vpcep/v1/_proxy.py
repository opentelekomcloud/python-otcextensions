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
#
from openstack import exceptions
from openstack import proxy
from otcextensions.sdk.vpcep.v1 import connection as _connection
from otcextensions.sdk.vpcep.v1 import endpoint as _endpoint
from otcextensions.sdk.vpcep.v1 import quota as _quota
from otcextensions.sdk.vpcep.v1 import service as _service
from otcextensions.sdk.vpcep.v1 import whitelist as _whitelist


class Proxy(proxy.Proxy):
    skip_discovery = True

    # ======== VPC Endpoint ========

    def endpoints(self, **query):
        """Return a generator of endpoints

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned. Valid parameters are:
        :returns: A generator of endpoint objects
        :rtype: :class:`~otcextensions.sdk.vpcep.endpoint.Endpoint`
        """
        if query.get('limit'):
            query.update(paginated=False)
        return self._list(_endpoint.Endpoint, **query)

    def create_endpoint(self, **attrs):
        """Create a new endpoint from attributes

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.vpcep.endpoint.Endpoint`,
            comprised of the properties on the Endpoint class.

        :returns: The results of endpoint creation
        :rtype: :class:`~otcextensions.sdk.vpcep.endpoint.Endpoint`
        """
        if attrs.get('ip') and attrs.get('port_ip'):
            raise TypeError(
                "You can use either the 'ip' or the 'port_ip' keyword argument"
            )
        elif attrs.get('ip'):
            attrs['port_ip'] = attrs['ip']
            del attrs['ip']
        return self._create(_endpoint.Endpoint, **attrs)

    def get_endpoint(self, endpoint):
        """Get a single endpoint

        :param endpoint: The value can be the ID of a endpoint or a
            :class:`~otcextensions.sdk.vpcep.endpoint.Endpoint`
            instance.

        :returns: One :class:`~otcextensions.sdk.vpcep.endpoint.Endpoint`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.

        """
        return self._get(_endpoint.Endpoint, endpoint)

    def delete_endpoint(self, endpoint, ignore_missing=True):
        """Delete a endpoint

        :param endpoint: The value can be either the ID of a endpoint or a
            :class:`~otcextensions.sdk.vpcep.endpoint.Endpoint` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the endpoint does not exist.
            When set to ``True``, no exception will be set when
            attempting to delete a nonexistent endpoint.

        :returns: ``None``
        """
        return self._delete(
            _endpoint.Endpoint, endpoint, ignore_missing=ignore_missing
        )

    # ======== Endpoint Service ========

    def services(self, **query):
        """Return a generator of endpoint services

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned. Valid parameters are:

        :returns: A generator of endpoint service objects
        :rtype: :class:`~otcextensions.sdk.vpcep.service.Service`
        """
        if query.get('limit'):
            query.update(paginated=False)
        return self._list(_service.Service, **query)

    def create_service(self, **attrs):
        """Create a new endpoint service from attributes

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.vpcep.service.Service`,
            comprised of the properties on the Service class.

        :returns: The results of endpoint service creation
        :rtype: :class:`~otcextensions.sdk.vpcep.service.Service`
        """
        return self._create(_service.Service, **attrs)

    def get_service(self, service):
        """Get a single endpoint service

        :param service: The value can be the ID of a endpoint service or a
            :class:`~otcextensions.sdk.vpcep.service.Service`
            instance.

        :returns: One :class:`~otcextensions.sdk.vpcep.service.Service`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.

        """
        return self._get(_service.Service, service)

    def find_service(self, name_or_id, ignore_missing=False):
        """Find a single endpoint service

        :param name_or_id: The name or ID of a service.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the resource does not exist.
            When set to ``True``, None will be returned when
            attempting to find a nonexistent resource.

        :returns: One :class:`~otcextensions.sdk.vpcep.service.Service`
            or None
        """
        return self._find(
            _service.Service,
            name_or_id,
            ignore_missing=ignore_missing,
        )

    def update_service(self, service, **attrs):
        """Update a endpoint service

        :param service: The service can be either the ID or a
            :class:`~otcextensions.sdk.vpcep.service.Service` instance.
        :param dict attrs: The attributes to update on the endpoint service
            represented by ``service``.

        :returns: The updated service
        :rtype: :class:`~otcextensions.sdk.vpcep.service.Service`
        """
        return self._update(_service.Service, service, **attrs)

    def delete_service(self, service, ignore_missing=True):
        """Delete a endpoint service

        :param service: The service can be either the ID or a
            :class:`~otcextensions.sdk.vpcep.service.Service` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the service does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent service.

        :returns: ``None``
        """
        return self._delete(
            _service.Service,
            service,
            ignore_missing=ignore_missing,
        )

    # ======== Endpoint Service Connections ========

    def service_connections(self, service, **query):
        """Return a generator of service connections

        :param service: The service can be either the ID or a
            :class:`~otcextensions.sdk.vpcep.service.Service` instance.
        :param dict query: Optional query parameters to be sent to limit
            the resources being returned. Valid parameters are:

        :returns: A generator of connection objects.
        :rtype: :class:`~otcextensions.sdk.vpcep.connection.Connection`
        """
        if query.get('limit'):
            query.update(paginated=False)
        endpoint_service = self._get_resource(_service.Service, service)
        return self._list(
            _connection.Connection,
            endpoint_service_id=endpoint_service.id,
            **query
        )

    def manage_service_connections(self, service, action, endpoints=[]):
        """Manage endpoint service connections

        :param service: The service can be either the ID or a
            :class:`~otcextensions.sdk.vpcep.service.Service` instance.
        :param action: action can be ``accept`` or ``reject``.
        :param endpoints: List of VPC Endpoints Id.

        :returns: A generator of connection objects.
        :rtype: :class:`~otcextensions.sdk.vpcep.connection.Connection`
        """

        endpoint_service = self._get_resource(_service.Service, service)
        connection = self._get_resource(
            _connection.Connection,
            None,
            endpoint_service_id=endpoint_service.id,
        )
        if action in ('accept', 'receive'):
            return connection.accept(self, endpoints)
        elif action == 'reject':
            return connection.reject(self, endpoints)
        raise exceptions.SDKException(
            "Value of action can be 'accept' or 'reject'."
        )

    # ======== Endpoint Service Whitelist ========

    def service_whitelist(self, service, **query):
        """Return a generator of service whitelist

        :param service: The service can be either the ID or a
            :class:`~otcextensions.sdk.vpcep.service.Service` instance.
        :param dict query: Optional query parameters to be sent to limit
            the resources being returned. Valid parameters are:

        :returns: A generator of whitelist objects.
        :rtype: :class:`~otcextensions.sdk.vpcep.whitelist.Whitelist`
        """
        if query.get('limit'):
            query.update(paginated=False)
        endpoint_service = self._get_resource(_service.Service, service)
        return self._list(
            _whitelist.Whitelist,
            endpoint_service_id=endpoint_service.id,
            **query
        )

    def manage_service_whitelist(self, service, action, domains=[]):
        """Manage endpoint service whitelist

        :param service: The service can be either the ID or a
            :class:`~otcextensions.sdk.vpcep.service.Service` instance.
        :param action: action can be ``add`` or ``remove``.
        :param domains: List of domains Ids to be added to whitelist.

        :returns: A generator of whitelist objects.
        :rtype: :class:`~otcextensions.sdk.vpcep.whitelist.Whitelist`
        """
        endpoint_service = self._get_resource(_service.Service, service)
        whitelist = self._get_resource(
            _whitelist.Whitelist,
            None,
            endpoint_service_id=endpoint_service.id,
        )
        if action == 'add':
            return whitelist.add(self, domains)
        elif action == 'remove':
            return whitelist.remove(self, domains)
        raise exceptions.SDKException(
            "Value of action can be 'add' or 'remove'."
        )

    # ======== VPCEP Resource Quota  ========

    def resource_quota(self, type=None):
        """Return a generator of vpcep quota

        :param type: Specify the resource type. Value of
            type can be: ``endpoint`` or ``endpoint_service``

        :returns: A generator of quota objects.
        :rtype: :class:`~otcextensions.sdk.vpcep.quota.Quota`
        """
        query = {}
        if type:
            query.update(type=type)
        return self._list(_quota.Quota, **query)
