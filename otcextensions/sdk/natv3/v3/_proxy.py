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
