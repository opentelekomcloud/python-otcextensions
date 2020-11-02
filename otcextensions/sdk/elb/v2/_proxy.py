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
from otcextensions.sdk.elb.v2 import lb_certificate as _certificate
from urllib.parse import urlparse

class Proxy(proxy.Proxy):

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self._credentials_base = None

    def _get_alternate_endpoint(self):
        if not self._credentials_base:
            identity_url = self.get_endpoint_data().url
            parsed_domain = urlparse(identity_url)
            self._credentials_base = '%s://%s' % (parsed_domain.scheme,
                                                  parsed_domain.netloc)
        return self._credentials_base

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