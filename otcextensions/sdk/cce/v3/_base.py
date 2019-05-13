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


class Metadata(resource.Resource):

    # Properties
    #: Annotations
    annotations = resource.Body('annotations', type=dict)
    #: UUID
    #: *Type:str
    id = resource.Body('uid', alternate_id=True)
    #: Labels
    labels = resource.Body('labels', type=dict)
    #: Name
    #: *Type:str
    name = resource.Body('name')
    #: Create time
    #: *Type:str
    created_at = resource.Body('creationTimeStamp')
    #: Update time
    #: *Type:str
    update_at = resource.Body('updateTimeStamp')


class Resource(resource.Resource):
    base_path = ''

    service_expectes_json_type = True

    # Properties
    #: Kind
    kind = resource.Body('kind')
    #: api version
    api_version = resource.Body('apiVersion', default='v3')
    #: metadata
    metadata = resource.Body('metadata', type=Metadata)
