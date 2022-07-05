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

from openstack import _log
from openstack import resource

from otcextensions.sdk.mrs.v1 import _base

_logger = _log.setup_logging('openstack')


class Jobbinary(_base.Resource):
    resource_key = 'job_binary'
    resources_key = 'binaries'
    base_path = '/job-binaries'

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'url', 'description', 'is_public',
        'is_protected')

    #: Properties
    #: Binary object ID
    id = resource.Body('id', alternate_id=True)
    #: Binary object name
    name = resource.Body('name')
    #: Binary object URL
    url = resource.Body('url')
    #: Binary object description
    description = resource.Body('description')
    #: Whether a binary object is public
    is_public = resource.Body('is_public')
    #: Whether a binary object is protected
    is_protected = resource.Body('is_protected')
    #: Binary object creation time
    created_at = resource.Body('created_at')
    #: Binary object update time
    updated_at = resource.Body('updated_at')
