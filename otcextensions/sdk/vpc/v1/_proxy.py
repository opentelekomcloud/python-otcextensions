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
from openstack import exceptions
from openstack import proxy, resource

from otcextensions.sdk.vpc.v1 import bandwidth as _bandwidth
from otcextensions.sdk.vpc.v1 import peering as _peering
from otcextensions.sdk.vpc.v1 import route as _route
from otcextensions.sdk.vpc.v1 import subnet as _subnet
from otcextensions.sdk.vpc.v1 import vpc as _vpc

from dataclasses import dataclass
from typing import List


@dataclass
class PublicInfo:
    publicip_id: str
    publicip_type: str


class Proxy(proxy.Proxy):
    skip_discovery = True

    # ======== Bandwidth ========
    def assign_bandwidth(self, **attrs):
        """Assign bandwidth

        :param dict attrs: Keyword arguments which will be used to assign
            a :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
        """
        project_id = self.get_project_id()
        version = 'v2.0'
        base_path = _bandwidth.Bandwidth.base_path % {'version': version,
                                                      'project_id': project_id}
        return self._create(_bandwidth.Bandwidth, project_id=project_id,
                            base_path=base_path, **attrs)

    def find_bandwidth(self, name_or_id, ignore_missing=False):
        """Find a single bandwidth

        :param name_or_id: The name or ID of a bandwidth
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the vpc peering does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent peering.

        :returns: One :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
        """
        project_id = self.get_project_id()
        version = 'v1'
        base_path = _bandwidth.Bandwidth.base_path % {'version': version,
                                                      'project_id': project_id}
        return self._find(
            _bandwidth.Bandwidth, name_or_id,
            project_id=project_id, base_path=base_path,
            ignore_missing=ignore_missing)

    def update_bandwidth(self, bandwidth, **attrs):
        """Update a vpc peering

        :param bandwidth: Either the ID of a vpc bandwidth or a
                       :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
                       instance.
        :param dict attrs: The attributes to update on the vpc bandwidth
            represented by ``bandwidth``.

        :returns: The updated bandwidth

        :rtype: :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
        """
        bandwidth = self._get_resource(_bandwidth.Bandwidth, bandwidth)
        project_id = self.get_project_id()
        version = 'v1'
        return bandwidth.update_bandwidth(
            self,
            project_id,
            version,
            **attrs)

    def add_eip_to_bandwidth(self, bandwidth, publicip_info: List[PublicInfo]):
        """Add an EIP to a shared bandwidth.

        :param bandwidth: The value can be the ID of a bandwidth
           or a :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
           instance.
        :param publicip_info: List of dictionaries in the format
           {'publicip_id': id, 'publicip_type': type}
        """
        bandwidth = self._get_resource(_bandwidth.Bandwidth, bandwidth)
        version = 'v2.0'
        return bandwidth.add_eip_to_bandwidth(
            self,
            version,
            publicip_info,
            project_id=self.get_project_id())

    def remove_eip_from_bandwidth(self, bandwidth, **attrs):
        """Add an EIP to a shared bandwidth.

        :param bandwidth: The value can be the ID of a bandwidth
             or a :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
             instance.
        :param attrs: Keyword arguments to remove eip: charge_mode, size,
            publicip_info - array of eip in the format {'publicip_id': id}
        """
        bandwidth = self._get_resource(_bandwidth.Bandwidth, bandwidth)
        project_id = self.get_project_id()
        version = 'v2.0'
        return bandwidth.remove_eip_from_bandwidth(
            self,
            project_id,
            version,
            **attrs)

    def delete_bandwidth(self, bandwidth, ignore_missing=True):
        """Delete a bandwidth

        :param bandwidth: key id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the vpc peering does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent peering.

        :returns: ``None``
        """
        project_id = self.get_project_id()
        version = 'v2.0'
        base_path = _bandwidth.Bandwidth.base_path % {'version': version,
                                                      'project_id': project_id}
        return self._delete(
            _bandwidth.Bandwidth, bandwidth,
            ignore_missing=ignore_missing, project_id=project_id,
            base_path=base_path)

    def wait_for_delete_bandwidth(self, bandwidth, interval=2, wait=60):
        """Wait for the bandwidth to be deleted.

        :param bandwidth:
            The :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
            or group ID to wait on to be deleted.
        :param int interval:
            Number of seconds to wait before to consecutive checks.
            Default to 2.
        :param int wait:
            Maximum number of seconds to wait for the delete.
            Default to 60.
        :return: Method returns self on success.
        :raises: :class:`~openstack.exceptions.ResourceTimeout` transition
                 to status failed to occur in wait seconds.
        """
        group = self._get_resource(_bandwidth.Bandwidth, bandwidth)
        return resource.wait_for_delete(self, group, interval, wait)

    # ======== Peering ========
    def create_peering(self, **attrs):
        """Create a new vpc peering from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vpc.v1.peering.Peering`
        """
        return self._create(_peering.Peering, **attrs)

    def delete_peering(self, peering, ignore_missing=True):
        """Delete a vpc peering

        :param peering: key id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.peering.Peering`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the vpc peering does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent peering.

        :returns: ``None``
        """
        return self._delete(
            _peering.Peering, peering,
            ignore_missing=ignore_missing)

    def peerings(self, **query):
        """Return a generator of vpc peerings

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of vpc peering objects

        :rtype: :class:`~otcextensions.sdk.vpc.v1.peering.Peering`
        """
        return self._list(_peering.Peering, **query)

    def get_peering(self, peering):
        """Get a single vpc peering

        :param peering: The value can be the ID of a vpc peering or a
                        :class:`~otcextensions.sdk.vpc.v1.peering.Peering`
                        instance.

        :returns: One :class:`~otcextensions.sdk.vpc.v1.peering.Peering`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_peering.Peering, peering)

    def find_peering(self, name_or_id, ignore_missing=False):
        """Find a single vpc peering

        :param name_or_id: The name or ID of a zone
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the vpc peering does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent peering.

        :returns: One :class:`~otcextensions.sdk.vpc.v1.peering.Peering`
        """
        return self._find(
            _peering.Peering, name_or_id,
            ignore_missing=ignore_missing)

    def update_peering(self, peering, **attrs):
        """Update a vpc peering

        :param peering: Either the ID of a vpc peering or a
                       :class:`~otcextensions.sdk.vpc.v1.peering.Peering`
                       instance.
        :param dict attrs: The attributes to update on the vpc peering
            represented by ``peering``.

        :returns: The updated peering

        :rtype: :class:`~otcextensions.sdk.vpc.v1.peering.Peering`
        """
        return self._update(_peering.Peering, peering, **attrs)

    def set_peering(self, peering, set_status):
        """Accept/Reject a vpc peering connection request

        :param peering: Either the ID of a vpc peering or a
                       :class:`~otcextensions.sdk.vpc.v1.peering.Peering`
                       instance.
        :param set_status: The value can been ``accept`` or ``reject``

        :returns: The updated peering

        :rtype: :class:`~otcextensions.sdk.vpc.v1.peering.Peering`
        """
        valid_status = ['accept', 'reject']
        if set_status.lower() not in valid_status:
            raise ValueError(
                "results: status must be one of %r." % valid_status)
        peering = self._get_resource(_peering.Peering, peering)
        return peering._set_peering(self, set_status.lower())

    # ======== Route ========
    def add_route(self, **attrs):
        """Add vpc route

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vpc.v1.route.Route`
        """
        return self._create(_route.Route, **attrs)

    def delete_route(self, route, ignore_missing=True):
        """Delete a vpc route

        :param route: route id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.route.Route`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the vpc route does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent route.

        :returns: ``None``
        """
        return self._delete(_route.Route, route,
                            ignore_missing=ignore_missing)

    def routes(self, **query):
        """Return a generator of vpc routes

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of vpc route objects

        :rtype: :class:`~otcextensions.sdk.vpc.v1.route.Route`
        """
        return self._list(_route.Route, **query)

    def get_route(self, route):
        """Get details of a single vpc route

        :param route: The value can be the ID of a vpc route or a
                        :class:`~otcextensions.sdk.vpc.v1.route.Route`
                        instance.

        :returns: One :class:`~otcextensions.sdk.vpc.v1.route.Route`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_route.Route, route)

    # ========== VPC ==========
    def vpcs(self, **query):
        """Return a generator of vpcs

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of vpc objects

        :rtype: :class:`~otcextensions.sdk.vpc.v1.vpc.Vpc`
        """
        query['project_id'] = self.get_project_id()
        return self._list(_vpc.Vpc, **query)

    def create_vpc(self, **attrs):
        """Create a new vpc from attributes

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.vpc.v1.vpc.Vpc`
        """
        return self._create(_vpc.Vpc, **attrs,
                            project_id=self.get_project_id())

    def delete_vpc(self, vpc, ignore_missing=True):
        """Delete a vpc

        :param vpc: vpc id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.vpc.Vpc`

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the vpc route does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent route.

        :returns: none
        """
        return self._delete(_vpc.Vpc, vpc,
                            project_id=self.get_project_id(),
                            ignore_missing=ignore_missing)

    def get_vpc(self, vpc):
        """Get a vpc by id

        :param vpc: vpc id or an instance of
           :class:`~otcextensions.sdk.vpc.v1.vpc.Vpc`

        :returns: One :class:`~otcextensions.sdk.vpc.v1.vpc.Vpc`
        """
        return self._get(_vpc.Vpc, vpc, project_id=self.get_project_id())

    def find_vpc(self, name_or_id, ignore_missing=False):
        """Find a single vpc

        :param name_or_id: The name or ID of a vpc

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the vpc does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent peering.

        :returns: One :class:`~otcextensions.sdk.vpc.v1.vpc.Vpc`
        """
        return self._find(
            _vpc.Vpc, name_or_id,
            ignore_missing=ignore_missing,
            project_id=self.get_project_id())

    def update_vpc(self, vpc, **attrs):
        """Update vpc

        :param vpc: vpc id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.vpc.Vpc`

        :param dict attrs: The attributes to update on the vpc
            represented by ``vpcd``.
        """
        attrs['project_id'] = self.get_project_id()
        return self._update(_vpc.Vpc, vpc, **attrs)

    # ========== Subnet ==========
    def subnets(self, **query):
        """Return a generator of subnets

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of subnet objects

        :rtype: :class:`~otcextensions.sdk.vpc.v1.subnet.Subnet`
        """
        query['project_id'] = self.get_project_id()
        return self._list(_subnet.Subnet, **query)

    def create_subnet(self, **attrs):
        """Create a new subnet from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vpc.v1.subnet.Subnet`
        """
        attrs['project_id'] = self.get_project_id()
        return self._create(_subnet.Subnet, **attrs)

    def get_subnet(self, subnet):
        """Get a subnet by id

        :param subnet: subnet id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.subnet.Subnet`

        :returns: One :class:`~otcextensions.sdk.vpc.v1.subnet.Subnet`
        """
        return self._get(_subnet.Subnet, subnet,
                         project_id=self.get_project_id())

    def find_subnet(self, name_or_id, ignore_missing=False):
        """Find a single subnet

        :param name_or_id: The name or ID of a subnet

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the subnet does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent peering.

        :returns: One :class:`~otcextensions.sdk.vpc.v1.subnet.Subnet`
        """
        return self._find(
            _subnet.Subnet, name_or_id,
            ignore_missing=ignore_missing,
            project_id=self.get_project_id())

    def update_subnet(self, subnet, **attrs):
        """Update subnet

        :param subnet: subnet id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.subnet.Subnet`

        :param dict attrs: The attributes to update on the subnet
            represented by ``subnet``.
        """
        attrs['project_id'] = self.get_project_id()

        rs = self._get_resource(_subnet.Subnet, subnet)
        if rs.vpc_id is None and 'vpc_id' not in attrs:
            raise AttributeError('Updating subnet requires VPC ID')
        vpc_id = attrs.pop('vpc_id', rs.vpc_id)  # vpc_id can't be changed

        attrs.pop('base_path', None)
        base_path = _subnet.vpc_subnet_base_path(vpc_id)

        return self._update(_subnet.Subnet,
                            subnet,
                            base_path=base_path,
                            **attrs)

    def _delete(self, resource_type, value, ignore_missing=True, **attrs):
        """Override of ``_delete`` with support of ``base_path``"""
        base_path = attrs.pop('base_path', None)

        res = self._get_resource(resource_type, value, **attrs)

        try:
            rv = res.delete(self, base_path=base_path)
        except exceptions.ResourceNotFound:
            if ignore_missing:
                return None
            raise

        return rv

    def delete_subnet(self, subnet, vpc_id=None, ignore_missing=True):
        """Delete a subnet

        :param subnet: subnet id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.subnet.Subnet`

        :param vpc_id: VPC id. By default, taken from ``subnet``, if provided.

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the subnet route does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent route.

        :returns: none
        """
        sn_res = self._get_resource(_subnet.Subnet, subnet)
        sn_res.vpc_id = vpc_id or sn_res.vpc_id
        if sn_res.vpc_id is None:
            raise AttributeError('Deleting subnet requires VPC ID')

        base_path = _subnet.vpc_subnet_base_path(sn_res.vpc_id)

        return self._delete(_subnet.Subnet, subnet,
                            ignore_missing=ignore_missing,
                            base_path=base_path)

    # ========== Project cleanup ==========
    def _get_cleanup_dependencies(self):
        return {
            'vpc': {
                'before': ['network']
            }
        }

    def _service_cleanup(self, dry_run=True, client_status_queue=None,
                         identified_resources=None,
                         filters=None, resource_evaluation_fn=None):
        for obj in self.peerings():
            self._service_cleanup_del_res(
                self.delete_peering,
                obj,
                dry_run=dry_run,
                client_status_queue=client_status_queue,
                identified_resources=identified_resources,
                filters=filters,
                resource_evaluation_fn=resource_evaluation_fn)
