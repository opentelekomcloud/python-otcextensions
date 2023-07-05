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
        'admin_state_up': obj.is_admin_state_up,
        'provider': obj.provider,
        'operating_status': obj.operating_status,
        'vip_address': obj.vip_address,
        'vip_subnet_cidr_id': obj.vip_subnet_id,
        'project_id': obj.project_id,
        'vip_port_id': obj.vip_port_id,
        'created_at': obj.created_at,
        'updated_at': obj.updated_at,
        'guaranteed': obj.guaranteed,
        'ipv6_vip_address': obj.ipv6_vip_address,
        'ipv6_vip_virsubnet_id': obj.ipv6_vip_subnet_id,
        'ipv6_vip_port_id': obj.ipv6_vip_port_id,
        'availability_zone_list': obj.availability_zones,
        'billing_info': obj.billing_info,
        'l4_flavor_id': obj.l4_flavor_id,
        'l4_scale_flavor_id': obj.l4_scale_flavor_id,
        'l7_flavor_id': obj.l7_flavor_id,
        'l7_scale_flavor_id': obj.l7_scale_flavor_id,
        'elb_virsubnet_ids': obj.network_ids,
        # 'elb_virsubnet_type': obj.elb_virsubnet_type,
        'ip_target_enable': obj.ip_target_enable,
        # 'frozen_scene': obj.frozen_scene,
        'pools': obj.pools
    }
    return data


def _add_eips_to_load_balancer_obj(obj, data, columns):
    """Add associated eips to column and data tuples
    """
    if obj.eips:
        data += (obj.eips.eip_id,)
        columns = columns + ('eip_id',)
        data += (obj.eips.eip_address,)
        columns = columns + ('eip_address',)
        data += (obj.eips.ip_version,)
        columns = columns + ('ip_version',)
    return data, columns


def _add_publicips_to_load_balancer_obj(obj, data, columns):
    """Add associated public ips to column and data tuples
    """
    if obj.floating_ips:
        data += (obj.floating_ips.publicip_id,)
        columns = columns + ('publicip_id',)
        data += (obj.floating_ips.publicip_address,)
        columns = columns + ('publicip_address',)
        data += (obj.floating_ips.ip_version,)
        columns = columns + ('piblicip_ip_version',)
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
    columns = ('ID', 'Name')

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
            # dest='marker',
            metavar='<ID>',
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
            '--is-page-reverse',
            action='store_false',
            help=_('Specifies the page direction.')
        )
        parser.add_argument(
            '--description',
            help=_('Provides supplementary information about the load balancer')
        )
        parser.add_argument(
            '--provisioning-status',
            metavar='<provisioning_status>',
            action='append',
            help=_('Specifies the provisioning status of the load balancer.')
        )
        parser.add_argument(
            '--operating-status',
            metavar='<operating_status>',
            action='append',
            help=_('Specifies the operating status of the load balancer.')
        )
        parser.add_argument(
            '--is-guaranteed',
            action='store_true',
            help=_('Specifies whether the load balancer is a dedicated'
                   ' load balancer. The value can only be true.')
        )
        parser.add_argument(
            '--vpc-id',
            metavar='<vpc_id>',
            action='append',
            help=_('Specifies the ID of the VPC where the load balancer works.')
        )
        parser.add_argument(
            '--vip-port-id',
            metavar='<vip_port_id>',
            action='append',
            help=_('Specifies the ID of the port bound to the virtual'
                   'IP address of the load balancer.')
        )
        parser.add_argument(
            '--vip-address',
            metavar='<vip_address>',
            action='append',
            help=_('Specifies the virtual IP address bound'
                   ' to the load balancer.')
        )
        parser.add_argument(
            '--vip-subnet-cidr-id',
            metavar='<vip_subnet_cidr_id>',
            action='append',
            help=_('Specifies the ID of the subnet where the'
                   ' load balancer works.')
        )
        parser.add_argument(
            '--l4-flavor-id',
            metavar='<l4_flavor_id>',
            action='append',
            help=_('Specifies the ID of the flavor at Layer 4.')
        )
        parser.add_argument(
            '--l4-scale-flavor-id',
            metavar='<l4_scale_flavor_id>',
            action='append',
            help=_('Specifies the elastic flavor that is reserved for now.')
        )
        parser.add_argument(
            '--availability-zone-list',
            metavar='<availability_zone_list>',
            action='append',
            help=_('Specifies the list of AZs where the load balancer'
                   'is created.')
        )
        parser.add_argument(
            '--eips',
            metavar='<eips>',
            action='append',
            help=_('Specifies the EIP bound to the load balancer.')
        )
        parser.add_argument(
            '--l7-flavor-id',
            metavar='<l7_flavor_id>',
            action='append',
            help=_('Specifies the ID of the flavor at Layer 7.')
        )
        parser.add_argument(
            '--l7-scale-flavor-id',
            metavar='<l7_scale_flavor_id>',
            action='append',
            help=_('Specifies the elastic flavor that is reserved for now.')
        )
        parser.add_argument(
            '--billing-info',
            metavar='<billing_info>',
            action='append',
            help=_('Provides billing information about the load balancer.')
        )
        parser.add_argument(
            '--member-device-id',
            metavar='<member_device_id>',
            action='append',
            help=_('Specifies the ID of the cloud server that serves as a backend server.')
        )
        parser.add_argument(
            '--member-address',
            metavar='<member_address>',
            action='append',
            help=_('Specifies the private IP address of the backend server. ')
        )
        parser.add_argument(
            '--publicips',
            metavar='<publicips>',
            action='append',
            help=_('Specifies the public IP address bound to the load balancer.')
        )
        parser.add_argument(
            '--ip-version',
            metavar='<ip_version>',
            action='append',
            help=_('Specifies the IP version. The value can be 4 (IPv4) or 6 (IPv6).')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.vlb

        args = {}
        if parsed_args.id:
            args['id'] = parsed_args.id
        if parsed_args.name:
            args['name'] = parsed_args.name
        if parsed_args.limit:
            args['limit'] = parsed_args.limit
        if parsed_args.is_page_reverse:
            args['page_reverse'] = parsed_args.is_page_reverse
        if parsed_args.description:
            args['description'] = parsed_args.description
        if parsed_args.provisioning_status:
            args['provisioning_status'] = parsed_args.provisioning_status
        if parsed_args.operating_status:
            args['operating_status'] = parsed_args.operating_status
        if parsed_args.is_guaranteed:
            args['guaranteed'] = parsed_args.is_guaranteed
        if parsed_args.vip_port_id:
            args['vip_port_id'] = parsed_args.vip_port_id
        if parsed_args.vip_address:
            args['vip_address'] = parsed_args.vip_address
        if parsed_args.vip_subnet_cidr_id:
            args['vip_subnet_cidr_id'] = parsed_args.vip_subnet_cidr_id
        if parsed_args.l4_flavor_id:
            args['l4_flavor_id'] = parsed_args.l4_flavor_id
        if parsed_args.l4_scale_flavor_id:
            args['l4_scale_flavor_id'] = parsed_args.l4_scale_flavor_id
        if parsed_args.availability_zone_list:
            args['availability_zone_list'] = parsed_args.availability_zone_list
        if parsed_args.eips:
            args['eips'] = parsed_args.eips
        if parsed_args.l7_flavor_id:
            args['l7_flavor_id'] = parsed_args.l7_flavor_id
        if parsed_args.l7_scale_flavor_id:
            args['l7_scale_flavor_id'] = parsed_args.l7_scale_flavor_id
        if parsed_args.billing_info:
            args['billing_info'] = parsed_args.billing_info
        if parsed_args.member_device_id:
            args['member_device_id'] = parsed_args.member_device_id
        if parsed_args.member_address:
            args['member_address'] = parsed_args.member_address
        if parsed_args.publicips:
            args['publicips'] = parsed_args.publicips
        if parsed_args.ip_version:
            args['ip_version'] = parsed_args.ip_version
        # if parsed_args.elb_virsubnet_type:
        #     args['elb_virsubnet_type'] = parsed_args.elb_virsubnet_type

        data = client.load_balancers(**args)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowLoadBalancer(command.ShowOne):
    _description = _('Shows details of a Load balancer')
    columns = (
        'id',
        'name',
        'description',
        'provisioning_status',
        'admin_state_up',
        'provider',
        'pools',
        'listeners',
        'operating_status',
        'vip_address',
        'vip_subnet_cidr_id',
        'project_id',
        'vip_port_id',
        'tags',
        'created_at',
        'updated_at',
        'guaranteed',
        'vpc_id',
        'ipv6_vip_address',
        'ipv6_vip_virsubnet_id',
        'ipv6_vip_port_id',
        'availability_zone_list',
        'billing_info',
        'l4_flavor_id',
        'l4_scale_flavor_id',
        'l7_flavor_id',
        'l7_scale_flavor_id',
        'elb_virsubnet_ids',
        'ip_target_enable',
        'ipv6_bandwidth')

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

         return self.columns, data


class CreateLoadBalancer(command.ShowOne):
    _description = _('Create Load balancer')
    columns = (
        'ID',
        'description',
        'provisioning_status',
        'admin_state_up',
        'provider',
        'pools',
        'listeners',
        'operating_status',
        'vip_address',
        'vip_subnet_cidr_id',
        'name',
        'project_id',
        'vip_port_id',
        'tags',
        'created_at',
        'updated_at',
        'guaranteed',
        'vpc_id',
        'ipv6_vip_address',
        'ipv6_vip_virsubnet_id',
        'ipv6_vip_port_id',
        'availability_zone_list',
        'enterprise_project_id',
        'billing_info',
        'l4_flavor_id',
        'l4_scale_flavor_id',
        'l7_flavor_id',
        'l7_scale_flavor_id',
        'elb_virsubnet_ids',
        'elb_virsubnet_type',
        'ip_target_enable',
        'frozen_scene',
        'ipv6_bandwidth'
    )

    def get_parser(self, prog_name):
        parser = super(CreateLoadBalancer, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the load balancer')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('User-defined Load balancer description.')
        )
        parser.add_argument(
            '--vip-address',
            metavar='<vip_address>',
            help=_('Specifies the virtual IP address'
                   ' bound to the load balancer.')
        )
        parser.add_argument(
            '--vip-subnet-cidr-id',
            metavar='<vip_subnet_cidr_id>',
            help=_('Specifies the ID of the IPv4 subnet'
                   ' where the load balancer works.')
        )
        parser.add_argument(
            '--ipv6-vip-virsubnet-id',
            metavar='<ipv6_vip_virsubnet_id>',
            type=str,
            help=_('Specifies the ID of the IPv6 subnet where'
                   ' the load balancer works.')
        )
        parser.add_argument(
            '--provider',
            type=str,
            default='vlb',
            help=_('Specifies the provider of the load balancer.'
                   'The value can only be vlb.')
        )
        parser.add_argument(
            '--l4-flavor-id',
            metavar='<l4_flavor_id>',
            help=_('Specifies the ID of the Layer-4 flavor.')
        )
        parser.add_argument(
            '--project-id',
            metavar='<project_id>',
            help=_('Specifies the project ID.')
        )
        parser.add_argument(
            '--is-guaranteed',
            action='store_false',
            help=_('Capacity, in GB.\n'
                   'Ranges from 1 to 10485760.')
        )
        parser.add_argument(
            '--vpc-id',
            metavar='<vpc_id>',
            help=_('Specifies the ID of the VPC where the load balancer works.')
        )
        parser.add_argument(
            '--availability-zone-list',
            metavar='<availability_zone_list>',
            action='append',
            required=True,
            help=_('Specifies the list of AZs where the load balancer'
                   'can be created.')
        )
        parser.add_argument(
            '--tag',
            metavar='<tag>',
            action='append',
            help=_('Tag to assign to the server in KEY=VALUE format. '
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--l7-flavor-id',
            metavar='<l7_flavor_id>',
            help=_('Specifies the ID of the Layer-7 flavor.')
        )
        parser.add_argument(
            '--ipv6-bandwidth',
            metavar='<ipv6_bandwidth>',
            help=_('Specifies the ID of the bandwidth. This parameter'
                   'is available only when you create or update'
                   ' a load balancer that has an IPv6 address bound.')
        )
        parser.add_argument(
            '--publicip-id',
            metavar='<publicip_id>',
            action='append',
            help=_('Specifies the ID of the EIP the system will automatically'
                   'assign and bind to the load balancer during load balancer'
                   ' creation. Repeat for multiple values.')
        )
        parser.add_argument(
            '--ip-version',
            metavar='<ip_version>',
            type=int,
            help=_('Specifies the IP address version for public ip')
        )
        parser.add_argument(
            '--network-type',
            metavar='<network_type>',
            choices=['5_bgp', '5_mailbgp'],
            help=_('Specifies the IP address version for public ip.'
                   'Mandatory for public ip.')
        )
        parser.add_argument(
            '--billing-info',
            metavar='<billing_info>',
            help=_('Provides billing information about the IPv4 EIP.')
        )
        parser.add_argument(
            '--public-ip-description',
            metavar='<public_ip_description>',
            help=_('Provides supplementary information about the IPv4 EIP.')
        )
        parser.add_argument(
            '--bandwidth',
            metavar='name=<name>,id=<id>,size=<size>,'
                    'charge_mode=<charge_mode>,share_type=<share_type>,'
                    'billing_info=<billing_info>',
            action=parseractions.MultiKeyValueAction,
            dest='bandwidth',
            optional_keys=['name', 'size', 'charge_mode', 'billing_info',
                           'share_type', 'billing_info', 'id'],
            help=_('Provides supplementary information about the bandwidth'
                   'for public ip. Mandatory for public ip.')
        )
        parser.add_argument(
            '--elb-virsubnet-id',
            metavar='<elb_virsubnet_id>',
            action='append',
            help=_('ID of the subnet on the downstream plane.'
                   'Repeat for multiple values.')
        )
        parser.add_argument(
            '--is-ip-target-enable',
            action='store_false',
            help=_('Specifies whether to enable cross-VPC backend.')
        )
        return parser

    def take_action(self, parsed_args):
        attrs = {}

        attrs['availability_zone_list'] = \
            parsed_args.availability_zone_list
        attrs['elb_virsubnet_ids'] = parsed_args.elb_virsubnet_id

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.vip_address:
            attrs['vip_address'] = parsed_args.vip_address
        if parsed_args.vip_subnet_cidr_id:
            attrs['vip_subnet_cidr_id'] = parsed_args.vip_subnet_cidr_id
        if parsed_args.ipv6_vip_virsubnet_id:
            attrs['ipv6_vip_virsubnet_id'] = parsed_args.ipv6_vip_virsubnet_id
        if parsed_args.provider:
            attrs['provider'] = parsed_args.provider
        if parsed_args.l4_flavor_id:
            attrs['l4_flavor_id'] = parsed_args.l4_flavor_id
        if parsed_args.is_guaranteed:
            attrs['guaranteed'] = parsed_args.is_guaranteed
        if parsed_args.project_id:
            attrs['project_id'] = parsed_args.project_id
        if parsed_args.vpc_id:
            attrs['vpc_id'] = parsed_args.vpc_id
        if parsed_args.tag:
            attrs['tag'] = parsed_args.tag
        if parsed_args.l7_flavor_id:
            attrs['l7_flavor_id'] = parsed_args.l7_flavor_id
        if parsed_args.ipv6_bandwidth:
            attrs['ipv6_bandwidth'] = parsed_args.ipv6_bandwidth
        if parsed_args.publicip_id:
            attrs['publicip_id'] = parsed_args.publicip_id
        if parsed_args.network_type:
            attrs['publicip']['bandwidth'] = parsed_args.bandwidth
            if parsed_args.ip_version:
                attrs['publicip']['ip_version'] = parsed_args.ip_version
            if parsed_args.network_type:
                attrs['publicip']['network_type'] = parsed_args.network_type
            if parsed_args.billing_info:
                attrs['publicip']['billing_info'] = parsed_args.billing_info
            if parsed_args.public_ip_description:
                attrs['publicip']['description'] = parsed_args.public_ip_description

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
        return self.columns, data


class UpdateLoadBalancer(command.ShowOne):
    _description = _('Update Load balancer')
    columns = (
        'id',
        'description',
        'provisioning_status',
        'admin_state_up',
        'provider',
        'pools',
        'listeners',
        'operating_status',
        'vip_address',
        'vip_subnet_cidr_id',
        'name',
        'project_id',
        'vip_port_id',
        'created_at',
        'updated_at',
        'guaranteed',
        'vpc_id',
        'ipv6_vip_address',
        'ipv6_vip_virsubnet_id',
        'ipv6_vip_port_id',
        'availability_zone_list',
        'billing_info',
        'l4_flavor_id',
        'l4_scale_flavor_id',
        'l7_flavor_id',
        'l7_scale_flavor_id',
        'elb_virsubnet_ids',
        'elb_virsubnet_type',
        'ip_target_enable',
        'frozen_scene',
        'ipv6_bandwidth'
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
            help=_('Name of the load balancer.')
        )
        parser.add_argument(
            '--ipv6-vip-virsubnet-id',
            metavar='ipv6_vip_virsubnet_id',
            help=_('Specifies the administrative status of the load balancer.'
                   'And the value can only be true')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Provides supplementary information'
                   ' about the load balancer.')
        )
        parser.add_argument(
            '--ipv6-vip-virsubnet-id',
            metavar='<ipv6_vip_virsubnet_id>',
            help=_('Specifies the ID of the IPv6 subnet where'
                   'the load balancer works.')
        )
        parser.add_argument(
            '--vip-subnet-cidr-id',
            metavar='<vip_subnet_cidr_id>',
            help=_('Specifies the ID of the IPv4 subnet where'
                   'the load balancer works.')
        )
        parser.add_argument(
            '--vip-address',
            metavar='<vip_address>',
            help=_('Specifies the virtual IP address'
                   'bound to the load balancer.')
        )
        parser.add_argument(
            '--l4-flavor-id',
            metavar='<l4_flavor_id>',
            help=_('Specifies the ID of the Layer-4 flavor.')
        )
        parser.add_argument(
            '--l7-flavor-id',
            metavar='<l7_flavor_id>',
            help=_('Specifies the ID of the Layer-7 flavor.')
        )
        parser.add_argument(
            '--ipv6-bandwidth',
            metavar='<ipv6_bandwidth>',
            action='append',
            help=_('Specifies the ID of the bandwidth. This parameter'
                   'is available only when you create or update'
                   'a load balancer that has an IPv6 address bound.')
        )
        return parser

    def take_action(self, parsed_args):
        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.ipv6_vip_virsubnet_id:
            attrs['ipv6_vip_virsubnet_id'] = parsed_args.ipv6_vip_virsubnet_id
        if parsed_args.vip_subnet_cidr_id:
            attrs['vip_subnet_cidr_id'] = parsed_args.vip_subnet_cidr_id
        if parsed_args.vip_address:
            attrs['vip_address'] = parsed_args.vip_address
        if parsed_args.l4_flavor_id:
            attrs['l4_flavor_id'] = parsed_args.l4_flavor_id
        if parsed_args.l7_flavor_id:
            attrs['l7_flavor_id'] = parsed_args.l7_flavor_id
        if parsed_args.ipv6_bandwidth:
            attrs['ipv6_bandwidth'] = parsed_args.ipv6_bandwidth
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

        return self.columns, data


class DeleteLoadBalancer(command.Command):
    _description = _('Delete load balancer')

    def get_parser(self, prog_name):
        parser = super(DeleteLoadBalancer, self).get_parser(prog_name)
        parser.add_argument(
            'loadbalancer',
            metavar='<vault>',
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
