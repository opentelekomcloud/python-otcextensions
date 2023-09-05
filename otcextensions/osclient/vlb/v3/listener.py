#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''Listener v3 action implementations'''
import logging

from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_listener(obj):
    """Flatten the structure of the listener into a single dict
    """
    data = {
        'client_ca_tls_container_ref': obj.client_ca_tls_container_ref,
        'connection_limit': obj.connection_limit,
        'created_at': obj.created_at,
        'default_pool_id': obj.default_pool_id,
        'default_tls_container_ref': obj.default_tls_container_ref,
        'description': obj.description,
        'http2_enable': obj.http2_enable,
        'id': obj.id,
        'insert_headers': obj.insert_headers,
        'is_admin_state_up': obj.is_admin_state_up,
        'name': obj.name,
        'project_id': obj.project_id,
        'security_policy_id': obj.security_policy_id,
        'sni_match_algo': obj.sni_match_algo,
        'protocol': obj.protocol,
        'protocol_port': obj.protocol_port,
        'sni_container_refs': obj.sni_container_refs,
        'tags': obj.tags,
        'updated_at': obj.updated_at,
        'tls_ciphers_policy': obj.tls_ciphers_policy,
        'enable_member_retry': obj.enable_member_retry,
        'keepalive_timeout': obj.keepalive_timeout,
        'client_timeout': obj.client_timeout,
        'member_timeout': obj.member_timeout,
        'ipgroup': obj.ipgroup,
        'transparent_client_ip_enable': obj.transparent_client_ip_enable,
        'enhance_l7policy_enable': obj.enhance_l7policy
    }
    return data


def _add_loadbalancers_to_listener_obj(obj, data, columns):
    """Add associated loadbalancers to column and data tuples
    """
    i = 0
    for lb in obj.load_balancers:
        name = 'loadbalancers_id_' + str(i + 1)
        data += (lb['id'],)
        columns = columns + (name,)
        i += 1
    return data, columns


def _add_tags_to_listener_obj(obj, data, columns):
    data += ('\n'.join((f'value={tag["value"]}, key={tag["key"]}'
                        for tag in obj.tags)),)
    columns = columns + ('tags',)
    return data, columns


def _normalize_tags(tags):
    result = []
    for tag in tags:
        try:
            tag = tag.split('=')
            result.append({
                'key': tag[0],
                'value': tag[1]
            })
        except IndexError:
            result.append({'key': tag[0], 'value': ''})
    return result


class ListListeners(command.Lister):
    _description = _('List listeners')
    columns = ('ID', 'Name', 'provisioning_status')

    def get_parser(self, prog_name):
        parser = super(ListListeners, self).get_parser(prog_name)
        parser.add_argument(
            '--id',
            help=_('Specifies the listener ID.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Specifies the name of the listener added'
                   'to the load balancer.')
        )
        parser.add_argument(
            '--protocol-port',
            metavar='protocol_port',
            help=_('Specifies the port used by the listener.')
        )
        parser.add_argument(
            '--protocol',
            help=_('Specifies the protocol used by the listener.'
                   'The protocol can be UDP, TCP, HTTP, or HTTPS.'
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--description',
            help=_('Provides supplementary information about the listener.')
        )
        parser.add_argument(
            '--default-tls-container-ref',
            metavar='default_tls_container_ref',
            help=_('Specifies the ID of the server certificate used'
                   'by the listener.')
        )
        parser.add_argument(
            '--client-ca-tls-container-ref',
            metavar='<client_ca_tls_container_ref>',
            help=_('Limit the number of results displayed')
        )
        parser.add_argument(
            '--default-pool-id',
            metavar='default_pool_id',
            help=_('Specifies the ID of the default backend server group.')
        )
        parser.add_argument(
            '--http2-enable',
            metavar='<http2_enable>',
            type=bool,
            help=_('Specifies whether to use HTTP/2. This parameter'
                   'is available only for HTTPS listeners. If you configure'
                   'this parameter for other types of listeners,'
                   'it will not take effect.')
        )
        parser.add_argument(
            '--loadbalancer-id',
            metavar='loadbalancer_id',
            help=_('Specifies the ID of the load balancer'
                   'that the listener is added to.')
        )
        parser.add_argument(
            '--tls-ciphers-policy',
            metavar='<tls_ciphers_policy>',
            help=_('Specifies the security policy used by the listener.'
                   'This parameter is available only for HTTPS listeners.')
        )
        parser.add_argument(
            '--member-address',
            metavar='<member_address>',
            help=_('Specifies the private IP address bound'
                   'to the backend server.')
        )
        parser.add_argument(
            '--member-device-id',
            metavar='<member_device_id>',
            help=_('Specifies the ID of the cloud server that serves'
                   'as a backend server.')
        )
        parser.add_argument(
            '--enable-member-retry',
            metavar='<enable_member_retry>',
            type=bool,
            help=_('Specifies whether to enable health check retries'
                   'for backend servers.')
        )
        parser.add_argument(
            '--member-timeout',
            metavar='<member_timeout>',
            help=_('Specifies the timeout duration for waiting for a request'
                   'from a backend server, in seconds.')
        )
        parser.add_argument(
            '--client-timeout',
            metavar='<client_timeout>',
            help=_('Specifies the timeout duration for waiting for a request'
                   'from a client, in seconds.')
        )
        parser.add_argument(
            '--keepalive-timeout',
            metavar='<keepalive_timeout>',
            help=_('Specifies the idle timeout duration, in seconds.')
        )
        parser.add_argument(
            '--transparent-client-ip-enable',
            metavar='<transparent_client_ip_enable>',
            type=bool,
            help=_('Specifies whether to pass source IP addresses'
                   'of the clients to backend servers.')
        )
        parser.add_argument(
            '--limit',
            type=int,
            help=_('Specifies the number of records on each page.')
        )
        parser.add_argument(
            '--marker',
            help=_('Specifies the ID of the last record on the previous page.'
                   'This parameter must be used together with limit.')
        )
        parser.add_argument(
            '--page-reverse',
            metavar='page_reverse',
            type=bool,
            help=_('Specifies the page direction.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vlb

        args = {}
        if parsed_args.id:
            args['id'] = parsed_args.id
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.protocol_port:
            args['protocol_port'] = parsed_args.protocol_port
        if parsed_args.protocol:
            args['protocol'] = parsed_args.protocol
        if parsed_args.description:
            args['description'] = parsed_args.description
        if parsed_args.default_tls_container_ref:
            args['default_tls_container_ref'] =\
                parsed_args.default_tls_container_ref
        if parsed_args.client_ca_tls_container_ref:
            args['client_ca_tls_container_ref'] =\
                parsed_args.client_ca_tls_container_ref
        if parsed_args.default_pool_id:
            args['default_pool_id'] = parsed_args.default_pool_id
        if parsed_args.http2_enable is not None:
            args['http2_enable'] = parsed_args.http2_enable
        if parsed_args.loadbalancer_id:
            args['loadbalancer_id'] = parsed_args.loadbalancer_id
        if parsed_args.tls_ciphers_policy:
            args['tls_ciphers_policy'] = parsed_args.tls_ciphers_policy
        if parsed_args.member_address:
            args['member_address'] = parsed_args.member_address
        if parsed_args.member_device_id:
            args['member_device_id'] = parsed_args.member_device_id
        if parsed_args.enable_member_retry is not None:
            args['enable_member_retry'] = parsed_args.enable_member_retry
        if parsed_args.member_timeout:
            args['member_timeout'] = parsed_args.member_timeout
        if parsed_args.client_timeout:
            args['client_timeout'] = parsed_args.client_timeout
        if parsed_args.keepalive_timeout:
            args['keepalive_timeout'] = parsed_args.keepalive_timeout
        if parsed_args.transparent_client_ip_enable:
            args['transparent_client_ip_enable'] =\
                parsed_args.transparent_client_ip_enable
        if parsed_args.limit:
            args['limit'] = parsed_args.limit
        if parsed_args.marker:
            args['marker'] = parsed_args.marker
        if parsed_args.page_reverse:
            args['page_reverse'] = parsed_args.page_reverse
        data = client.listeners(**args)

        return (
            self.columns,
            (utils.get_item_properties(
                s, self.columns,
            ) for s in data)
        )


class ShowListener(command.ShowOne):
    _description = _('Shows details of a listener')
    columns = (
        'ID',
        'name',
        'client_ca_tls_container_ref',
        'provisioning_status',
        'connection_limit',
        'created_at',
        'default_pool_id',
        'default_tls_container_ref',
        'description',
        'http2_enable',
        'project_id',
        'protocol',
        'protocol_port',
        'sni_container_refs',
        'updated_at',
        'tls_ciphers_policy',
        'enable_member_retry',
        'keepalive_timeout',
        'client_timeout',
        'member_timeout',
        'transparent_client_ip_enable'
        )

    def get_parser(self, prog_name):
        parser = super(ShowListener, self).get_parser(prog_name)
        parser.add_argument(
            'listener',
            metavar='<listener>',
            help=_('ID or name of the listener')
        )
        return parser

    def take_action(self, parsed_args):
         client = self.app.client_manager.vlb

         obj = client.find_listener(
             name_or_id=parsed_args.listener,
             ignore_missing=False
         )

         data = utils.get_dict_properties(
             _flatten_listener(obj), self.columns)
         if obj.load_balancers:
             data, self.columns = _add_loadbalancers_to_listener_obj(
                 obj, data, self.columns)

         return self.columns, data


class CreateListener(command.ShowOne):
    _description = _('Create listener')
    columns = (
        'ID',
        'name',
        'client_ca_tls_container_ref',
        'provisioning_status',
        'connection_limit',
        'created_at',
        'default_pool_id',
        'default_tls_container_ref',
        'description',
        'http2_enable',
        'project_id',
        'protocol',
        'protocol_port',
        'sni_container_refs',
        'updated_at',
        'tls_ciphers_policy',
        'enable_member_retry',
        'keepalive_timeout',
        'client_timeout',
        'member_timeout',
        'transparent_client_ip_enable'
    )

    def get_parser(self, prog_name):
        parser = super(CreateListener, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name of the load balancer')
        )
        parser.add_argument(
            '--client-ca-tls-container-ref',
            metavar='<client_ca_tls_container_ref>',
            help=_('Specifies the ID of the CA certificate'
                   'used by the listener.')
        )
        parser.add_argument(
            '--default-pool-id',
            metavar='<default_pool_id>',
            help=_('Specifies the ID of the default backend server group.'
                   'If there is no matched forwarding policy, requests are'
                   'forwarded to the default backend server for processing.')
        )
        parser.add_argument(
            '--default-tls-container-ref',
            metavar='<default_tls_container_ref>',
            help=_('Specifies the ID of the server certificate'
                   'used by the listener.')
        )
        parser.add_argument(
            '--description',
            type=str,
            help=_('Provides supplementary information about the listener.')
        )
        parser.add_argument(
            '--http2-enable',
            action='store_true',
            help=_('Specifies whether to use HTTP/2. This parameter'
                   'is available only for HTTPS listeners. If you configure'
                   'this parameter for other types of listeners, it will not'
                   'take effect.')
        )
        parser.add_argument(
            '--insert-headers',
            metavar='<insert_headers>',
            type=dict,
            help=_('insert_headers')
        )
        parser.add_argument(
            '--loadbalancer-id',
            metavar='<loadbalancer_id>',
            required=True,
            help=_('Specifies the ID of the load balancer that the listener'
                   'is added to.')
        )
        parser.add_argument(
            '--project-id',
            metavar='project_id',
            help=_('Specifies the project ID.')
        )
        parser.add_argument(
            '--protocol',
            required=True,
            choices=['TCP', 'HTTP', 'UDP', 'HTTPS'],
            help=_('Specifies the protocol used by the listener.')
        )
        parser.add_argument(
            '--protocol-port',
            metavar='<protocol_port>',
            type=int,
            required=True,
            help=_('Specifies the port used by the listener.')
        )
        parser.add_argument(
            '--sni-container-refs',
            action='append',
            dest='sni_container_refs',
            help=_('Lists the IDs of SNI certificates (server certificates'
                   'with domain names) used by the listener.'
                   'This parameter will be ignored and an empty array will be'
                   'returned if the listener protocol is not HTTPS.')
        )
        parser.add_argument(
            '--sni-match-algo',
            metavar='<sni_match_algo>',
            help=_('Specifies how wildcard domain name matches with the SNI'
                   'certificates used by the listener.'
                   'longest_suffix indicates longest suffix match.'
                   'wildcard indicates wildcard match.'
                   'The default value is wildcard.')
        )
        parser.add_argument(
            '--tag',
            action='append',
            metavar='<tags>',
            help=_('Lists the tags.')
        )
        parser.add_argument(
            '--tls-ciphers-policy',
            metavar='<tls_ciphers_policy>',
            choices=['tls-1-0', 'tls-1-1', 'tls-1-2', 'tls-1-2-strict'],
            help=_('Specifies the security policy that will be used'
                   'by the listener. This parameter is available only for'
                   'HTTPS listeners. The default value is tls-1-0.')
        )
        parser.add_argument(
            '--security-policy-id',
            metavar='<security_policy_id>',
            help=_('Specifies the ID of the custom security policy.')
        )
        parser.add_argument(
            '--disable-member-retry',
            action='store_true',
            help=_('Specifies whether to enable health check retries for'
                   'backend servers. This parameter is available only for'
                   'HTTP and HTTPS listeners.')
        )
        parser.add_argument(
            '--keepalive-timeout',
            metavar='<keepalive_timeout>',
            type=int,
            help=_('Specifies the idle timeout duration, in seconds.')
        )
        parser.add_argument(
            '--client-timeout',
            metavar='<client_timeout>',
            type=int,
            help=_('Specifies the timeout duration for waiting for'
                   'a request from a client, in seconds. This parameter is'
                   'available only for HTTP and HTTPS listeners.'
                   '60 by default.')
        )
        parser.add_argument(
            '--member-timeout',
            metavar='<member_timeout>',
            type=int,
            help=_('Specifies the timeout duration for waiting for a request'
                   'from a backend server, in seconds. This parameter is'
                   'available only for HTTP and HTTPS listeners.'
                   'The value ranges from 1 to 300, and the default'
                   'value is 60.')
        )
        parser.add_argument(
            '--ipgroup-id',
            metavar='<ipgroup_id>',
            help=_('Specifies the ID of the IP address group associated with'
                   'the listener.')
        )
        parser.add_argument(
            '--disable-ipgroup',
            action='store_true', #default enable true
            help=_('Specifies whether to enable access control.')
        )
        parser.add_argument(
            '--ipgroup-type',
            metavar='<ipgroup_type>',
            help=_('Specifies how access to the listener is controlled.'
                   'Can be black and white.')
        )
        parser.add_argument(
            '--enable-enhance_l7policy',
            action='store_true',  #default false
            help=_('Specifies whether to enable advanced forwarding.'
                   'If advanced forwarding is enabled, more flexible'
                   'forwarding policies and rules are supported.')
        )
        return parser

    def take_action(self, parsed_args):
        attrs = {}

        attrs['protocol'] = parsed_args.protocol
        attrs['protocol_port'] = parsed_args.protocol_port
        attrs['loadbalancer_id'] = parsed_args.loadbalancer_id

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.client_ca_tls_container_ref:
            attrs['client_ca_tls_container_ref'] =\
                parsed_args.client_ca_tls_container_ref
        if parsed_args.default_pool_id:
            attrs['default_pool_id'] = parsed_args.default_pool_id
        if parsed_args.default_tls_container_ref:
            attrs['default_tls_container_ref'] =\
                parsed_args.default_tls_container_ref
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.http2_enable:
            attrs['http2_enable'] = True
        if parsed_args.insert_headers:
            attrs['insert_headers'] = parsed_args.insert_headers
        if parsed_args.project_id:
            attrs['project_id'] = parsed_args.project_id
        if parsed_args.sni_container_refs:
            attrs['sni_container_refs'] = parsed_args.sni_container_refs
        if parsed_args.sni_match_algo:
            attrs['sni_match_algo'] = parsed_args.sni_match_algo
        if parsed_args.tags:
            attrs['tags'] = parsed_args.tags
        if parsed_args.tls_ciphers_policy:
            attrs['tls_ciphers_policy'] = parsed_args.tls_ciphers_policy
        if parsed_args.security_policy_id:
            attrs['security_policy_id'] = parsed_args.security_policy_id
        if parsed_args.disable_member_retry is True:
            attrs['enable_member_retry'] = False
        if parsed_args.keepalive_timeout:
            attrs['keepalive_timeout'] = parsed_args.keepalive_timeout
        if parsed_args.client_timeout:
            attrs['client_timeout'] = parsed_args.client_timeout
        if parsed_args.member_timeout:
            attrs['member_timeout'] = parsed_args.member_timeout
        if parsed_args.enable_enhance_l7policy:
            attrs['enable_enhance_l7policy'] = True
        if parsed_args.ipgroup_id:
            attrs['ipgroup'] = {'ipgroup_id': parsed_args.ipgroup_id}
            if parsed_args.disable_ipgroup is True:
                attrs['ipgroup']['enable_ipgroup'] = False
            if parsed_args.ipgroup_type:
                attrs['ipgroup']['type'] = parsed_args.ipgroup_type

        client = self.app.client_manager.vlb
        obj = client.create_listener(**attrs)

        data = utils.get_dict_properties(
            _flatten_listener(obj), self.columns)

        if obj.tags:
            data, self.columns = _add_tags_to_listener_obj(
                obj, data, self.columns)
        if obj.loadbalancers:
            data, self.columns = _add_loadbalancers_to_listener_obj(
                obj, data, self.columns)
        return self.columns, data


class UpdateListener(command.ShowOne):
    _description = _('Update listener')
    columns = (
        'ID',
        'name',
        'client_ca_tls_container_ref',
        'connection_limit',
        'created_at',
        'default_pool_id',
        'default_tls_container_ref',
        'description',
        'insert_headers',
        'http2_enable',
        'project_id',
        'protocol',
        'protocol_port',
        'sni_container_refs',
        'updated_at',
        'tls_ciphers_policy',
        'enable_member_retry',
        'keepalive_timeout',
        'client_timeout',
        'member_timeout',
        'transparent_client_ip_enable'
    )

    def get_parser(self, prog_name):
        parser = super(UpdateListener, self).get_parser(prog_name)
        parser.add_argument(
            'listener',
            help=_('Specifies listener name of id.')
        )
        parser.add_argument(
            '--name',
            help=_('Specifies the new name.')
        )
        parser.add_argument(
            '--client-ca-tls-container-ref',
            metavar='<client_ca_tls_container_ref>',
            help=_('Specifies the ID of the CA certificate'
                   'used by the listener.')
        )
        parser.add_argument(
            '--default-pool-id',
            metavar='<default_pool_id>',
            help=_('Specifies the ID of the default backend server group.'
                   'If there is no matched forwarding policy, requests are'
                   'forwarded to the default backend server for processing.')
        )
        parser.add_argument(
            '--default-tls-container-ref',
            metavar='<default_tls_container_ref>',
            help=_('Specifies the ID of the server certificate'
                   'used by the listener.')
        )
        parser.add_argument(
            '--description',
            type=str,
            help=_('Provides supplementary information about the listener.')
        )
        parser.add_argument(
            '--http2-enable',
            type='store_true',
            help=_('Specifies whether to use HTTP/2. This parameter'
                   'is available only for HTTPS listeners. If you configure'
                   'this parameter for other types of listeners, it will not'
                   'take effect.')
        )
        parser.add_argument(
            '--insert-headers',
            metavar='<insert_headers>',
            type=dict,
            help=_('insert_headers')
        )
        parser.add_argument(
            '--sni-container-refs',
            action='append',
            dest='sni_container_refs',
            help=_('Lists the IDs of SNI certificates (server certificates'
                   'with domain names) used by the listener.'
                   'This parameter will be ignored and an empty array will be'
                   'returned if the listener protocol is not HTTPS.')
        )
        parser.add_argument(
            '--sni-match-algo',
            metavar='<sni_match_algo>',
            help=_('Specifies how wildcard domain name matches with the SNI'
                   'certificates used by the listener. longest_suffix indicates'
                   'longest suffix match. wildcard indicates wildcard match.')
        )
        parser.add_argument(
            '--tls-ciphers-policy',
            metavar='<tls_ciphers_policy>',
            choices=['tls-1-0', 'tls-1-1', 'tls-1-2', 'tls-1-2-strict'],
            help=_('Specifies the security policy that will be used'
                   'by the listener. This parameter is available only for'
                   'HTTPS listeners. The default value is tls-1-0.')
        )
        parser.add_argument(
            '--security-policy-id',
            metavar='<security_policy_id>',
            help=_('Specifies the ID of the custom security policy.')
        )
        parser.add_argument(
            '--disable-member-retry',
            action='story_true',
            help=_('Specifies whether to enable health check retries for'
                   'backend servers. This parameter is available only for'
                   'HTTP and HTTPS listeners.')
        )
        parser.add_argument(
            '--keepalive-timeout',
            metavar='<keepalive_timeout>',
            type=int,
            help=_('Specifies the idle timeout duration, in seconds.')
        )
        parser.add_argument(
            '--client-timeout',
            metavar='<client_timeout>',
            type=int,
            help=_('Specifies the timeout duration for waiting for'
                   'a request from a client, in seconds. This parameter is'
                   'available only for HTTP and HTTPS listeners.'
                   '60 by default.')
        )
        parser.add_argument(
            '--member-timeout',
            metavar='<member_timeout>',
            type=int,
            help=_('Specifies the timeout duration for waiting for a request'
                   'from a backend server, in seconds. This parameter is'
                   'available only for HTTP and HTTPS listeners.'
                   'The value ranges from 1 to 300, and the default'
                   'value is 60.')
        )
        parser.add_argument(
            '--ipgroup-id',
            metavar='<ipgroup_id>',
            help=_('Specifies the ID of the IP address group associated with'
                   'the listener.')
        )
        parser.add_argument(
            '--disable-ipgroup',
            action='store_true',
            help=_('Specifies whether to enable access control.')
        )
        parser.add_argument(
            '--ipgroup-type',
            metavar='<ipgroup_type>',
            help=_('Specifies how access to the listener is controlled.'
                   'Can be black and white.')
        )
        parser.add_argument(
            '--enable-enhance_l7policy',
            action='store_true',  #default false
            help=_('Specifies whether to enable advanced forwarding.'
                   'If advanced forwarding is enabled, more flexible'
                   'forwarding policies and rules are supported.')
        )
        return parser

    def take_action(self, parsed_args):
        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.client_ca_tls_container_ref:
            attrs['client_ca_tls_container_ref'] =\
                parsed_args.client_ca_tls_container_ref
        if parsed_args.default_pool_id:
            attrs['default_pool_id'] = parsed_args.default_pool_id
        if parsed_args.default_tls_container_ref:
            attrs['default_tls_container_ref'] =\
                parsed_args.default_tls_container_ref
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.http2_enable is True:
            attrs['http2_enable'] = True
        if parsed_args.insert_headers:
            attrs['insert_headers'] = parsed_args.insert_headers
        if parsed_args.sni_container_refs:
            attrs['sni_container_refs'] = parsed_args.sni_container_refs
        if parsed_args.sni_match_algo:
            attrs['sni_match_algo'] = parsed_args.sni_match_algo
        if parsed_args.tls_ciphers_policy:
            attrs['tls_ciphers_policy'] = parsed_args.tls_ciphers_policy
        if parsed_args.security_policy_id:
            attrs['security_policy_id'] = parsed_args.security_policy_id
        if parsed_args.disable_member_retry is True:
            attrs['enable_member_retry'] = False
        if parsed_args.keepalive_timeout:
            attrs['keepalive_timeout'] = parsed_args.keepalive_timeout
        if parsed_args.client_timeout:
            attrs['client_timeout'] = parsed_args.client_timeout
        if parsed_args.member_timeout:
            attrs['member_timeout'] = parsed_args.member_timeout
        if parsed_args.ipgroup_id or parsed_args.enable_ipgroup or\
                parsed_args.ipgroup_type:
            attrs['ipgroup'] = {}
            if parsed_args.ipgroup_id:
                attrs['ipgroup']['ipgroup_id'] = parsed_args.ipgroup_id
            if parsed_args.disable_ipgroup is True:
                attrs['ipgroup']['enable_ipgroup'] = False
            if parsed_args.ipgroup_type:
                attrs['ipgroup']['type'] = parsed_args.ipgroup_type

        client = self.app.client_manager.vlb

        listener = client.find_listener(
            name_or_id=parsed_args.listener,
            ignore_missing=False
        )
        obj = client.update_listener(listener=listener.id, **attrs)

        data = utils.get_dict_properties(
            _flatten_listener(obj), self.columns)

        return self.columns, data


class DeleteListener(command.Command):
    _description = _('Delete listener')

    def get_parser(self, prog_name):
        parser = super(DeleteListener, self).get_parser(prog_name)
        parser.add_argument(
            'listener',
            help=_('ID or name of the listener')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        listener = client.find_listener(
            name_or_id=parsed_args.listener,
            ignore_missing=False
        )

        self.app.client_manager.vlb.delete_listener(
            listener=listener.id,
            ignore_missing=False)
