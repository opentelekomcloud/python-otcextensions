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
from openstack import proxy

from otcextensions.sdk.vpcep.v1 import vpc_endpoint as _vpc_endpoint

from dataclasses import dataclass
from typing import List


@dataclass
class PublicInfo:
    publicip_id: str
    publicip_type: str


class Proxy(proxy.Proxy):
    skip_discovery = True

    # ======== VpcEndpoint ========
    def add_vpc_endpoint(self, **attrs):
        """Add vpc endpoint

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vpc.v1.vpc_endpoint.VpcEndpoint`
        """
        attrs['project_id'] = self.get_project_id()
        return self._create(_vpc_endpoint.VpcEndpoint, **attrs)

    def delete_vpc_endpoint(self, vpc_endpoint, ignore_missing=True):
        """Delete a vpc endpoint

        :param vpc_endpoint: endpoint id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.vpc_endpoint.VpcEndpoint`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the vpc endpoint does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent endpoint.

        :returns: ``None``
        """
        return self._delete(_vpc_endpoint.VpcEndpoint, vpc_endpoint,
                            project_id=self.get_project_id(),
                            ignore_missing=ignore_missing)

    def vpc_endpoints(self, **query):
        """Return a generator of vpc endpoints

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of vpc endpoint objects

        :rtype: :class:`~otcextensions.sdk.vpc.v1.vpc_endpoint.VpcEndpoint`
        """
        query['project_id'] = self.get_project_id()
        return self._list(_vpc_endpoint.VpcEndpoint, **query)

    def get_vpc_endpoint(self, vpc_endpoint):
        """Get details of a single vpc endpoint

        :param vpc_endpoint: The value can be the ID of a vpc endpoint or a
                        :class:`~otcextensions.sdk.vpc.v1.vpc_endpoint.VpcEndpoint`
                        instance.

        :returns: One :class:`~otcextensions.sdk.vpc.v1.vpc_endpoint.VpcEndpoint`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_vpc_endpoint.VpcEndpoint, vpc_endpoint, project_id=self.get_project_id())
