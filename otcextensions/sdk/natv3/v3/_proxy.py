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
from otcextensions.sdk.natv3.v3 import dnat as _dnat
from otcextensions.sdk.natv3.v3 import gateway as _gateway


class Proxy(proxy.Proxy):

    skip_discovery = True

    def _extract_name(self, url, service_type=None, project_id=None):
        return extract_url_parts(url, project_id)

    def private_nat_gateways(self, **query):
        """Return a generator of private NAT gateways.

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of private NAT gateway objects.
        """
        return self._list(_gateway.PrivateNatGateway, **query)

    def get_private_nat_gateway(self, gateway):
        """Get a single Private Nat gateway

        :param gateway: The value can be the ID of a NAT Gatway

        :returns: One :class:`~otcextensions.sdk.natv3.v3.gateway.PrivateNatGateway`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_gateway.PrivateNatGateway, gateway)

    def create_private_nat_gateway(self, **attrs):
        """Create a new Private gateway from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`,
            comprised of the properties on the Gateway class.

        :returns: The results of the Gateway Creation

        :rtype: :class:`~otcextensions.sdk.nat.v3.gateway.PrivateNatGateway`
        """
        return self._create(_gateway.PrivateNatGateway, **attrs)

    def update_private_nat_gateway(self, gateway, **attrs):
        """Update a Private Nat gateway

        :param gateway: The value can be either the ID of a gateway or a
            :class:`~otcextensions.sdk.natv3.v3.gateway.PrivateNatGateway` instance.
        :param dict attrs: The attributes to update on the gateway represented
            by ``gateway``.

        :returns: The updated gateway.

        :rtype: :class:`~otcextensions.sdk.natv3.v3.gateway.PrivateNatGateway`
        """
        return self._update(_gateway.PrivateNatGateway, gateway, **attrs)

    def delete_private_nat_gateway(self, gateway, ignore_missing=True):
        """Delete a Private Nat gateway
        :param gateway: The value can be the ID or a
            :class:`~otcextensions.sdk.natv3.v3.gateway.PrivateNatGateway` instance.`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the gateway does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent gateway.
        :returns: None
        """

        return self._delete(
            _gateway.PrivateNatGateway, gateway, ignore_missing=ignore_missing
        )

    # ======== DNAT rules ========

    def private_dnat_rules(self, **query):
        """Query DNAT rules of a private NAT gateway.

        This API is used to query DNAT rules.

        :param kwargs query: Optional query parameters to filter the results.
            Supported parameters include:
            limit, marker, page_reverse, id, project_id,
            enterprise_project_id, description, gateway_id,
            transit_ip_id, external_ip_address, network_interface_id,
            type, private_ip_address, protocol,
            internal_service_port, transit_service_port,
            created_at, updated_at

        :returns: A generator of :class:`~otcextensions.sdk.nat_gateway.v3.dnat.Dnat`
        """
        return self._list(_dnat.PrivateDnat, **query)

    def create_private_dnat_rule(self, **attrs):
        """Create a private DNAT rule from attributes.

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.natv3.v3.dnat.PrivateDnat`,
            comprised of the properties on the PrivateDnat class.

        :returns: The result of private DNAT rule creation.

        :rtype: :class:`~otcextensions.sdk.natv3.v3.dnat.PrivateDnat`
        """
        return self._create(_dnat.PrivateDnat, **attrs)

    def get_private_dnat_rule(self, dnat_rule):
        """Get a single private DNAT rule.

        :param dnat_rule: The value can be the ID of a private DNAT rule.

        :returns: One :class:`~otcextensions.sdk.natv3.v3.dnat.PrivateDnat`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_dnat.PrivateDnat, dnat_rule)
