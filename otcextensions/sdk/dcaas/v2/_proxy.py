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

from otcextensions.sdk.dcaas.v2 import virtual_gateway as _virtual_gateway
from otcextensions.sdk.dcaas.v2 import connection as _connection
from otcextensions.sdk.dcaas.v2 import virtual_interface as _virtual_interface
from otcextensions.sdk.dcaas.v2 import endpoint_group as _endpoint_group


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Virtual gateways ========
    def virtual_gateways(self, **query):
        """Retrieve a generator of virtual gateways

        :returns: A generator of virtual gateways
         :class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`
         instances
        """
        return self._list(_virtual_gateway.VirtualGateway, **query)

    def create_virtual_gateway(self, **attrs):
        """Create a new virtual gateway from attributes

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`,
            comprised of the properties on the VirtualGateway class.
        :returns: The results of virtual gateway creation
        :rtype: :class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.
            VirtualGateway`
        """
        return self._create(_virtual_gateway.VirtualGateway,
                            prepend_key=False, **attrs)

    def get_virtual_gateway(self, virtual_gateway):
        """Get a virtual_gateway

        :param virtual_gateway: The value can be the ID of a virtual_gateway
             or a :class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.
             VirtualGateway` instance.
        :returns: Virtual gateway instance
        :rtype: :class:`~otcextensions.sdk.dcaasdcaas.v2.virtual_gateway.
            VirtualGateway`
        """
        return self._get(_virtual_gateway.VirtualGateway, virtual_gateway)

    def delete_virtual_gateway(self, virtual_gateway, ignore_missing=True):
        """Delete a virtual_gateway

        :param virtual_gateway: The value can be the ID of a virtual gateway
             or a :class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.
             VirtualGateway` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the virtual gateway does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent zone.

        :returns: `None`
        """
        return self._delete(_virtual_gateway.VirtualGateway, virtual_gateway,
                            ignore_missing=ignore_missing)

    def update_virtual_gateway(self, virtual_gateway, **attrs):
        """Update virtual gateway attributes

        :param virtual_gateway: The id or an instance of
            :class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`

        :rtype: :class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.
            VirtualGateway`
        """
        return self._update(_virtual_gateway.VirtualGateway,
                            virtual_gateway, **attrs)

    def find_virtual_gateway(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single virtual gateway

        :param name_or_id: The name or ID of a virtual gateway
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the zone does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent virtual gateway.

        :returns: ``None``
        """
        return self._find(_virtual_gateway.VirtualGateway, name_or_id,
                          ignore_missing=ignore_missing,
                          **attrs)

    # ======== Connections ========
    def connections(self, **query):
        """Retrieve a generator of connections

        :returns: A generator of connections
            :class:`~otcextensions.sdk.dcaas.v2.connection.Connection`
            instances
        """
        return self._list(_connection.Connection, **query)

    def create_connection(self, **attrs):
        """Create a new connection from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dcaas.v2.connection.Connection`,
            comprised of the properties on the Connection class.
        :returns: The results of connection creation
        :rtype: :class:`~otcextensions.sdk.dcaas.v2.connection.Connection`
        """
        return self._create(_connection.Connection, prepend_key=False, **attrs)

    def get_connection(self, connection):
        """Get a connection

        :param connection: The value can be the ID of a connection
             or a :class:`~otcextensions.sdk.dcaas.v2.connection.Connection`
             instance.
        :returns: Connection instance
        :rtype: :class:`~otcextensions.sdk.dcaas.v2.connection.Connection`
        """
        return self._get(_connection.Connection, connection)

    def delete_connection(self, connection, ignore_missing=True):
        """Delete a connection

        :param connection: The value can be the ID of a connection
             or a :class:`~otcextensions.sdk.dcaas.v2.connection.Connection`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the connection does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent connection.

        :returns: `None`
        """
        return self._delete(_connection.Connection, connection,
                            ignore_missing=ignore_missing)

    def update_connection(self, connection, **attrs):
        """Update connection attributes

        :param connection: The id or an instance of
            :class:`~otcextensions.sdk.dcaas.v2.connection.Connection`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.dcaas.v2.connection.Connection`

        :rtype:
            :class:`~otcextensions.sdk.dcaas.v2.connection.Connection`
        """
        return self._update(_connection.Connection, connection, **attrs)

    def find_connection(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single connection

        :param name_or_id: The name or ID of a connection
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the connection does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent connection.

        :returns: ``None``
        """
        return self._find(_connection.Connection, name_or_id,
                          ignore_missing=ignore_missing,
                          **attrs)

    # ======== Virtual interface ========
    def virtual_interfaces(self, **query):
        """Retrieve a generator of virtual interfaces

        :returns: A generator of virtual interfaces
            :class:`~otcextensions.sdk.dcaas.v2.virtual_interface.
            VirtualInterface` instances
        """
        return self._list(_virtual_interface.VirtualInterface, **query)

    def create_virtual_interface(self, **attrs):
        """Create a new virtual interface from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dcaas.v2.virtual_interface.
            VirtualInterface`, comprised of the properties on the Connection
            class.
        :returns: The results of virtual interface creation
        :rtype: :class:`~otcextensions.sdk.dcaas.v2.virtual_interface.
            VirtualInterface`
        """
        return self._create(_virtual_interface.VirtualInterface,
                            prepend_key=False, **attrs)

    def get_virtual_interface(self, virtual_interface):
        """Get a virtual_interface

        :param virtual_interface: The value can be the ID of a
            virtual_interface or a :class:`~otcextensions.sdk.dcaas.v2.
            virtual_interface.VirtualInterface` instance.
        :returns: Virtual interface instance
        :rtype:
            :class:`~otcextensions.sdk.dcaas.v2.virtual_interface.
            VirtualInterface`
        """
        return self._get(_virtual_interface.VirtualInterface,
                         virtual_interface)

    def delete_virtual_interface(self, virtual_interface, ignore_missing=True):
        """Delete a virtual interface

        :param virtual_interface: The value can be the ID of a virtual
            interface or a :class:`~otcextensions.sdk.dcaas.v2.
            virtual_interface.VirtualInterface` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the virtual interface does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent virtual interface.

        :returns: `None`
        """
        return self._delete(_virtual_interface.VirtualInterface,
                            virtual_interface, ignore_missing=ignore_missing)

    def update_virtual_interface(self, virtual_interface, **attrs):
        """Update virtual interface attributes

        :param virtual_interface: The id or an instance of
            :class:`~otcextensions.sdk.dcaas.v2.virtual_interface.
            VirtualInterface`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.dcaas.v2.virtual_interface.
            VirtualInterface`

        :rtype: :class:`~otcextensions.sdk.dcaas.v2.virtual_interface.
            VirtualInterface`
        """
        return self._update(_virtual_interface.VirtualInterface,
                            virtual_interface, **attrs)

    def find_virtual_interface(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single virtual interface

        :param name_or_id: The name or ID of a virtual interface
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the virtual interface does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent virtual interface.

        :returns: ``None``
        """
        return self._find(_virtual_interface.VirtualInterface, name_or_id,
                          ignore_missing=ignore_missing,
                          **attrs)

    # ======== Direct Connect Endpoint Group ========
    def endpoint_groups(self, **query):
        """Retrieve a generator of direct connect endpoint groups.

        :returns: A generator of direct connect endpoint groups.
            :class:`~otcextensions.sdk.dcaas.v2.endpoint_group.
                DirectConnectEndpointGroup` instances
        """
        return self._list(_endpoint_group.DirectConnectEndpointGroup, **query)

    def create_endpoint_group(self, **attrs):
        """Create a new direct connect endpoint group from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dcaas.v2.endpoint_group.
            DirectConnectEndpointGroup`, comprised of the properties on the
            DirectConnectEndpointGroup class.
        :returns: The results of endpoint group creation
        :rtype: :class:`~otcextensions.sdk.dcaas.v2.endpoint_group.
            DirectConnectEndpointGroup`
        """
        return self._create(_endpoint_group.DirectConnectEndpointGroup,
                            prepend_key=False, **attrs)

    def get_endpoint_group(self, endpoint_group):
        """Get a direct connect endpoint group.

        :param endpoint_group: The value can be the ID of a
            endpoint group or a :class:`~otcextensions.sdk.dcaas.v2.
            endpoint_group.DirectConnectEndpointGroup` instance.
        :returns: Endpoint Group instance
        :rtype:
            :class:`~otcextensions.sdk.dcaas.v2.endpoint_group.
            DirectConnectEndpointGroup`
        """
        return self._get(_endpoint_group.DirectConnectEndpointGroup,
                         endpoint_group)

    def delete_endpoint_group(self, endpoint_group, ignore_missing=True):
        """Delete a Direct Connect Endpoint Group.

        :param endpoint_group: The value can be the ID of a endpoint
            group or a :class:`~otcextensions.sdk.dcaas.v2.
            endpoint_group.DirectConnectEndpointGroup` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the endpoint group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent endpoint group.

        :returns: `None`
        """
        return self._delete(_endpoint_group.DirectConnectEndpointGroup,
                            endpoint_group, ignore_missing=ignore_missing)

    def update_endpoint_group(self, endpoint_group, **attrs):
        """Update Direct Connect Endpoint Group attributes

        :param endpoint_group: The id or an instance of
            :class:`~otcextensions.sdk.dcaas.v2.endpoint_group.
            DirectConnectEndpointGroup`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.dcaas.v2.endpoint_group.
            DirectConnectEndpointGroup`

        :rtype: :class:`~otcextensions.sdk.dcaas.v2.endpoint_group.
            DirectConnectEndpointGroup`
        """
        return self._update(_endpoint_group.DirectConnectEndpointGroup,
                            endpoint_group, **attrs)

    def find_endpoint_group(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single Endpoint Group.

        :param name_or_id: The name or ID of a endpoint group.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the endpoint group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent endpoint group.

        :returns: ``None``
        """
        return self._find(_endpoint_group.DirectConnectEndpointGroup,
                          name_or_id, ignore_missing=ignore_missing,
                          **attrs)
