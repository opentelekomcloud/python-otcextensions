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
from otcextensions.sdk.vpcep.v1 import endpoint as _endpoint
from otcextensions.sdk.vpcep.v1 import endpoint_service as _endpoint_service

from openstack import proxy


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Endpoint Service ========
    def create_endpoint_service(self, **attrs):
        """Create a new endpoint_service from attributes

        :param dict attrs: Keyword arguments which will be used to create a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`
          ,comprised of the properties on the EndpointService class.

        :returns: The results of the EndpointService Creation

        :rtype:
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`
        """
        return self._create(_endpoint_service.EndpointService, **attrs)

    def delete_endpoint_service(self, endpoint_service, ignore_missing=True):
        """Delete a endpoint_service

        :param endpoint_service:
          The value can be the ID of a Endpoint Service or a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`
          instance.
        :param bool ignore_missing: When set to ``False``
          :class:`~openstack.exceptions.ResourceNotFound` will be raised when
          the endpoint_service does not exist.
          When set to ``True``, no exception will be set when attempting to
          delete a nonexistent endpoint_service.

        :returns: ``None``
        """
        return self._delete(_endpoint_service.EndpointService,
                            endpoint_service, ignore_missing=ignore_missing)

    def endpoint_services(self, **query):
        """Return a generator of endpoint_services

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of endpoint_service objects.
        """
        return self._list(_endpoint_service.EndpointService, **query)

    def get_endpoint_service(self, endpoint_service):
        """Get a single endpoint_service

        :param endpoint_service:
          The value can be the ID of a Endpoint Service or a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`
          instance.

        :returns: One
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
          when no resource can be found.
        """
        return self._get(_endpoint_service.EndpointService, endpoint_service)

    def update_endpoint_service(self, endpoint_service, **attrs):
        """Update a endpoint_service

        :param endpoint_service:
          The value can be either the ID of a endpoint_service or a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`
          instance.
        :param dict attrs: The attributes to update on the
          endpoint_service represented by ``endpoint_service``.

        :returns: The updated endpoint_service.

        :rtype:
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`
        """
        return self._update(_endpoint_service.EndpointService,
                            endpoint_service, **attrs)

    def connections(self, endpoint_service, **params):
        """Return a generator of endpoint_service connections

        :param endpoint_service:
          The value can be the ID of a Endpoint Service or a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`
          instance.
        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of endpoint_service Connection objects.
        """
        endpoint_service = self._get_resource(
            _endpoint_service.EndpointService,
            endpoint_service)
        return self._list(_endpoint_service.Connection,
                          endpoint_service_id=endpoint_service.id,
                          **params)

    def manage_connection(self,
                          endpoint_service,
                          endpoints,
                          action):
        """Return a generator of endpoint_service_connections

        :param endpoint_service:
          The value can be the ID of a Endpoint Service or a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`
          instance.
        :param lists: List of VPC Endpoints Id.
        :param action: Specifies whether to receive or reject a VPC endpoint
          connection for a VPC endpoint service.

        :returns: A generator of
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.Connection`
          instance.
        """

        endpoint_service = self._get_resource(
            _endpoint_service.EndpointService,
            endpoint_service
        )

        connection = self._get_resource(
            _endpoint_service.Connection, None,
            endpoint_service_id=endpoint_service.id,
        )
        return connection._manage_connection(
            self, endpoints, action)

    def whitelist(self, endpoint_service, **params):
        """Return a generator of vpc endpoint service whitelist

        :param endpoint_service:
          The value can be the ID of a Endpoint Service or a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.EndpointService`
          instance.
        :param dict query: Optional query parameters to be sent to limit
          the resources being returned.

        :returns: A generator of endpoint_service Whitelist objects.
        """
        endpoint_service = self._get_resource(
            _endpoint_service.EndpointService,
            endpoint_service)

        return self._list(_endpoint_service.Whitelist,
                          endpoint_service_id=endpoint_service.id,
                          **params)

    def manage_whitelist(self,
                         endpoint_service,
                         domains,
                         action):
        """Return a generator of endpoint_service_connections

        :param endpoint_service:
          The value can be the ID of a Endpoint Service or a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.Whitelist`
          instance.
        :param demains: List of Domain IDs to be added or removed
          from whitelist of a VPC Endpoint Service.
        :param action: Specifies whether to add or remove the domains
          from whitelist for a VPC endpoint service.

        :returns: A generator of
          :class:`~otcextensions.sdk.vpcep.v1.endpoint_service.Whitelist`
          instance.
        """
        endpoint_service = self._get_resource(
            _endpoint_service.EndpointService,
            endpoint_service
        )

        whitelist = self._get_resource(
            _endpoint_service.Whitelist, None,
            endpoint_service_id=endpoint_service.id,
        )
        return whitelist._manage_whitelist(self, domains, action)

    # ======== VPC Endpoint ========

    def create_endpoint(self, **attrs):
        """Create a new VPC Endpoint from attributes

        :param dict attrs: Keyword arguments which will be used to create
          a :class:`~otcextensions.sdk.vpcep.v1.endpoint.Endpoint`,
          comprised of the properties on the Endpoint class.

        :returns: The result of Endpoint rule creation

        :rtype: :class:`~otcextensions.sdk.vpcep.v1.endpoint.Endpoint`
        """
        return self._create(_endpoint.Endpoint, **attrs)

    def delete_endpoint(self, endpoint, ignore_missing=True):
        """Delete a VPC Endpoint

        :param endpoint: The value can be the ID of a VPC Endpoint or a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint.Endpoint` instance.
        :param bool ignore_missing: When set to ``False``
          :class:`~openstack.exceptions.ResourceNotFound` will be raised when
          the VPC Endpoint does not exist.
          When set to ``True``, no exception will be set when attempting to
          delete a nonexistent VPC Endpoint.

        :returns: ``None``
        """
        return self._delete(_endpoint.Endpoint, endpoint,
                            ignore_missing=ignore_missing)

    def get_endpoint(self, endpoint):
        """Get a single VPC Endpoint

        :param endpoint: The value can be the ID of a VPC Endpoint or a
          :class:`~otcextensions.sdk.vpcep.v1.endpoint.Endpoint` instance.

        :returns: One :class:`~otcextensions.sdk.vpcep.v1.endpoint.Endpoint`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
          when no resource can be found.
        """
        return self._get(_endpoint.Endpoint, endpoint)

    def endpoints(self, **query):
        """Return a generator of VPC Endpoint

        :param dict query: Optional query parameters to be sent to limit
          the VPC Endpoints being returned.

        :returns: A generator of Endpoint objects.
        """
        return self._list(_endpoint.Endpoint, **query)
