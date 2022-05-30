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
from openstack import _log

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class Datasource(sdk_resource.Resource):
    resource_key = 'data_source'
    resources_key = 'data_sources'
    base_path = '/data-sources'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_update = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'type', 'url', 'description', 'is_public',
        'is_protected')

    #: Properties
    #: Data source ID
    id = resource.Body('id', alternate_id=True)
    #: Data source name
    name = resource.Body('name')
    #: type of the ds
    type = resource.Body('type')
    #: Data source URL
    url = resource.Body('url')
    #: Data source description
    description = resource.Body('description')
    #: Whether the data source is public
    is_public = resource.Body('is_public')
    #: Whether the data source is protected
    is_protected = resource.Body('is_protected')
    #: Data source creation time
    created_at = resource.Body('created_at')
    #: Data source update time
    updated_at = resource.Body('updated_at')
