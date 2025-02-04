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


class Log(resource.Resource):
    base_path = '/fgs/functions/%(function_urn)s/lts-log-detail'
    # Capabilities
    allow_create = True
    allow_fetch = True

    # Properties
    function_urn = resource.URI('function_urn', type=str)

    # Attributes
    #: Log group name.
    group_name = resource.Body('group_name', type=str)
    #: Log group ID.
    group_id = resource.Body('group_id', type=str)
    #: Log stream ID.
    stream_id = resource.Body('stream_id', type=str)
    #: Log stream name.
    stream_name = resource.Body('stream_name', type=str)
