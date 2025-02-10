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
    #: Specifies the tag key.
    key = resource.Body('key')
    #: Specifies the tag value.
    value = resource.Body('value')


class Endpoint(resource.Resource):
    base_path = '/vpc-endpoints'
    resources_key = 'endpoints'
    resource_key = None

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id',
        'offset',
        'limit',
        'router_id',
        'endpoint_service_name',
        'sort_dir',
        'sort_key',
        router_id='vpc_id',
    )

    # Properties
    #: Domain status.
    active_status = resource.Body('active_status', type=list)
    #: Creation time of the VPC endpoint.
    created_at = resource.Body('created_at')
    #: Description of the VPC endpoint.
    description = resource.Body('description')
    #: Domain name for accessing the associated VPC endpoint service.
    dns_names = resource.Body('dns_names', type=list)
    #: ID of the cluster associated with the VPC endpoint.
    endpoint_pool_id = resource.Body('endpoint_pool_id')
    #: ID of the VPC endpoint service.
    endpoint_service_id = resource.Body('endpoint_service_id')
    #: Name of the VPC endpoint service.
    endpoint_service_name = resource.Body('endpoint_service_name')
    #: VPC endpoint ID.
    id = resource.Body('id')
    #: IP address for accessing the associated VPC endpoint service.
    ip = resource.Body('ip')
    #: IP address for accessing the associated VPC endpoint service.
    port_ip = resource.Body('port_ip', alias='ip')
    #: Whether to create a private domain name.
    is_dns_enabled = resource.Body('enable_dns', type=bool)
    #: Whether the VPC endpoint is enabled.
    is_enabled = resource.Body('enable_status', type=bool)
    #: Whether access control is enabled.
    is_whitelist_enabled = resource.Body('enable_whitelist', type=bool)
    #: Packet ID of the VPC endpoint.
    marker_id = resource.Body('marker_id', type=int)
    #: Specifies the ID of the network in the VPC/Router.
    network_id = resource.Body('subnet_id')
    #: Project ID.
    project_id = resource.Body('project_id')
    #: IDs of route tables.
    route_tables = resource.Body('routetables', type=list)
    #: ID of the VPC/Router where the VPC endpoint is to be created.
    router_id = resource.Body('vpc_id')
    #: Type of the VPC endpoint service that is associated with the
    #:  VPC endpoint.
    service_type = resource.Body('service_type')
    #: Specifies the name of the VPC endpoint specifications.
    specification_name = resource.Body('specification_name')
    #: Specifies the connection status of the VPC endpoint.
    status = resource.Body('status')
    #: Lists the resource tags.
    tags = resource.Body('tags', type=list, list_type=TagsSpec)
    #: Update time of the VPC endpoint.
    updated_at = resource.Body('updated_at')
    #: Whitelist for controlling access to the VPC endpoint.
    whitelist = resource.Body('whitelist', type=list)

    @classmethod
    def existing(cls, connection=None, **kwargs):
        """Create an instance of an existing remote resource.

        When creating the instance set the ``_synchronized`` parameter
        of :class:`Resource` to ``True`` to indicate that it represents the
        state of an existing server-side resource. As such, all attributes
        passed in ``**kwargs`` are considered "clean", such that an immediate
        :meth:`update` call would not generate a body of attributes to be
        modified on the server.

        :param dict kwargs: Each of the named arguments will be set as
            attributes on the resulting Resource object.
        """
        if 'enable_status' in kwargs.keys():
            enable_status = kwargs['enable_status']
            kwargs['enable_status'] = (
                True if enable_status == 'enable' else False
            )
        return cls(_synchronized=True, connection=connection, **kwargs)

    def _translate_response(
        self,
        response,
        has_body=None,
        error_message=None,
        *,
        resource_response_key=None,
    ):
        """Given a KSA response, inflate this instance with its data

        DELETE operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body

        exceptions.raise_from_response(response, error_message=error_message)

        if has_body:
            try:
                body = response.json()
                if resource_response_key and resource_response_key in body:
                    body = body[resource_response_key]
                elif self.resource_key and self.resource_key in body:
                    body = body[self.resource_key]
                if 'enable_status' in body.keys():
                    enable_status = body['enable_status']
                    body['enable_status'] = (
                        True if enable_status == 'enable' else False
                    )
                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                body.pop("self", None)

                body_attrs = self._consume_body_attrs(body)
                if self._allow_unknown_attrs_in_body:
                    body_attrs.update(body)
                    self._unknown_attrs_in_body.update(body)
                elif self._store_unknown_attrs_as_properties:
                    body_attrs = self._pack_attrs_under_properties(
                        body_attrs, body
                    )

                self._body.attributes.update(body_attrs)
                self._body.clean()
                if self.commit_jsonpatch or self.allow_patch:
                    # We need the original body to compare against
                    self._original_body = body_attrs.copy()
            except ValueError:
                # Server returned not parse-able response (202, 204, etc)
                # Do simply nothing
                pass

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
        self._update_location()
        dict.update(self, self.to_dict())
