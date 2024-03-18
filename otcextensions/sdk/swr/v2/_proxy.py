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
from otcextensions.sdk.swr.v2 import _base
from otcextensions.sdk.swr.v2 import organization as _organization
from otcextensions.sdk.swr.v2 import repository as _repository
from otcextensions.sdk.swr.v2 import domain as _domain


def update_permissions_attrs(attrs):
    for permission in attrs.get('permissions', []):
        permission['auth'] = permission.pop('user_auth', None)
    return attrs


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
        """Get an organization

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
        orgobj = self._get_resource(_organization.Organization, namespace)
        return self._delete(_organization.Organization, orgobj.id,
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
        attrs = update_permissions_attrs(attrs)
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
            delete a nonexistent permission.

        :returns: ``None``
        """
        base_path = f'/manage/namespaces/{namespace}/access'
        res = self._get_resource(_base.Resource, namespace)
        return res._delete(self, user_ids, base_path)

    def update_organization_permissions(self, **attrs):
        """Update an organization permissions

        :param dict attrs: The attributes to update on the permissions
         represented by ``permissions``.

        :returns: The updated permissions.

        :rtype: :class:`~otcextensions.sdk.swr.v2.organization.Permission`
        """
        attrs = update_permissions_attrs(attrs)
        return self._update(_organization.Permission, **attrs)

    def create_repository(self, **attrs):
        """Create a new image repository from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.swr.v2.
            repository.Repository`, comprised of the properties on the
            Repository class.

        :returns: The results of organization creation
        :rtype: :class:`~otcextensions.sdk.swr.v2.repository.Repository`
        """
        return self._create(_repository.Repository, **attrs)

    def delete_repository(
            self, namespace, repository, ignore_missing=True
    ):
        """Delete a repository

        :param repository: Image repository name need to be deleted.
        :param namespace: The namespace can be either the name or a
            :class:`~otcextensions.sdk.swr.v2.repository.Repository`
            instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the load balancer does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent repository.

        :returns: ``None``
        """
        orgobj = self._get_resource(_organization.Organization, namespace)
        repotype = _repository.Repository
        repotype.requires_id = True
        self._delete(repotype, repository,
                     ignore_missing=ignore_missing, namespace=orgobj.id)

    def get_repository(self, namespace, repository):
        """Get a repository

        :returns: One
             :class:`~otcextensions.sdk.swr.v2.repository.Repository`
        """
        orgobj = self._get_resource(_organization.Organization, namespace)
        return self._get(_repository.Repository, repository,
                         namespace=orgobj.id)

    def repositories(self, **query):
        """Retrieve a generator of repositories

        :returns: A generator of repositories instances
        """
        base_path = '/manage/repos'
        return self._list(_repository.Repository, base_path=base_path, **query)

    def update_repository(self, **attrs):
        """Update a repository

        :param dict attrs: The attributes to update on the repository
         represented by ``repository``.

        :returns: The updated repository.

        :rtype: :class:`~otcextensions.sdk.swr.v2.repository.Repository`
        """
        bp = f'/manage/namespaces/%(namespace)s/repos/{attrs["repository"]}'
        repotype = _repository.Repository
        repotype.requires_id = False
        return self._update(repotype, base_path=bp, **attrs)

    def create_repository_permissions(self, **attrs):
        """Create a new repository permissions from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.swr.v2.
            repository.Permission`, comprised of the properties on the
            Permission class.

        :returns: The results of repository permission creation
        :rtype: :class:`~otcextensions.sdk.swr.v2.repository.Permission`
        """
        attrs = update_permissions_attrs(attrs)
        return self._create(_repository.Permission, **attrs)

    def repository_permissions(self, namespace, repository, **query):
        """Retrieve a generator of repository permissions

        :returns: A generator of repository permissions instances
        """
        return self._list(_repository.Permission,
                          namespace=namespace,
                          repository=repository,
                          **query)

    def delete_repository_permissions(
            self, namespace, repository, user_ids, ignore_missing=True
    ):
        """Delete a repository permissions

        :param repository: The repository can be either the name or a
            :class:`~otcextensions.sdk.swr.v2.repository.Permission`
            instance
        :param user_ids: Users IDs whose permissions need to be deleted.
        :param namespace: The namespace can be either the name or a
            :class:`~otcextensions.sdk.swr.v2.organization.Permission`
            instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the load balancer does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent permission.

        :returns: ``None``
        """
        bp = f'/manage/namespaces/{namespace}/repos/{repository}/access'
        res = self._get_resource(_base.Resource, namespace)
        return res._delete(self, user_ids, bp)

    def update_repository_permissions(self, **attrs):
        """Update a repository permissions

        :param dict attrs: The attributes to update on the permissions
         represented by ``permissions``.

        :returns: The updated permissions.

        :rtype: :class:`~otcextensions.sdk.swr.v2.repository.Permission`
        """
        attrs = update_permissions_attrs(attrs)
        return self._update(_repository.Permission, **attrs)

    def create_domain(self, **attrs):
        """Create a new image repository from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.swr.v2.
            domain.Domain`, comprised of the properties on the
            Repository class.

        :returns: The results of organization creation
        :rtype: :class:`~otcextensions.sdk.swr.v2.domain.Domain`
        """
        return self._create(_domain.Domain, **attrs)

    def delete_domain(
            self, namespace, repository, access_domain, ignore_missing=True
    ):
        """Delete a domain

        :param access_domain: Name of the account need to be deleted.
        :param repository: Image repository name.
        :param namespace: Organization name.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the load balancer does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent repository.

        :returns: ``None``
        """
        self._delete(_domain.Domain, repository=repository,
                     id=access_domain,
                     ignore_missing=ignore_missing,
                     namespace=namespace)

    def domains(self, **query):
        """Retrieve a generator of domains

        :returns: A generator of domain instances
        """
        return self._list(_domain.Domain, **query)

    def update_domain(self, **attrs):
        """Update a domain

        :param dict attrs: The attributes to update on the domain
         represented by ``permissions``.

        :returns: The updated domain.

        :rtype: :class:`~otcextensions.sdk.swr.v2.domain.Domain`
        """
        return self._update(_domain.Domain, id=attrs['access_domain'], **attrs)

    def get_domain(self, namespace, repository, access_domain):
        """Get a domain

        :returns: One
             :class:`~otcextensions.sdk.swr.v2.domain.Domain`
        """
        return self._get(_domain.Domain,
                         repository=repository,
                         id=access_domain,
                         namespace=namespace)
