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
from openstack import resource

from otcextensions.sdk.dms.v1 import _base


class AvailabilityZone(_base.Resource):
    """DMS AZ resource"""
    resources_key = 'available_zones'
    base_path = '/availableZones'

    # capabilities
    allow_list = True

    #: Properties
    #: AZ code
    code = resource.Body('code')
    #: Has free resources
    has_available_resources = resource.Body('resource_availability', type=bool)
    #: Port number
    port = resource.Body('port')
    #: Region ID
    region_id = resource.Body('region_id')

    @classmethod
    def list(cls, session, **params):
        return super(AvailabilityZone, cls).list_override(session, **params)
