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


class DownlinkVpcSpec(resource.Resource):
    vpc_id = resource.Body('vpc_id')
    virsubnet_id = resource.Body('virsubnet_id')
    ngport_ip_address = resource.Body('ngport_ip_address')


class TagSpec(resource.Resource):
    key = resource.Body('key')
    value = resource.Body('value')


class Gateway(resource.Resource):
    base_path = '/private-nat/gateways'
    resource_key = 'gateway'
    resources_key = 'gateways'
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'limit', 'marker', 'page_reverse',
        'id', 'name', 'description', 'spec', 'project_id',
        'status', 'vpc_id', 'virsubnet_id', 'enterprise_project_id'
    )

    id = resource.Body('id')
    project_id = resource.Body('project_id')
    name = resource.Body('name')
    description = resource.Body('description')
    spec = resource.Body('spec')
    status = resource.Body('status')
    created_at = resource.Body('created_at')
    updated_at = resource.Body('updated_at')
    downlink_vpcs = resource.Body('downlink_vpcs', type=list,
                                  list_type=DownlinkVpcSpec)
    tags = resource.Body('tags', type=list, list_type=TagSpec)
    enterprise_project_id = resource.Body('enterprise_project_id')
    rule_max = resource.Body('rule_max', type=int)
    transit_ip_pool_size_max = resource.Body('transit_ip_pool_size_max',
                                             type=int)
