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

from otcextensions.sdk.ddmv1.v1 import _proxy


class Ddmv1Service(service_description.ServiceDescription):
    """The Distributed Database Middleware service."""

    supported_versions = {
        '1': _proxy.Proxy
    }
