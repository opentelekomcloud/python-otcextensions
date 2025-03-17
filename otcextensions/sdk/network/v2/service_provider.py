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
from urllib.parse import urlunparse
from urllib.parse import urlparse

from openstack import exceptions
from openstack import utils

from openstack.network.v2 import service_provider


class ServiceProvider(service_provider.ServiceProvider):
    @classmethod
    def list(cls, session, paginated=False,
             endpoint_override=None, headers=None, requests_auth=None,
             **params):
        return [True]
