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


class StorageType(resource.Resource):

    base_path = '/storage-type/%(datastore_name)s'
    resources_key = 'storage_type'

    # capabilities
    allow_list = True
    _query_mapping = resource.QueryParameters(
        'version_name')

    #: DB engine name
    #: *Type: str*
    datastore_name = resource.URI('datastore_name')
    #: Indicates the storage type
    #: *Type: str*
    name = resource.Body('name')
    #: Indicates the performance specifications
    #: *Type: list*
    compute_group_type = resource.Body('support_compute_group_type', type=list)
    #: Availability Zone Status
    #: *Type: dict*
    az_status = resource.Body('az_status', type=dict)
