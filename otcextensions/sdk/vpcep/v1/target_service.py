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
#
from openstack import resource


class TargetService(resource.Resource):
    base_path = '/vpc-endpoint-services/describe'

    _query_mapping = resource.QueryParameters(
        'id',
        name='endpoint_service_name',
    )

    # capabilities
    allow_create = False
    allow_fetch = True
    allow_commit = False
    allow_delete = False
    allow_list = True

    requires_id = False

    # Properties
    #: ID of the VPC endpoint service.
    id = resource.Body('id')
    #: Name of the VPC endpoint service.
    service_name = resource.Body('service_name')
    #: Type of the VPC endpoint service.
    service_type = resource.Body('service_type')
    #: Creation time of the VPC endpoint service.
    created_at = resource.Body('created_at')
    #: If the usage of the VPC endpoint service will be charged.
    is_charge = resource.Body('is_charge')
