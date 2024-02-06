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
from urllib import parse

from openstack import proxy
from otcextensions.sdk.swr.v2 import organization as _organization


class Proxy(proxy.Proxy):
    skip_discovery = True

    def _extract_name(self, url, service_type=None, project_id=None):
        path = parse.urlparse(url).path.strip()
        # Remove / from the beginning to keep the list indexes of interesting
        # things consistent
        if path.startswith('/'):
            path = path[1:]

        # Split url into parts and exclude potential project_id in some urls
        url_parts = [
            x for x in path.split('/') if x != project_id
        ]
        # exclude version
        url_parts = list(filter(lambda x: not any(
            c.isdigit() for c in x[1:]) and (
                x[0].lower() != 'v'), url_parts))

        # Strip out anything that's empty or None
        return [part for part in url_parts if part]

    def create_organization(self, **attrs):
        """Create a new organization from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.swr.v2.
            organization.Organization`, comprised of the properties on the
            Organization class.

        :returns: The results of organization creation
        :rtype: :class:`~otcextensions.sdk.swr.v2.organization.Organization`
        """
        return self._create(_organization.Organization, **attrs)

    def get_organization(self, *attrs):
        """Get a organization

        :returns: One
             :class:`~otcextensions.sdk.swr.v2.organization.Organization`
        """
        return self._get(_organization.Organization, *attrs)

    def organizations(self, **query):
        """Retrieve a generator of organizations

        :returns: A generator of organization instances
        """
        return self._list(_organization.Organization, **query)

    def delete_organization(self, namespace, ignore_missing=True):
        """Delete an organization

        :param namespace: The namespace can be either the name or a
            :class:`~otcextensions.sdk.swr.v2.organization.Organization`
            instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the load balancer does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent organization.

        :returns: ``None``
        """
        return self._delete(_organization.Organization, namespace,
                            ignore_missing=ignore_missing)

    def find_organization(self, name_or_id, ignore_missing=True):
        """Find a single organization

        :param name_or_id: The name or ID of an organization
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the organization does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent organization.

        :returns: ``None``
        """
        return self._find(_organization.Organization, name_or_id,
                          ignore_missing=ignore_missing)

    def create_organization_permissions(self, **attrs):
        """Create a new organization from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.swr.v2.
            organization.Organization`, comprised of the properties on the
            Organization class.

        :returns: The results of organization creation
        :rtype: :class:`~otcextensions.sdk.swr.v2.organization.Permission`
        """
        return self._create(_organization.Permission, **attrs)

    def organization_permissions(self, namespace, **query):
        """Retrieve a generator of organization permissions

        :returns: A generator of organization permissions instances
        """
        return self._list(_organization.Permission,
                          namespace=namespace, **query)

    def delete_organization_permissions(
            self, namespace, user_ids, ignore_missing=True
    ):
        """Delete an organization permissions

        :param user_ids: Users IDs whose permissions need to be deleted.
        :param namespace: The namespace can be either the name or a
            :class:`~otcextensions.sdk.swr.v2.organization.Permission`
            instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the load balancer does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent organization.

        :returns: ``None``
        """
        permission = self._get_resource(_organization.Permission, namespace)
        return permission._delete_permissions(self, user_ids)

    def update_organization_permissions(self, **attrs):
        """Update an organization permissions

        :param dict attrs: The attributes to update on the permissions
         represented by ``permissions``.

        :returns: The updated permissions.

        :rtype: :class:`~otcextensions.sdk.swr.v2.organization.Permission`
        """
        return self._update(_organization.Permission, **attrs)
