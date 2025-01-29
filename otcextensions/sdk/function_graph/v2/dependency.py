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
from openstack import exceptions


class ListDependenciesResult(resource.Resource):
    id = resource.Body('id', type=str)
    owner = resource.Body('owner', type=str)
    link = resource.Body('link', type=str)
    runtime = resource.Body('runtime', type=str)
    etag = resource.Body('etag', type=str)
    size = resource.Body('size', type=int)
    name = resource.Body('name', type=str)
    file_name = resource.Body('file_name', type=str)
    description = resource.Body('description', type=str)
    version = resource.Body('version', type=int)
    last_modified = resource.Body('last_modified', type=int)
    dep_id = resource.Body('dep_id', type=str)
    is_shared = resource.Body('is_shared', type=bool)


class Dependency(resource.Resource):
    base_path = '/fgs/dependencies'

    requires_id = False
    # Capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'marker', 'maxitems', 'ispublic',
        'dependency_type', 'runtime', 'name', 'limit'
    )

    # Properties
    depend_file = resource.Body('depend_file', type=str)
    depend_link = resource.Body('depend_link', type=str)
    depend_type = resource.Body('depend_type', type=str)
    runtime = resource.Body('runtime', type=str)
    name = resource.Body('name', type=str)
    description = resource.Body('description', type=str)

    # Attributes
    #: Dependency list.
    dependencies = resource.Body(
        'dependencies', type=list, list_type=ListDependenciesResult
    )
    #: Next read location.
    next_marker = resource.Body('next_marker', type=int)
    #: Total number of dependencies.
    count = resource.Body('count', type=int)

    owner = resource.Body('owner', type=str)
    link = resource.Body('link', type=str)
    etag = resource.Body('etag', type=str)
    size = resource.Body('size', type=int)
    file_name = resource.Body('file_name', type=str)
    version = resource.Body('version', type=int)
    dep_id = resource.Body('dep_id', type=str)
    last_modified = resource.Body('last_modified', type=int)

    def _delete_version(self, session, dependency):
        """Delete Version
        """
        url = self.base_path + (f'/{dependency.dep_id}'
                                f'/version/{dependency.version}')
        response = session.delete(url)
        exceptions.raise_from_response(response)
        return None
