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


class MaintenanceTimeWindow(resource.Resource):

    resources_key = 'maintain_windows'

    base_path = '/instances/maintain-windows'

    # capabilities
    allow_list = True

    #: Properties
    #: An indicator of whether the maintenance time window is set to the
    # default time segment.
    default = resource.Body('default', type=bool)
    #: Sequence number of the maintenance time window.
    seq = resource.Body('seq', type=int)
    #: Start time of the maintenance time window.
    begin = resource.Body('begin')
    #: End time of the maintenance time window.
    end = resource.Body('end')
