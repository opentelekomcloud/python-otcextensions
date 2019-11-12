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
from otcextensions.sdk.nat.v2 import nat_gateway as _nat_gateway

from openstack import proxy

class Proxy(proxy.Proxy):

# NAT Gateway

    def create_gateway(self, **attrs):
        """Create a new gateway from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.nat.v2.nat_gateway.NatGateway`
        """
        return self._create(_nat_gateway.NatGateway, **attrs)

    def delete_gateway(self, id):
        """Create a new gateway from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.nat.v2.nat_gateway.NatGateway`
        """
        return self._delete(_nat_gateway.NatGateway, id=id)

    def gateways(self, **attrs):
        """Return a generator of NAT Gateways

        :param kwargs query: Optional query parameters to be sent to limit
            the resources being returned.
        :returns: A generator of NAT Gateway objects
        :rtype: :class:`~otcextensions.sdk.nat.v2.nat_gateway.NatGateway`
        """
        return self._list(_nat_gateway.NatGateway, **attrs)

    def get_nat_gateway(self, nat_gateway):
        """Get a single Nat Gateway

        :param nat_gateway: The value can be the ID of a NAT Gatway or a
                        :class:`~otcextensions.sdk.nat.v2.nat_gateway.NatGateway`
                        instance.

        :returns: One :class:`~otcextensions.sdk.nat.v2.nat_gateway.NatGateway`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_nat_gateway.NatGateway, nat_gateway)

    def update_nat_gateway(self, nat_gateway, **attrs):
        """Update a NAT Gateway

        :param nat_gateway: Either the ID of a NAT Gateway or a
                       :class:`~otcextensions.sdk.nat.v2.nat_gateway.NatGateway` instance.
        :attrs kwargs: The attributes to update on the server represented
                       by ``server``.

        :returns: The updated NAT Gateway
        :rtype: :class:`~otcextensions.sdk.nat.v2.nat_gateway.NatGateway`
        """
        return self._update(_server.Server, server, **attrs)
