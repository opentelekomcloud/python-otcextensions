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

from openstack.load_balancer.v2 import _proxy

from otcextensions.sdk.elb.v2 import lb_certificate as _certificate


class Proxy(_proxy.Proxy):
    skip_discovery = True

    # ======== Certificate ========
    def create_certificate(self, **attrs):
        """Create a new certificate from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.elb.v2.lb_certificate.Certificate`,
            comprised of the properties on the Certificate class.

        :returns: The results of the Certificate Creation

        :rtype: :class:`~otcextensions.sdk.elb.v2.lb_certificate.Certificate`
        """
        return self._create(_certificate.Certificate, **attrs)

    def certificates(self, **query):
        """Return a generator of certificates

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of certificates objects.
        """
        return self._list(_certificate.Certificate, **query)