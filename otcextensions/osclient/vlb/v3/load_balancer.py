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
'''LoadBalancer v3 action implementations'''
import logging

from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_loadbalancer(obj):
    """Flatten the structure of the loadbalancer into a single dict
    """
    data = {
        'id': obj.id,
        'name': obj.name,
        'description': obj.description,
        'provisioning_status': obj.provisioning_status,
        'provider': obj.provider,
        'operating_status': obj.operating_status,
        'ip_address': obj.ip_address,
        'is_admin_state_up': obj.is_admin_state_up,
        'subnet_id': obj.subnet_id,
        'subnet_type': obj.subnet_type,
        'project_id': obj.project_id,
        'port_id': obj.port_id,
        'created_at': obj.created_at,
        'updated_at': obj.updated_at,
        'is_guaranteed': obj.is_guaranteed,
        'vpc_id': obj.vpc_id,
        'availability_zone_list': obj.availability_zones,
        'l4_flavor_id': obj.l4_flavor_id,
        'l7_flavor_id': obj.l7_flavor_id,
        'network_ids': obj.network_ids,
        'deletion_protection_enable': obj.deletion_protection_enable,
        'ip_target_enable': obj.ip_target_enable
    }
    return data


def _add_eips_to_load_balancer_obj(obj, data, columns):
    """Add associated eips to column and data tuples
    """
    i = 0
    for eip in obj.eips:
        data += (eip['eip_id'],)
        columns = columns + ('eip_id_' + str(i + 1),)
        data += (eip['eip_address'],)
        columns = columns + ('eip_address_' + str(i + 1),)
        data += (eip['ip_version'],)
        columns = columns + ('ip_version_' + str(i + 1),)
        i += 1
    return data, columns


def _add_publicips_to_load_balancer_obj(obj, data, columns):
    """Add associated public ips to column and data tuples
    """
    i = 0
    for fip in obj.floating_ips:
        data += (fip['publicip_id'],)
        columns = columns + ('publicip_id_' + str(i + 1),)
        data += (fip['publicip_address'],)
        columns = columns + ('publicip_address_' + str(i + 1),)
        data += (fip['ip_version'],)
        columns = columns + ('publicip_ip_version_' + str(i + 1),)
        i += 1
    return data, columns


def _add_pools_to_load_balancer_obj(obj, data, columns):
    """Add associated pools to column and data tuples
    """
    i = 0
    for pool in obj.pools:
        name = 'pool_id_' + str(i + 1)
        data += (pool['id'],)
        columns = columns + (name,)
        i += 1
    return data, columns


def _add_listeners_to_load_balancer_obj(obj, data, columns):
    """Add associated listeners to column and data tuples
    """
    i = 0
    for s in obj.listeners:
        name = 'listener_id_' + str(i + 1)
        data += (obj.listeners[i]['id'],)
        columns = columns + (name,)
        i += 1
    return data, columns


def _add_tags_to_load_balancer_obj(obj, data, columns):
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


class ListLoadBalancers(command.Lister):
    _description = _('List load balancers')
    columns = ('ID',
               'Name',
               'description',
               'provider',
               'operating_status',
               'project_id',
               'vpc_id')

    def get_parser(self, prog_name):
        parser = super(ListLoadBalancers, self).get_parser(prog_name)
        parser.add_argument(
            '--id',
            required=False,
            help=_('Specifies the load balancer ID.')
        )
        parser.add_argument(
            '--name',
            help=_('Specifies the load balancer name.')
        )
        parser.add_argument(
            '--marker',
            metavar='<marker>',
            help=_('Specifies the ID of the last record on the previous page.')
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            default=None,
            help=_('Limit the number of results displayed')
        )
        parser.add_argument(
            '--page-reverse',
            metavar='page_reverse',
            type=bool,
            dest='page_reverse',
            help=_('Specifies the page direction.')
        )
        parser.add_argument(
            '--description',
            help=_('Provides supplementary information about the'
                   'load balancer')
        )
        parser.add_argument(
            '--provisioning-status',
            metavar='<provisioning_status>',
            help=_('Specifies the provisioning status of the load balancer.')
        )
        parser.add_argument(
            '--operating-status',
            metavar='<operating_status>',
            help=_('Specifies the operating status of the load balancer.')
        )
        parser.add_argument(
            '--guaranteed',
            metavar='guaranteed',
            type=bool,
            dest='guaranteed',
            help=_('Specifies whether the load balancer is a dedicated'
                   'load balancer. The value can only be true.')
        )
        parser.add_argument(
            '--vpc-id',
            metavar='<vpc_id>',
            help=_('Specifies the ID of the VPC where the load'
                   'balancer works.')
        )
        parser.add_argument(
            '--port-id',
            dest='vip_port_id',
            help=_('Specifies the ID of the port bound to the virtual'
                   'IP address of the load balancer.')
        )
        parser.add_argument(
            '--ip-address',
            dest='vip_address',
            help=_('Specifies the virtual IP address bound'
                   ' to the load balancer.')
        )
        parser.add_argument(
            '--subnet-id',
            dest='vip_subnet_cidr_id',
            help=_('Specifies the ID of the subnet where the'
                   ' load balancer works.')
        )
        parser.add_argument(
            '--eip',
            dest='eips',
            action='append',
            help=_('Specifies the EIP bound to the load balancer.')
        )
        parser.add_argument(
            '--publicip',
            dest='publicips',
            action='append',
            help=_('Specifies the public IP address bound'
                   'to the load balancer.')
        )
        parser.add_argument(
            '--availability-zone-list',
            metavar='<availability_zone_list>',
            help=_('Specifies the list of AZs where the load balancer'
                   'is created.')
        )
        parser.add_argument(
            '--l4-flavor-id',
            metavar='<l4_flavor_id>',
            help=_('Specifies the ID of the flavor at Layer 4.')
        )
        parser.add_argument(
            '--l7-flavor-id',
            metavar='<l7_flavor_id>',
            help=_('Specifies the ID of the flavor at Layer 7.')
        )
        parser.add_argument(
            '--member-device-id',
            metavar='<member_device_id>',
            help=_('Specifies the ID of the cloud server that serves as'
                   'a backend server.')
        )
        parser.add_argument(
            '--member-address',
            metavar='<member_address>',
            help=_('Specifies the private IP address of the backend server.')
        )
        parser.add_argument(
            '--ip-version',
            metavar='<ip_version>',
            help=_('Specifies the IP version. The value can be 4 (IPv4)'
                   'or 6 (IPv6).')
        )
        parser.add_argument(
            '--subnet-type',
            dest='elb_virsubnet_type',
            help=_('Specifies the type of the subnet on the downstream plane.')
        )
        parser.add_argument(
            '--deletion-protection-enable',
            metavar='<deletion_protection_enable>',
            type=bool,
            help=_('Specifies whether to enable deletion protection.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vlb
        query = {}

        args_list = ['id', 'name', 'marker', 'limit', 'page_reverse',
                     'description', 'provisioning_status', 'operating_status',
                     'guaranteed', 'vpc_id', 'vip_port_id',
                     'eips', 'publicips', 'vip_address', 'vip_subnet_cidr_id',
                     'availability_zone_list', 'l4_flavor_id', 'l7_flavor_id',
                     'member_device_id', 'member_address', 'ip_version',
                     'elb_virsubnet_type', 'deletion_protection_enable']

        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val is not None:
                query[arg] = val
        data = client.load_balancers(**query)
        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_loadbalancer(s), self.columns,
                 ) for s in data))
        return table


class ShowLoadBalancer(command.ShowOne):
    _description = _('Shows details of a Load balancer')
    columns = (
        'id',
        'name',
        'description',
        'subnet_id',
        'subnet_type',
        'port_id',
        'provider',
        'ip_address',
        'provisioning_status',
        'operating_status',
        'project_id',
        'created_at',
        'updated_at',
        'guaranteed',
        'vpc_id',
        'availability_zone_list',
        'l4_flavor_id',
        'l7_flavor_id',
        'network_ids',
        'deletion_protection_enable',
        'ip_target_enable'
    )

    def get_parser(self, prog_name):
        parser = super(ShowLoadBalancer, self).get_parser(prog_name)
        parser.add_argument(
            'loadbalancer',
            metavar='<loadbalancer>',
            help=_('ID or name of the load balancer')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vlb

        obj = client.find_load_balancer(
            name_or_id=parsed_args.loadbalancer,
            ignore_missing=False
        )

        data = utils.get_dict_properties(
            _flatten_loadbalancer(obj), self.columns)
        if obj.eips:
            data, self.columns = _add_eips_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.floating_ips:
            data, self.columns = _add_publicips_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.listeners:
            data, self.columns = _add_listeners_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.pools:
            data, self.columns = _add_pools_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.tags:
            data, self.columns = _add_tags_to_load_balancer_obj(
                obj, data, self.columns)
        return self.columns, data


class CreateLoadBalancer(command.ShowOne):
    _description = _('Create Load balancer')
    columns = (
        'ID',
        'description',
        'provisioning_status',
        'provider',
        'operating_status',
        'ip_address',
        'subnet_id',
        'name',
        'project_id',
        'port_id',
        'created_at',
        'updated_at',
        'guaranteed',
        'vpc_id',
        'availability_zone_list',
        'l4_flavor_id',
        'l7_flavor_id',
        'network_ids'
    )

    def get_parser(self, prog_name):
        parser = super(CreateLoadBalancer, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name of the load balancer')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('User-defined Load balancer description.')
        )
        parser.add_argument(
            '--ip-address',
            metavar='ip_address',
            dest='vip_address',
            help=_('Specifies the virtual IP address'
                   'bound to the load balancer.')
        )
        parser.add_argument(
            '--subnet-id',
            metavar='subnet_id',
            dest='vip_subnet_cidr_id',
            help=_('Specifies the ID of the IPv4 subnet where the load'
                   'balancer works. ')
        )
        parser.add_argument(
            '--provider',
            metavar='<provider>',
            help=_('Specifies the provider of the load balancer.')
        )
        parser.add_argument(
            '--l4-flavor-id',
            metavar='<l4_flavor_id>',
            help=_('Specifies the ID of the Layer-4 flavor.'
                   'Specify either l4_flavor_id or l7_flavor_id or both'
                   'l4_flavor_id and l7_flavor_id when you create'
                   'a load balancer.')
        )
        parser.add_argument(
            '--l7-flavor-id',
            metavar='<l7_flavor_id>',
            help=_('Specifies the ID of the Layer-7 flavor.'
                   'Specify either l4_flavor_id or l7_flavor_id or both'
                   'l4_flavor_id and l7_flavor_id when you create'
                   'a load balancer.')
        )
        parser.add_argument(
            '--vpc-id',
            metavar='<vpc_id>',
            help=_('Specifies the ID of the VPC where the load balancer'
                   'works.')
        )
        parser.add_argument(
            '--availability-zone',
            dest='availability_zone_list',
            action='append',
            required=True,
            help=_('Specifies the list of AZs where the load balancer'
                   'can be created.')
        )
        parser.add_argument(
            '--tag',
            metavar='key=<keyname1>,value=<value1>',
            action=parseractions.MultiKeyValueAction,
            dest='tags',
            required_keys=['key', 'value'],
            help=_('List of tags. Repeat option for '
                   'multiple tags.\n'
                   'Example:\n'
                   '--tag key=mykey1,value=myvalue1')
        )
        parser.add_argument(
            '--project-id',
            metavar='<project_id>',
            help=_('Specifies the project ID.')
        )
        parser.add_argument(
            '--publicip-id',
            dest='publicip_ids',
            action='append',
            help=_('Specifies the ID of the EIP the system will automatically'
                   'assign and bind to the load balancer during load balancer'
                   'creation. Currently, only the first EIP will be bound to'
                   'the load balancer although multiple EIP IDs can be set')
        )
        parser.add_argument(
            '--ip-version-publicip',
            metavar='<ip_version_publicip>',
            type=int,
            help=_('Specifies the IP address version for public ip.'
                   'Can only be 4 (IPv4). 4 by default.')
        )
        parser.add_argument(
            '--network-type',
            metavar='<network_type>',
            choices=['5_bgp', '5_mailbgp'],
            help=_('Specifies the IP address version for public ip.'
                   'Mandatory for public ip.')
        )
        parser.add_argument(
            '--publicip-description',
            metavar='<publicip_description>',
            help=_('Provides supplementary information about the IPv4 EIP.')
        )
        parser.add_argument(
            '--bandwidth',
            metavar='name=<name>,id=<id>,size=<size>,'
                    'charge_mode=<charge_mode>,share_type=<share_type>,'
                    'billing_info=<billing_info>',
            action=parseractions.MultiKeyValueAction,
            optional_keys=['name', 'size', 'charge_mode', 'billing_info',
                           'share_type', 'billing_info', 'id'],
            help=_('Provides supplementary information about the bandwidth'
                   'for public ip. Mandatory for public ip.')
        )
        parser.add_argument(
            '--network-id',
            metavar='network_id',
            dest='elb_virsubnet_ids',
            action='append',
            help=_('ID of the subnet on the downstream plane.'
                   'The subnets must be in the VPC where the load balancer'
                   'works.'
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--ip-target-enable',
            dest='ip_target_enable',
            action='store_true',
            help=_('Specifies whether to enable IP as a Backend Server.')
        )
        parser.add_argument(
            '--deletion-protection-enable',
            dest='deletion_protection_enable',
            action='store_true',
            help=_('Specifies whether to enable deletion protection for'
                   'the load balancer.')
        )
        return parser

    def take_action(self, parsed_args):
        attrs = {}

        attrs['availability_zone_list'] = \
            parsed_args.availability_zone_list
        attrs['elb_virsubnet_ids'] = parsed_args.elb_virsubnet_ids

        args_list = ['name', 'description', 'vip_address',
                     'vip_subnet_cidr_id', 'provider',
                     'l4_flavor_id', 'l7_flavor_id',
                     'vpc_id', 'availability_zone_list', 'tags',
                     'project_id', 'publicip_ids', 'elb_virsubnet_ids',
                     'ip_target_enable', 'deletion_protection_enable']

        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val is not None:
                attrs[arg] = val

        if parsed_args.ip_target_enable is not None:
            attrs['ip_target_enable'] = parsed_args.ip_target_enable
        if parsed_args.deletion_protection_enable is not None:
            attrs['deletion_protection_enable'] =\
                parsed_args.deletion_protection_enable

        if (parsed_args.network_type or parsed_args.publicip_billing_info
                or parsed_args.ip_version or parsed_args.bandwidth
                or parsed_args.publicip_description):
            attrs['publicip'] = {}
            if parsed_args.bandwidth:
                attrs['publicip']['bandwidth'] = parsed_args.bandwidth[0]
            else:
                attrs['publicip']['bandwidth'] = {}
            if parsed_args.ip_version_publicip:
                attrs['publicip']['ip_version'] =\
                    parsed_args.ip_version_publicip
            if parsed_args.network_type:
                attrs['publicip']['network_type'] = parsed_args.network_type
            if parsed_args.publicip_description:
                attrs['publicip']['description'] \
                    = parsed_args.publicip_description

        client = self.app.client_manager.vlb
        obj = client.create_load_balancer(**attrs)

        data = utils.get_dict_properties(
            _flatten_loadbalancer(obj), self.columns)

        if obj.tags:
            data, self.columns = _add_tags_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.eips:
            data, self.columns = _add_eips_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.floating_ips:
            data, self.columns = _add_publicips_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.listeners:
            data, self.columns = _add_listeners_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.pools:
            data, self.columns = _add_pools_to_load_balancer_obj(
                obj, data, self.columns)
        return self.columns, data


class UpdateLoadBalancer(command.ShowOne):
    _description = _('Update Load balancer')
    columns = (
        'ID',
        'description',
        'provisioning_status',
        'provider',
        'operating_status',
        'ip_address',
        'subnet_id',
        'name',
        'project_id',
        'port_id',
        'created_at',
        'updated_at',
        'guaranteed',
        'vpc_id',
        'availability_zone_list',
        'l4_flavor_id',
        'l7_flavor_id',
        'network_ids'
    )

    def get_parser(self, prog_name):
        parser = super(UpdateLoadBalancer, self).get_parser(prog_name)
        parser.add_argument(
            'loadbalancer',
            metavar='<loadbalancer>',
            help=_('ID or name of the load balancer.')
        )
        parser.add_argument(
            '--name',
            help=_('New name of the load balancer.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Provides supplementary information'
                   'about the load balancer.')
        )
        parser.add_argument(
            '--subnet-id',
            metavar='<subnet_id>',
            dest='vip_subnet_cidr_id',
            help=_('Specifies the ID of the IPv4 subnet where'
                   'the load balancer works. The IPv4 subnet can be updated'
                   'using vip_subnet_cidr_id, and the private IPv4 address'
                   'of the load balancer will be changed accordingly.'
                   'If vip_address is also specified, the IP address specified'
                   'by it must be in the subnet specified by'
                   'vip_subnet_cidr_id and will be used as the private'
                   'IPv4 address of the load balancer. The IPv4 subnet'
                   'must be in the VPC'
                   'specified by vpc_id. Enter null if the private IPv4'
                   'address is unbound from the load balancer.')
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip_address>',
            dest='vip_address',
            help=_('Specifies the virtual IP address'
                   'bound to the load balancer. The IP address must be from'
                   'the IPv4 subnet of the VPC where the load balancer works'
                   'and IP address should not be occupied by other services.'
                   'The IP address specified by this parameter must be in the'
                   'subnet specified by vip_subnet_cidr_id and will be used'
                   'as the private IPv4 address of the load balancer.')
        )
        parser.add_argument(
            '--l4-flavor-id',
            metavar='<l4_flavor_id>',
            help=_('Specifies the ID of the Layer-4 flavor.'
                   'The value cannot be changed from null to a specific value,'
                   'or the other way around. If you need to change the flavor,'
                   'you must select a larger one.')
        )
        parser.add_argument(
            '--l7-flavor-id',
            metavar='<l7_flavor_id>',
            help=_('Specifies the ID of the Layer-7 flavor.'
                   'The value cannot be changed from null to a specific value,'
                   'or the other way around. If you need to change the flavor,'
                   'you must select a larger one.')
        )
        parser.add_argument(
            '--ip-target-enable',
            dest='ip_target_enable',
            action='store_true',
            help=_('Specifies whether to enable IP as a Backend Server.'
                   'The value can only be updated to true.')
        )
        parser.add_argument(
            '--network-id',
            metavar='network_id',
            dest='elb_virsubnet_ids',
            action='append',
            help=_('ID of the subnet on the downstream plane.'
                   'The subnets must be in the VPC where the load balancer'
                   'works.'
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--deletion-protection-enable',
            dest='deletion_protection_enable',
            type=bool,
            help=_('Specifies whether to enable deletion protection for'
                   'the load balancer.')
        )
        return parser

    def take_action(self, parsed_args):
        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.vip_subnet_cidr_id:
            attrs['vip_subnet_cidr_id'] = parsed_args.vip_subnet_cidr_id
        if parsed_args.vip_address:
            attrs['vip_address'] = parsed_args.vip_address
        if parsed_args.l4_flavor_id:
            attrs['l4_flavor_id'] = parsed_args.l4_flavor_id
        if parsed_args.l7_flavor_id:
            attrs['l7_flavor_id'] = parsed_args.l7_flavor_id
        if parsed_args.ip_target_enable:
            attrs['ip_target_enable'] = parsed_args.ip_target_enable
        if parsed_args.elb_virsubnet_ids:
            attrs['elb_virsubnet_ids'] = parsed_args.elb_virsubnet_ids
        if parsed_args.deletion_protection_enable is not None:
            attrs['deletion_protection_enable'] = \
                parsed_args.deletion_protection_enable
        client = self.app.client_manager.vlb
        loadbalancer = client.find_load_balancer(
            name_or_id=parsed_args.loadbalancer,
            ignore_missing=False
        )

        if attrs:
            obj = client.update_load_balancer(
                loadbalancer=loadbalancer.id, **attrs)
        else:
            obj = loadbalancer

        data = utils.get_dict_properties(
            _flatten_loadbalancer(obj), self.columns)

        if obj.tags:
            data, self.columns = _add_tags_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.eips:
            data, self.columns = _add_eips_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.floating_ips:
            data, self.columns = _add_publicips_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.listeners:
            data, self.columns = _add_listeners_to_load_balancer_obj(
                obj, data, self.columns)
        if obj.pools:
            data, self.columns = _add_pools_to_load_balancer_obj(
                obj, data, self.columns)

        return self.columns, data


class DeleteLoadBalancer(command.Command):
    _description = _('Delete load balancer')

    def get_parser(self, prog_name):
        parser = super(DeleteLoadBalancer, self).get_parser(prog_name)
        parser.add_argument(
            'loadbalancer',
            help=_('ID or name of the load balancer')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cbr

        loadbalancer = client.find_load_balancer(
            name_or_id=parsed_args.loadbalancer,
            ignore_missing=False
        )

        self.app.client_manager.vlb.delete_load_balancer(
            load_balancer=loadbalancer.id,
            ignore_missing=False)
