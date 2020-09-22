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
from urllib.parse import urlparse

from openstack import resource
from openstack.utils import urljoin


class BadBaseResource(resource.Resource):
    """A base class for all terribly exposed non Keystone native extensions
    """

    def __init__(self, _synchronized=False, connection=None, **attrs):
        super(BadBaseResource, self).__init__(
            _synchronized=_synchronized,
            connection=connection, **attrs)
        if connection:
            # Hopefully we land here when creating/fetching resource. If this
            # is the case - try to modify base_url of the resource to be
            # pointing to the FQDN instead of relative URL due to a completely
            # insane service publishing.
            # We need this for the operations, which doesn't support overriding
            # base_path from proxy layer
            identity_url = connection.identity.get_endpoint_data().url
            parsed_domain = urlparse(identity_url)
            self.__base = '%s://%s' % (
                parsed_domain.scheme, parsed_domain.netloc)
            self.base_path = urljoin(
                self.__base,
                self.base_path)
