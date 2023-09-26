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
import os
from urllib import parse
from otcextensions.sdk import ak_auth
from otcextensions.sdk import sdk_proxy


class Proxy(sdk_proxy.Proxy):
    skip_discovery = True

    CONTAINER_ENDPOINT = \
        'https://%(container)s.obs.%(region_name)s.otc.t-systems.com'

    def _extract_name(self, url, service_type=None, project_id=None):
        url_path = parse.urlparse(url).path.strip()
        # Remove / from the beginning to keep the list indexes of interesting
        # things consistent
        if url_path.startswith('/'):
            url_path = url_path[1:]

        # Split url into parts and exclude potential project_id in some urls
        url_parts = url_path.split('/')

        # Strip out anything that's empty or None
        parts = [part for part in url_parts if part]

        # Getting the root of an endpoint is a bucket operation
        if not parts:
            return ['bucket']
        else:
            return ['object']

    def get_container_endpoint(self, container):
        """Override to return mapped endpoint if override and region are set

        """
        region_name = getattr(self, 'region_name', 'eu-de')
        endpoint = self.CONTAINER_ENDPOINT % {
            'container': container,
            'region_name': region_name
        }
        return endpoint

    def _get_req_auth(self, host=None):
        auth = getattr(self, '_ak_auth', None)
        if not auth:
            ak = None
            sk = None
            conn = self.session._sdk_connection
            if hasattr(conn, 'get_ak_sk'):
                (ak, sk) = conn.get_ak_sk(conn)
            if not (ak and sk):
                self.log.error('Cannot obtain AK/SK from config')
                return None
            region = getattr(self, 'region_name', 'eu-de')
            if not host:
                host = self.get_endpoint()

            auth = ak_auth.AKRequestsAuth(
                access_key=ak,
                secret_access_key=sk,
                host=host,
                region=region,
                service='s3'
            )
            setattr(self, '_ak_auth', auth)
        return auth

    # ======== Containers ========

    def containers(self, **query):
        """Obtain Container objects for this account.

        :param kwargs query: Optional query parameters to be sent to limit
                                 the resources being returned.

        :rtype: A generator of
            :class:`~otcextensions.sdk.obs.v1.container.Container` objects.
        """
        return self._list(_container.Container,
                          requests_auth=self._get_req_auth(),
                          **query)

    def get_container(self, container):
        """Get the detail of a container

        :param container: Container name or an object of class
                   :class:`~otcextensions.sdk.obs.v1.container.Container`
        :returns: Detail of container
        :rtype: :class:`~otcextensions.sdk.obs.v1.container.Container`
        """
        container = self._get_container_name(container=container)
        endpoint = self.get_container_endpoint(container)
        return self._head(
            _container.Container,
            container,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint))

    def create_container(self, **attrs):
        """Create a new container from attributes

        :param container: Name of the container to create.
        :param dict attrs: Keyword arguments which will be used to create
               a :class:`~otcextensions.sdk.obs.v1.container.Container`,
               comprised of the properties on the Container class.

        :returns: The results of container creation
        :rtype: :class:`~otcextensions.sdk.obs.v1.container.Container`
        """
        container = attrs.get('name', None)
        endpoint = self.get_container_endpoint(container)
        return self._create(
            _container.Container,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
            # prepend_key=False,
            **attrs)

    def delete_container(self, container, ignore_missing=True):
        """Delete a container

        :param container: The value can be either the name of a container or a
                      :class:`~otcextensions.sdk.obs.v1.container.Container`
                      instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the container does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent server.

        :returns: ``None``
        """
        container = self._get_container_name(container=container)
        endpoint = self.get_container_endpoint(container)
        self._delete(_container.Container, container,
                     endpoint_override=endpoint,
                     requests_auth=self._get_req_auth(endpoint),
                     ignore_missing=ignore_missing)
