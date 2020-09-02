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

from otcextensions.sdk.waf.v1 import _base


class ServerEntry(resource.Resource):
    #: Properties
    #: IP address
    address = resource.Body('address')
    #: Client protocol
    client_protocol = resource.Body('client_protocol')
    #: Server protocol
    server_protocol = resource.Body('server_protocol')
    #: Port number
    port = resource.Body('port', type=int)


class Domain(_base.Resource):
    """WAF Domain Resource"""
    resources_key = 'items'
    base_path = '/waf/instance'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'name', 'hostname', 'policy_name', 'limit', 'offset',
        policy_name='policyname',
        name='hostname')

    #: Properties
    #: Specifies whether a domain name is connected to WAF
    access_status = resource.Body('access_status', type=int)
    #: Certificate ID.
    #: This parameter is mandatory when client_protocol is set to HTTPS.
    certificate_id = resource.Body('certificate_id')
    #: CNAME
    cname = resource.Body('cname')
    #: domain name
    name = resource.Body('hostname', aka='hostname')
    #: Specifies the policy ID.
    policy_id = resource.Body('policy_id')
    #: protocol type of the client. The options are HTTP, HTTPS, and HTTP,HTTPS.
    protocol = resource.Body('protocol')
    #: WAF mode.
    protect_status = resource.Body('protect_status', type=int)
    #: Specifies whether a proxy is configured.
    proxy = resource.Body('proxy', type=bool)
    #: Specifies the origin server information, including the client_protocol,
    #: server_protocol, address, and port fields.
    server = resource.Body('server', type=list, list_type=ServerEntry)
    #: source IP header. This parameter is required only when proxy is set
    #: to true.
    #: The options are as follows: default, cloudflare, akamai, and custom.
    sip_header_name = resource.Body('sip_header_name')
    #: Specifies the HTTP request header for identifying the real source IP
    #: address. This parameter is required only when proxy is set to true.
    #: - If sip_header_name is default, sip_header_list is ["X-Forwarded-For"].
    #: - If sip_header_name is cloudflare, sip_header_list is
    #: ["CF-Connecting-IP", "X-Forwarded-For"].
    #: - If sip_header_name is akamai, sip_header_list is ["True-Client-IP"].
    #: - If sip_header_name is custom, you can customize a value.
    sip_header_list = resource.Body('sip_header_list', type=list)
    #: subdomain name.
    #: This parameter is returned only when proxy is set to true.
    subdomain = resource.Body('sub_domain')
    #: Certificate uploading timestamp
    timestamp = resource.Body('timestamp')
    #: TXT record. This parameter is returned only when proxy is set to true.
    txt_record = resource.Body('txt_code')
