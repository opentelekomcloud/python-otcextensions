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


class MaintenanceWindow(_base.Resource):
    """DMS Maintenance window resource"""
    resources_key = 'maintain_windows'
    base_path = '/instances/maintain-windows'

    # capabilities
    allow_list = True

    #: Properties
    #: Indicates the sequential number of a maintenance time window.
    seq = resource.Body('seq', type=int)
    #: Indicates the time at which a maintenance time window starts.
    begin = resource.Body('begin')
    #: Indicates the time at which a maintenance time window ends.
    end = resource.Body('end')
    #: Indicates whether a maintenance time window is set to the
    #: default time segment.
    is_default = resource.Body('default', type=bool)

    @classmethod
    def list(cls, session, **params):
        return super(MaintenanceWindow, cls).list_override(session, **params)
