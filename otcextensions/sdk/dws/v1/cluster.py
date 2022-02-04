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


class Cluster(resource.Resource):
    resource_key = 'cluster'
    resource_key = 'clusters'
    base_path = '/%(project_id)s/clusters'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_get = True
    allow_list = True
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'availability_zone', 'public_ip', 'number_of_node', 'vpc_id',
        'user_name', 'security_group_id', 'number_of_cn', 'user_pwd',
        'enterprise_project_id', 'node_type', 'port', 'name',
        'subnet_id', 'project_id', project_id='tenant_id',
    )

    # Properties
    project_id = resource.URI('project_id')
    # AZ of a cluster
    availability_zone = resource.Body('availability_zone')
    # Public IP address. If the parameter is not specified,
    # public connection is not used by default.
    public_ip = resource.Body('public_ip')
    # Number of nodes in a cluster. The value ranges from 3 to 32.
    number_of_node = resource.Body('number_of_node')
    # VPC ID, which is used for configuring cluster network.
    vpc_id = resource.Body('vpc_id')
    # Administrator username for logging in to a data warehouse cluster.
    user_name = resource.Body('user_name')
    # ID of a security group, which is used for configuring cluster network
    security_group_id = resource.Body('security_group_id')
    # Number of deployed CNs.
    # The value ranges from 2 to the number of cluster nodes minus 1.
    # The maximum value is 5 and the default value is 2.
    number_of_cn = resource.Body('number_of_cn')
    # Password of the administrator for logging in to a datawarehouse cluster
    user_pwd = resource.Body('user_pwd')
    # Enterprise project ID.
    # If no enterprise project is specified for a cluster,
    # the default enterprise project ID 0 is used.
    enterprise_project_id = resource.Body('enterprise_project_id')
    # Node Type
    node_type = resource.Body('node_type')
    # Service port of a cluster. The value ranges from 8000 to 30000.
    # The default value is 8000.
    port = resource.Body('port')
    # Cluster name, which must be unique.
    name = resource.Body('name')
    # Subnet ID, which is used for configuring cluster network.
    subnet_id = resource.Body('subnet_id')
    # Binding type of an EIP. The value can be one of the following:
    # - auto_assign
    # - not_use
    # - bind_existing
    public_bind_type = resource.Body('public_bind_type')
    # EIP ID
    eip_id = resource.Body('eip_id')
