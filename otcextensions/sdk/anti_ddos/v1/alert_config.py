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

from otcextensions.sdk import sdk_resource


class AlertConfig(sdk_resource.Resource):

    base_path = '/warnalert/alertconfig/query'

    # capabilities
    allow_get = True

    # Properties
    #: warn alert config information
    #: *Type: dict*
    config = resource.Body('warn_config', type=dict)
    #: unique topic id
    topic_urn = resource.Body('topic_urn')
    #: warn alert group name
    display_name = resource.Body('display_name')

    # # This overrides the default behavior of resource get
    # def get(self, session, requires_id=False):
    #     return super(AlertConfig, self).get(session, requires_id=requires_id)
