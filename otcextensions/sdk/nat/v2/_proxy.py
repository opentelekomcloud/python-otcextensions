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
from otcextensions.sdk.nat.v2 import gateway as _gateway
from otcextensions.sdk.nat.v2 import snat as _snat
from otcextensions.sdk.nat.v2 import dnat as _dnat

from openstack import proxy


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Gateway ========
    def create_gateway(self, **attrs):
        """Create a new gateway from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
        """
        return self._create(_gateway.Gateway, **attrs)

    def delete_gateway(self, gateway, ignore_missing=True):
        """Delete a gateway

        :param gateway: key id or an instance of
            :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the gateway does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent gateway.

        :returns: Gateway been deleted
        :rtype: :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
        """
        return self._delete(_gateway.Gateway, gateway,
                            ignore_missing=ignore_missing)

    def gateways(self, **query):
        """Return a generator of gateways

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.
        :returns: A generator of gateway objects
        :rtype: :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
        """
        return self._list(_gateway.Gateway, **query)

    def get_gateway(self, gateway):
        """Get a single gateway

        :param gateway: The value can be the ID of a NAT Gatway or a
                        :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
                        instance.

        :returns: One :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_gateway.Gateway, gateway)

    def update_gateway(self, gateway, **attrs):
        """Update a gateway

        :param gateway: Either the ID of a gateway or a
                       :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
                       instance.
        :param dict attrs: The attributes to update on the gateway represented
                       by ``gateway``.

        :returns: The updated gateway
        :rtype: :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
        """
        return self._update(_gateway.Gateway, gateway, **attrs)

    def find_gateway(self, name_or_id, ignore_missing=True):
        """Find a single Nat Gateway

        :param name_or_id: The name or ID of a zone
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the gateway does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent gateway.

        :returns: ``None``
        """
        return self._find(_gateway.Gateway, name_or_id,
                          ignore_missing=ignore_missing)

    # ======== SNAT rules ========
    def create_snat_rule(self, **attrs):
        """Create a new SNAT rule from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.nat.v2.snat.Snat`
        """
        return self._create(_snat.Snat, **attrs)

    def delete_snat_rule(self, snat, ignore_missing=True):
        """Delete a SNAT rule

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the SNAT rule does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent SNAT rule.

        :returns: SNAT rule been deleted
        :rtype: :class:`~otcextensions.sdk.nat.v2.snat.Snat`
        """
        return self._delete(_snat.Snat, snat, ignore_missing=ignore_missing)

    def get_snat_rule(self, snat_rule):
        """Get a single SNAT rule

        :param snat_rule: The value can be the ID of a SNAT rule or a
                        :class:`~otcextensions.sdk.nat.v2.snat.Snat`
                        instance.

        :returns: One :class:`~otcextensions.sdk.nat.v2.snat.Snat`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_snat.Snat, snat_rule)

    def snat_rules(self, **query):
        """Return a generator of SNAT rules

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.
        :returns: A generator of Snat rule objects
        :rtype: :class:`~otcextensions.sdk.nat.v2.snat.Snat`
        """
        return self._list(_snat.Snat, **query)

    # ======== DNAT rules ========
    def create_dnat_rule(self, **attrs):
        """Create a new DNAT rule from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.nat.v2.dnat.Dnat`
        """
        return self._create(_dnat.Dnat, **attrs)

    def delete_dnat_rule(self, dnat, ignore_missing=True):
        """Delete a DNAT rule

        :param dict attrs: Keyword arguments which will be used to delete
            a :class:`~otcextensions.sdk.nat.v2.dnat.Dnat`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the DNAT rule does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent DNAT rule.

        :returns: DNAT rule been deleted
        :rtype: :class:`~otcextensions.sdk.nat.v2.dnat.Dnat`
        """
        return self._delete(_dnat.Dnat, dnat, ignore_missing=ignore_missing)

    def get_dnat_rule(self, dnat_rule):
        """Get a single DNAT rule

        :param dnat_rule: The value can be the ID of a DNAT rule or a
                        :class:`~otcextensions.sdk.nat.v2.dnat.Dnat`
                        instance.

        :returns: One :class:`~otcextensions.sdk.nat.v2.dnat.Dnat`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_dnat.Dnat, dnat_rule)

    def dnat_rules(self, **query):
        """Return a generator of DNAT rules

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.
        :returns: A generator of DNAT rules objects
        :rtype: :class:`~otcextensions.sdk.nat.v2.dnat.Dnat`
        """
        return self._list(_dnat.Dnat, **query)
