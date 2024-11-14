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

from openstack import service_description
from otcextensions.sdk.apig.v2 import _proxy
from otcextensions.sdk.sdk_make_proxy import ServiceProxy


class ApigService(service_description.ServiceDescription):
    """The APIG service."""

    supported_versions = {
        '2': _proxy.Proxy
    }

    def _make_proxy(self, instance):
        """Create a Proxy for the service in question.

        :param instance:
          The `openstack.connection.Connection` we're working with.
        """
        # Instantiate the ServiceProxy with the current instance and service type
        service_proxy = ServiceProxy(instance, self.service_type, self.supported_versions)

        # If service not in service catalog the create_proxy method
        # creates and returns the proxy object based on base_service endpoint
        return service_proxy.create_proxy(
            base_service="aomv2",
            target_service="apig",
        )
