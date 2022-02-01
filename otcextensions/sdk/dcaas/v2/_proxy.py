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

        :returns: Virtual gateway been deleted
        :rtype: :class:`~otcextensions.sdk.direct_conect.v2.virtual_gateway.
            VirtualGateway`
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
            to delete a nonexistent zone.

        :returns: ``None``
        """
        return self._find(_virtual_gateway.VirtualGateway, name_or_id,
                          ignore_missing=ignore_missing,
                          **attrs)
