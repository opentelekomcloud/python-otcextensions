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
from openstack import resource

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
            a :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`,
            comprised of the properties on the Gateway class.

        :returns: The results of the Gateway Creation

        :rtype: :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
        """
        return self._create(_gateway.Gateway, **attrs)

    def delete_gateway(self, gateway, ignore_missing=True):
        """Delete a gateway

        :param gateway: The value can be the ID of a NAT Gatway or a
            :class:`~otcextensions.sdk.nat.v2.gateway.Gateway` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the gateway does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent gateway.

        :returns: ``None``
        """
        return self._delete(_gateway.Gateway, gateway,
                            ignore_missing=ignore_missing)

    def wait_for_gateway(self, gateway, status='ACTIVE', failures=None,
                         interval=2, wait=300, attribute='status'):
        """Wait for an gateway to be in a particular status.

        :param gateway:
            The :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
            or gateway ID to wait on to reach the specified status.
        :param status: Desired status.
        :param failures:
            Statuses that would be interpreted as failures.
        :type failures: :py:class:`list`
        :param int interval:
            Number of seconds to wait before to consecutive checks.
            Default to 2.
        :param int wait:
            Maximum number of seconds to wait before the change.
            Default to 180
        :return: The resource is returned on success.
        :raises: :class:`~openstack.exceptions.ResourceTimeout` if transition
                 to the desired status failed to occur in specified seconds.
        :raises: :class:`~openstack.exceptions.ResourceFailure` if the resource
                 has transited to one of the failure statuses.
        """
        failures = ['INACTIVE'] if failures is None else failures
        return resource.wait_for_status(
            self, gateway, status, failures, interval, wait)

    def wait_for_delete_gateway(self, gateway, interval=2, wait=180):
        """Wait for the gateway to be deleted.

        :param gateway:
            The :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
            or instance ID to wait on to be deleted.
        :param int interval:
            Number of seconds to wait before to consecutive checks.
            Default to 2.
        :param int wait:
            Maximum number of seconds to wait for the delete.
            Default to 180.
        :return: Method returns self on success.
        :raises: :class:`~openstack.exceptions.ResourceTimeout` transition
                 to status failed to occur in wait seconds.
        """
        gateway = self._get_resource(_gateway.Gateway, gateway)
        return resource.wait_for_delete(self, gateway, interval, wait)

    def gateways(self, **query):
        """Return a generator of gateways

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of gateway objects.
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

        :param gateway: The value can be either the ID of a gateway or a
            :class:`~otcextensions.sdk.nat.v2.gateway.Gateway` instance.
        :param dict attrs: The attributes to update on the gateway represented
            by ``gateway``.

        :returns: The updated gateway.

        :rtype: :class:`~otcextensions.sdk.nat.v2.gateway.Gateway`
        """
        return self._update(_gateway.Gateway, gateway, **attrs)

    def find_gateway(self, name_or_id, ignore_missing=False):
        """Find a single gateway

        :param name_or_id: The name or ID of a gateway
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the gateway does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent gateway.

        :returns:
            One :class:`~otcextensions.sdk.nat.v2.gateway.Gateway` or ``None``
        """
        return self._find(_gateway.Gateway, name_or_id,
                          ignore_missing=ignore_missing)

    # ======== SNAT rules ========
    def create_snat_rule(self, **attrs):
        """Create a new SNAT rule from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.nat.v2.snat.Snat`, comprised of the
            properties on the Snat class.

        :returns: The result of Snat rule creation

        :rtype: :class:`~otcextensions.sdk.nat.v2.snat.Snat`
        """
        return self._create(_snat.Snat, **attrs)

    def delete_snat_rule(self, snat, ignore_missing=True):
        """Delete a SNAT rule

        :param gateway: The value can be the ID of a snat rule or a
            :class:`~otcextensions.sdk.nat.v2.snat.Snat` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the snat rule does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent snat rule.

        :returns: ``None``
        """
        return self._delete(_snat.Snat, snat, ignore_missing=ignore_missing)

    def get_snat_rule(self, snat_rule):
        """Get a single SNAT rule

        :param snat_rule: The value can be the ID of a snat rule or a
            :class:`~otcextensions.sdk.nat.v2.snat.Snat` instance.

        :returns: One :class:`~otcextensions.sdk.nat.v2.snat.Snat`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_snat.Snat, snat_rule)

    def snat_rules(self, **query):
        """Return a generator of SNAT rules

        :param dict query: Optional query parameters to be sent to limit
            the snat rules being returned.

        :returns: A generator of Snat objects.
        """
        return self._list(_snat.Snat, **query)

    def wait_for_snat(self, snat, status='ACTIVE', failures=None,
                         interval=2, wait=300, attribute='status'):
        """Wait for an snat rule to be in a particular status.

        :param snat:
            The :class:`~otcextensions.sdk.nat.v2.snat.Snat`
            or snat ID to wait on to reach the specified status.
        :param status: Desired status.
        :param failures:
            Statuses that would be interpreted as failures.
        :type failures: :py:class:`list`
        :param int interval:
            Number of seconds to wait before to consecutive checks.
            Default to 2.
        :param int wait:
            Maximum number of seconds to wait before the change.
            Default to 180
        :return: The resource is returned on success.
        :raises: :class:`~openstack.exceptions.ResourceTimeout` if transition
                 to the desired status failed to occur in specified seconds.
        :raises: :class:`~openstack.exceptions.ResourceFailure` if the resource
                 has transited to one of the failure statuses.
        """
        failures = ['INACTIVE'] if failures is None else failures
        return resource.wait_for_status(
            self, snat, status, failures, interval, wait)

    def wait_for_delete_snat(self, snat, interval=2, wait=180):
        """Wait for the snat rule to be deleted.

        :param gateway:
            The :class:`~otcextensions.sdk.nat.v2.snat.Snat`
            or instance ID to wait on to be deleted.
        :param int interval:
            Number of seconds to wait before to consecutive checks.
            Default to 2.
        :param int wait:
            Maximum number of seconds to wait for the delete.
            Default to 180.
        :return: Method returns self on success.
        :raises: :class:`~openstack.exceptions.ResourceTimeout` transition
                 to status failed to occur in wait seconds.
        """
        snat = self._get_resource(_snat.Snat, snat)
        return resource.wait_for_delete(self, snat, interval, wait)

    # ======== DNAT rules ========
    def create_dnat_rule(self, **attrs):
        """Create a new DNAT rule from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.nat.v2.dnat.Dnat`, comprised of the
            properties on the Dnat class.

        :returns: The result of Dnat rule creation.

        :rtype: :class:`~otcextensions.sdk.nat.v2.dnat.Dnat`
        """
        return self._create(_dnat.Dnat, **attrs)

    def delete_dnat_rule(self, dnat, ignore_missing=True):
        """Delete a DNAT rule

        :param gateway: The value can be the ID of a dnat rule or a
            :class:`~otcextensions.sdk.nat.v2.dnat.Dnat` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the dnat rule does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent dnat rule.

        :returns: ``None``
        """
        return self._delete(_dnat.Dnat, dnat, ignore_missing=ignore_missing)

    def get_dnat_rule(self, dnat_rule):
        """Get a single DNAT rule

        :param snat_rule: The value can be the ID of a dnat rule or a
            :class:`~otcextensions.sdk.nat.v2.dnat.Dnat` instance.

        :returns: One :class:`~otcextensions.sdk.nat.v2.dnat.Dnat`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_dnat.Dnat, dnat_rule)

    def dnat_rules(self, **query):
        """Return a generator of DNAT rules

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of Dnat objects.
        """
        return self._list(_dnat.Dnat, **query)

    # ======== Project cleanup ========
    def _get_cleanup_dependencies(self):
        return {
            'nat': {
                'before': ['network']
            }
        }

    def _service_cleanup(self, dry_run=True, client_status_queue=None,
                         identified_resources=None,
                         filters=None, resource_evaluation_fn=None):
        for obj in self.gateways():
            need_delete = self._service_cleanup_del_res(
                self.delete_gateway,
                obj,
                dry_run=dry_run,
                client_status_queue=client_status_queue,
                identified_resources=identified_resources,
                filters=filters,
                resource_evaluation_fn=resource_evaluation_fn)
            if dry_run and need_delete:
                for port in self._connection.network.ports(device_id=obj.id):
                    identified_resources[port.id] = port
