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
        'description', 'name', 'project_id', 'provider',
    )

    # Properties
    #: List of IPv4 or IPv6 CIDRs.
    allowed_cidrs = resource.Body('allowed_cidrs', type=list)
    #: Specifies the ID of the CA certificate used by the listener.
    client_ca_tls_container_ref = resource.Body('client_ca_tls_container_ref')
    #: Specifies the timeout duration for waiting
    #: for a request from a client, in seconds.
    client_timeout = resource.Body('client_timeout', type=int)
    #: Specifies the maximum number of connections.
    connection_limit = resource.Body('connection_limit', type=int)
    #: Timestamp when the load balancer was created
    created_at = resource.Body('created_at')
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
    #: Specifies the IP address group associated with the listener.
    ipgroup = resource.Body('ipgroup', type=dict)
    #: The administrative state of the load balancer *Type: bool*
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies whether to enable health check retries for backend servers.
    keepalive_timeout = resource.Body('keepalive_timeout', type=int)
    #: List of l7policies associated with this listener.
    l7_policies = resource.Body('l7policies', type=list)
    #: The ID of the parent load balancer.
    load_balancer_id = resource.Body('loadbalancer_id')
    #: List of load balancers associated with this listener.
    #: *Type: list of dicts which contain the load balancer IDs*
    load_balancers = resource.Body('loadbalancers', type=list)
    #: Specifies the timeout duration for waiting
    #: for a request from a backend server, in seconds.
    member_timeout = resource.Body('member_timeout', type=int)
    #: Operating status of the listener.
    operating_status = resource.Body('operating_status')
    #: The ID of the project this listener is associated with.
    project_id = resource.Body('project_id')
    #: The protocol of the listener, which is TCP, HTTP, HTTPS
    #: or TERMINATED_HTTPS.
    protocol = resource.Body('protocol')
    #: Port the listener will listen to, e.g. 80.
    protocol_port = resource.Body('protocol_port', type=int)
    #: The provisioning status of this listener.
    provisioning_status = resource.Body('provisioning_status')
    #: A list of references to TLS secrets.
    #: *Type: list*
    sni_container_refs = resource.Body('sni_container_refs', type=list)
    #: Lists the tags.
    tags = resource.Body('tags', type=list)
    #: Frontend client inactivity timeout in milliseconds.
    timeout_client_data = resource.Body('timeout_client_data', type=int)
    #: Backend member connection timeout in milliseconds.
    timeout_member_connect = resource.Body('timeout_member_connect', type=int)
    #: Backend member inactivity timeout in milliseconds.
    timeout_member_data = resource.Body('timeout_member_data', type=int)
    #: Time, in milliseconds, to wait for additional TCP packets for content
    #: inspection.
    timeout_tcp_inspect = resource.Body('timeout_tcp_inspect', type=int)
    #: Stores a cipher string in OpenSSL format.
    tls_ciphers = resource.Body('tls_ciphers')
    #: Specifies the security policy that will be used by the listener.
    tls_ciphers_policy = resource.Body('tls_ciphers_policy')
    #: A lsit of TLS protocols to be used by the listener
    tls_versions = resource.Body('tls_versions', type=list)
    #: Specifies whether to pass source IP addresses of the clients
    #: to backend servers.
    transparent_ip = resource.Body('transparent_client_ip_enable', type=bool)
    #: Timestamp when the listener was last updated.
    updated_at = resource.Body('updated_at')
