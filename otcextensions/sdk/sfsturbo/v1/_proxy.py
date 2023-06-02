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
from openstack import proxy, resource

from otcextensions.sdk.sfsturbo.v1 import share as _sfs
from otcextensions.common.exc import HTTPMethodNotAllowed


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ========== Sfs Turbo ==========
    def shares(self, **query):
        """Return a generator of sfs turbo file systems

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of share objects

        :rtype: :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`
        """
        base_path = _sfs.Share.base_path + '/detail'
        return self._list(_sfs.Share, base_path=base_path, **query)

    def create_share(self, **attrs):
        """Create a new sfs turbo file system

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`
        """
        return self._create(_sfs.Share, **attrs)

    def update_share(self, share, **attrs):
        """Update a new sfs turbo file system
        """
        raise HTTPMethodNotAllowed

    def delete_share(self, share, ignore_missing=True):
        """Delete a sfs turbo file system

        :param share: share id or an instance of
            :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the vpc route does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent route.

        :returns: none
        """
        return self._delete(_sfs.Share, share,
                            ignore_missing=ignore_missing)

    def get_share(self, share):
        """Get a sfs turbo file system by id

        :param share: share id or an instance of
           :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`

        :returns: One :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`
        """
        return self._get(_sfs.Share, share)

    def find_share(self, name_or_id, ignore_missing=True):
        """Find a single sfs turbo file system by id

        :param name_or_id: The name or ID of a share

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the vpc does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent peering.

        :returns: One :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`
        """
        return self._find(
            _sfs.Share, name_or_id,
            ignore_missing=ignore_missing,
            list_base_path='/sfs-turbo/shares/detail',
        )

    def wait_for_share(self, share, status='200', failures=None,
                       interval=2, wait=350, attribute='status'):
        """Wait for an share to be in a particular status.

        :param share:
            The :class:`~otcextensions.sdk.share.v1.share.Share`
            or share ID to wait on to reach the specified status.
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
        return resource.wait_for_status(
            self, share, status, failures, interval, wait)

    def wait_for_extend_capacity(self, share, new_capacity,
                                 interval=5, wait=500):
        """Wait for an share to be in a particular status.

        :param failures:
            Size that would be interpreted as failures.
        :type failures: :py:class:`list`
        """
        return share.wait_for_extend_capacity(
            self, new_capacity, interval, wait)

    def extend_capacity(self, share, new_size):
        """Extend the capacity of the file system

        :param share: The value can be the ID of a share
             or a :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`
             instance.
        :param new_size: Specifies the new capacity (GB)
            of the shared file system.
        """
        share = self._get_resource(_sfs.Share, share)
        extend = {'new_size': new_size}
        return share.extend_capacity(
            self,
            extend=extend)

    def change_security_group(self, share, security_group_id):
        """Change the security group bound to an SFS Turbo file system.

        :param share: The value can be the ID of a share
             or a :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`
             instance.
        :param security_group_id: Specifies the ID of the security group to be
             modified.
        """
        share = self._get_resource(_sfs.Share, share)
        change_security_group = {'security_group_id': security_group_id}
        return share.change_security_group(
            self,
            change_security_group=change_security_group)
