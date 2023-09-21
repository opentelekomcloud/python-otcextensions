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


class Listener(resource.Resource):
    resource_key = 'listener'
    resources_key = 'listeners'
    base_path = '/elb/listeners'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'protocol_port', 'protocol', 'description',
        'default_tls_container_ref', 'client_ca_tls_container_ref',
        'connection_limit', 'default_pool_id',
        'id', 'name', 'http2_enable', 'loadbalancer_id', 'tls_ciphers_policy',
        'sni_container_refs', 'admin_state_up', 'tls_container_id'
    )

    # Properties
    #: Specifies the ID of the CA certificate used by the listener.
    client_ca_tls_container_ref = resource.Body('client_ca_tls_container_ref')
    #: Specifies the timeout duration for waiting
    #: for a request from a client, in seconds.
    client_timeout = resource.Body('client_timeout', type=int)
    #: Timestamp when the load balancer was created
    created_at = resource.Body('created_at')
    #: Specifies the maximum number of connections.
    connection_limit = resource.Body('connection_limit', type=int)
    #: The listener description
    description = resource.Body('description')
    #: Specifies the ID of the default backend server group.
    default_pool_id = resource.Body('default_pool_id')
    #: Specifies the ID of the server certificate used by the listener.
    default_tls_container_ref = resource.Body('default_tls_container_ref')
    #: Specifies whether to enable health check retries for backend servers.
    enable_member_retry = resource.Body('enable_member_retry', type=bool)
    #: Specifies whether to enable advanced forwarding.
    enhance_l7policy = resource.Body('enhance_l7policy_enable', type=bool)
    #: Specifies whether to use HTTP/2.
    http2_enable = resource.Body('http2_enable', type=bool)
    #: Dictionary of additional headers insertion into HTTP header.
    insert_headers = resource.Body('insert_headers', type=dict)
    #: Specifies the administrative status of the listener.
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: List of load balancers associated with this listener.
    #: *Type: list of dicts which contain the load balancer IDs*
    load_balancers = resource.Body('loadbalancers', type=list, elements=dict)
    #: Specifies the ID of the load balancer that the listener is added to.
    loadbalancer_id = resource.Body('loadbalancer_id')
    #: Specifies the IP address group associated with the listener.
    ipgroup = resource.Body('ipgroup', type=dict)
    #: Name of the listener.
    name = resource.Body('name')
    #: Specifies whether to enable health check retries for backend servers.
    keepalive_timeout = resource.Body('keepalive_timeout', type=int)
    #: Specifies the timeout duration for waiting
    #: for a request from a backend server, in seconds.
    member_timeout = resource.Body('member_timeout', type=int)
    #: The protocol of the listener, which is TCP, HTTP, HTTPS
    #: or TERMINATED_HTTPS.
    protocol = resource.Body('protocol')
    #: Port the listener will listen to, e.g. 80.
    protocol_port = resource.Body('protocol_port', type=int)
    #: The ID of the project this listener is associated with.
    project_id = resource.Body('project_id')
    #: Specifies the ID of the custom security policy.
    security_policy_id = resource.Body('security_policy_id')
    #: A list of references to TLS secrets.
    #: *Type: list*
    sni_container_refs = resource.Body('sni_container_refs', type=list)
    #: Specifies how wildcard domain name matches with the
    # SNI certificates used by the listener.
    sni_match_algo = resource.Body('sni_match_algo')
    #: Lists the tags.
    tags = resource.Body('tags', type=list)
    #: Specifies whether to pass source IP addresses of the clients to
    # backend servers.
    transparent_client_ip_enable = resource.Body(
        'transparent_client_ip_enable', type=bool)
    #: Specifies the security policy that will be used by the listener.
    tls_ciphers_policy = resource.Body('tls_ciphers_policy')
    #: Timestamp when the listener was last updated.
    updated_at = resource.Body('updated_at')
