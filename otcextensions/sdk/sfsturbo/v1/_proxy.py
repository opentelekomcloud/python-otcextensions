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

from otcextensions.sdk.sfsturbo.v1 import share as _sfs


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ========== Sfs Turbo ==========
    def shares(self, **query):
        """Return a generator of sfs turbo file systems

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of vpc objects

        :rtype: :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`
        """
        return self._list(_sfs.Share, **query)

    def create_share(self, **attrs):
        """Create a new sfs turbo file system

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.sfsturbo.v1.share.Share`
        """
        return self._create(_sfs.Share, **attrs)

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

    def find_share(self, name_or_id, ignore_missing=False):
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
            ignore_missing=ignore_missing)
