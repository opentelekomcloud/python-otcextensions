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
from openstack import exceptions
from openstack import resource


class TagsSpec(resource.Resource):
    #: Tag key.
    key = resource.Body('key')
    #: Tag value.
    value = resource.Body('value')


class PortSpec(resource.Resource):
    #: Port for accessing the VPC endpoint.
    client_port = resource.Body('client_port', type=int)
    #: Port mapping protocol.
    protocol = resource.Body('protocol')
    #: Port for accessing the VPC endpoint service.
    server_port = resource.Body('server_port', type=int)


class Service(resource.Resource):
    base_path = '/vpc-endpoint-services'
    resources_key = 'endpoint_services'

    _query_mapping = resource.QueryParameters(
        'id',
        'limit',
        'name',
        'offset',
        'sort_key',
        'sort_dir',
        'status',
        name='endpoint_service_name',
    )

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    # Properties
    #: Creation time of the VPC endpoint service.
    created_at = resource.Body('created_at')
    #: Count of Creating or Accepted VPC endpoints under the
    #:  VPC endpoint service.
    connection_count = resource.Body('connection_count', type=int)
    #: Supplementary information about the VPC endpoint service.
    description = resource.Body('description')
    #: Specifies the user's domain ID.
    domain_id = resource.Body('domain_id')
    #: ID of the VPC endpoint service.
    id = resource.Body('id')
    #: Whether connection approval is required.
    is_approval_enabled = resource.Body('approval_enabled', type=bool)
    #: ID of the cluster associated with the target VPCEP resource.
    pool_id = resource.Body('pool_id')
    #: ID for identifying the backend resource of the VPC endpoint service.
    port_id = resource.Body('port_id')
    #: Lists the port mappings opened to the VPC endpoint service.
    ports = resource.Body('ports', type=list, list_type=PortSpec)
    #: Project ID.
    project_id = resource.Body('project_id')
    #: ID of the router to which the backend resource of the VPC endpoint
    #:  service belongs.
    router_id = resource.Body('vpc_id')
    #: Resource type.
    server_type = resource.Body('server_type')
    #: Name of the VPC endpoint service.
    service_name = resource.Body('service_name')
    #: Type of the VPC endpoint service.
    service_type = resource.Body('service_type')
    #: Status of the VPC endpoint service.
    status = resource.Body('status')
    #: Lists the resource tags.
    tags = resource.Body('tags', type=list, list_type=TagsSpec)
    #: Specifies whether the client IP address and port number or marker_id
    #:  information is transmitted to the server.
    tcp_proxy = resource.Body('tcp_proxy')
    #: Update time of the VPC endpoint service.
    updated_at = resource.Body('updated_at')

    @classmethod
    def _get_one_match(cls, name_or_id, results):
        """Given a list of results, return the match"""
        the_result = None
        for maybe_result in results:
            id_value = cls._get_id(maybe_result)
            name_value = maybe_result.service_name

            if (id_value == name_or_id) or (name_value == name_or_id):
                # Only allow one resource to be found. If we already
                # found a match, raise an exception to show it.
                if the_result is None:
                    the_result = maybe_result
                else:
                    msg = "More than one %s exists with the name '%s'."
                    msg = msg % (cls.__name__, name_or_id)
                    raise exceptions.DuplicateResource(msg)
        return the_result
