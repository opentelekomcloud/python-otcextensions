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
'''Instance v1 action implementations'''
import argparse
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def set_attributes_for_print(instances):
    for instance in instances:
        if getattr(instance, 'volume', None):
            setattr(instance, 'size', instance.volume['size'])
        else:
            setattr(instance, 'size', '-')
        datastore = instance.datastore
        if datastore.get('version'):
            setattr(instance, 'datastore_version', datastore['version'])
        if datastore.get('type'):
            setattr(instance, 'datastore_type', datastore['type'])
        yield instance


def set_attributes_for_print_detail(obj):
    info = {}  # instance._info.copy()
    attr_list = [
        'id', 'name', 'datastore', 'flavor_ref', 'disk_encryption_id',
        'region', 'availability_zone', 'vpc_id', 'subnet_id',
        'security_group_id', 'port', 'backup_strategy', 'configuration_id',
        'charge_info', 'backup_strategy'
    ]
    for attr in dir(obj):
        if attr == 'datastore' and getattr(obj, attr):
            info['datastore'] = obj.datastore['type']
            info['datastore_version'] = obj.datastore['version']
        elif attr == 'volume' and getattr(obj, attr):
            info['volume_type'] = obj.volume['type']
            info['size'] = obj.volume['size']
        elif attr == 'charge_info' and getattr(obj, attr):
            info['charge_mode'] = obj.charge_info['charge_mode']
        elif attr in attr_list and getattr(obj, attr):
            info[attr] = getattr(obj, attr)
    return info


class ListDatabaseInstances(command.Lister):
    _description = _('List database instances')
    columns = [
        'ID', 'Name', 'Datastore Type', 'Datastore Version', 'Status',
        'Flavor_ref', 'Type', 'Size', 'Region'
    ]

    def get_parser(self, prog_name):
        parser = super(ListDatabaseInstances, self).get_parser(prog_name)
        parser.add_argument('--limit',
                            dest='limit',
                            metavar='<limit>',
                            type=int,
                            default=None,
                            help=_('Limit the number of results displayed'))
        parser.add_argument('--id',
                            dest='id',
                            metavar='<id>',
                            type=str,
                            default=None,
                            help=_('Specifies the DB instance ID.'))
        parser.add_argument('--name',
                            dest='name',
                            metavar='<name>',
                            type=str,
                            default=None,
                            help=_('Specifies the DB instance Name.'))
        parser.add_argument(
            '--type',
            dest='type',
            metavar='<type>',
            type=str,
            default=None,
            help=_(
                'Specifies the instance type. Values cane be single/ha/replica'
            ))
        parser.add_argument('--database',
                            dest='datastore_type',
                            metavar='<datastore_type>',
                            type=str,
                            default=None,
                            help=_(
                                'Specifies the database type. '
                                'value is MySQL, PostgreSQL, or SQLServer.'))
        parser.add_argument('--router_id',
                            dest='router_id',
                            metavar='<router_id>',
                            type=str,
                            default=None,
                            help=_('Specifies the ID of Router to which '
                                   'instance should be connected to.'))
        parser.add_argument('--subnet_id',
                            dest='subnet_id',
                            metavar='<subnet_id>',
                            type=str,
                            default=None,
                            help=_('Indicates the Subnet ID of DB Instance.'))
        parser.add_argument('--offset',
                            dest='offset',
                            metavar='<offset>',
                            type=int,
                            default=None,
                            help=_('Specifies the index position.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        args_list = [
            'name', 'id', 'router_id', 'subnet_id', 'type', 'datastore_type',
            'offset', 'limit'
        ]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        data = client.instances(**attrs)
        if data:
            data = set_attributes_for_print(data)

        return (self.columns, (utils.get_item_properties(
            s,
            self.columns,
        ) for s in data))


class ShowDatabaseInstance(command.ShowOne):
    _description = _("Show instance details.")

    def get_parser(self, prog_name):
        parser = super(ShowDatabaseInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Instance (name or ID)'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        obj = client.find_instance(parsed_args.instance)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateDatabaseInstance(command.ShowOne):

    _description = _("Creates a new database instance.")

    def get_parser(self, prog_name):
        parser = super(CreateDatabaseInstance, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_("Name of the instance."),
        )
        parser.add_argument(
            'flavor_ref',
            metavar='<flavor_ref>',
            help=_("Flavor spec_code"),
        )
        parser.add_argument(
            '--size',
            metavar='<size>',
            type=int,
            required=True,
            help=_("Size of the instance disk volume in GB. "),
        )
        parser.add_argument(
            '--volume-type',
            metavar='<volume_type>',
            type=str,
            default=None,
            choices=['COMMON', 'ULTRAHIGH'],
            help=_("Volume type. (COMMON, ULTRAHIGH)."),
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            default=None,
            help=_("The Zone hint to give to Nova."),
        )
        parser.add_argument(
            '--datastore',
            metavar='<datastore>',
            default=None,
            help=_("datastore name"),
        )
        parser.add_argument(
            '--datastore-version',
            default=None,
            metavar='<datastore_version>',
            help=_("datastore version."),
        )
        parser.add_argument(
            '--configuration',
            dest='configuration_id',
            metavar='<configuration_id>',
            default=None,
            help=_("ID of the configuration group to attach to the instance."),
        )
        parser.add_argument(
            '--disk-encryption-id',
            metavar='<disk_encryption_id>',
            default=None,
            help=_("key ID for disk encryption."),
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            default=None,
            type=int,
            help=_("Database Port"),
        )
        parser.add_argument(
            '--password',
            metavar='<password>',
            help=_("ID of the configuration group to attach to the instance."),
        )
        parser.add_argument(
            '--replica-of',
            metavar='<source_instance>',
            default=None,
            help=_("ID or name of an existing instance to replicate from."),
        )
        parser.add_argument(
            '--region',
            metavar='<region>',
            type=str,
            default=None,
            help=argparse.SUPPRESS,
        )
        parser.add_argument('--router-id',
                            metavar='<router_id>',
                            type=str,
                            help=_('ID of a Router the DB should be connected '
                                   'to'))
        parser.add_argument('--subnet-id',
                            metavar='<subnet_id>',
                            type=str,
                            help=_('ID of a subnet the DB should be connected '
                                   'to.'))
        parser.add_argument('--security-group-id',
                            dest='security_group_id',
                            metavar='<security_group_id>',
                            type=str,
                            help=_('Security group ID'))
        parser.add_argument(
            '--ha-mode',
            metavar='<ha_replication_mode>',
            type=str,
            default=None,
            help=_('replication mode for the standby DB instance'))
        parser.add_argument('--charge-mode',
                            metavar='<charge_mode>',
                            type=str,
                            default='postPaid',
                            help=_('Specifies the billing mode'))
        return parser

    def take_action(self, parsed_args):
        # raise NotImplementedError
        # Attention: not conform password result in BadRequest with no info
        client = self.app.client_manager.rds

        attrs = {}
        args_list = [
            'name', 'availability_zone', 'configuration_id', 'region',
            'router_id', 'subnet_id', 'security_group_id',
            'disk_encryption_id', 'port', 'password', 'flavor_ref'
        ]
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)
        volume = {}
        if parsed_args.size:
            volume = {"size": parsed_args.size}
            if parsed_args.volume_type:
                volume['type'] = parsed_args.volume_type
            attrs['volume'] = volume
        if parsed_args.replica_of:
            attrs['replica_of_id'] = \
                client.find_instance(parsed_args.replica_of).id
        if parsed_args.datastore:
            datastore = {
                'type': parsed_args.datastore,
                'version': parsed_args.datastore_version
            }
            attrs['datastore'] = datastore
        if parsed_args.ha_mode:
            ha = {'mode': 'ha', 'replication_mode': parsed_args.ha_mode}
            attrs['ha'] = ha
        if parsed_args.charge_mode:
            attrs['charge_info'] = {'charge_mode': parsed_args.charge_mode}
        obj = client.create_instance(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters={})
        return (display_columns, data)


class DeleteDatabaseInstance(command.Command):

    _description = _("Deletes an instance.")

    def get_parser(self, prog_name):
        parser = super(DeleteDatabaseInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID or name of the Instance'),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        instance = client.find_instance(parsed_args.instance)
        try:
            client.delete_instance(instance.id)
        except Exception as e:
            msg = (_("Failed to delete instance %(instance)s: %(e)s") % {
                'instance': parsed_args.instance,
                'e': e
            })
            raise exceptions.CommandError(msg)


class RestoreDatabaseInstance(command.Command):

    _description = _("Restores an instance from backup.")

    def get_parser(self, prog_name):
        parser = super(RestoreDatabaseInstance, self).get_parser(prog_name)
        parser.add_argument('instance',
                            metavar='<instance>',
                            type=str,
                            help=_('ID or name of the instance.'))
        parser.add_argument('--backup',
                            metavar='<backup>',
                            default=None,
                            type=str,
                            help=_('ID or name of the backup.'))
        parser.add_argument('--restore_time',
                            metavar='<restore_time>',
                            default=None,
                            type=str,
                            help=_('Specifies the time point of data '
                                   'restoration in the UNIX timestamp'))
        parser.add_argument('--target_instance',
                            metavar='<target_instance>',
                            default=None,
                            type=str,
                            help=_('ID or name of the target instance.'))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        client.restore_instance(instance=parsed_args.instance,
                                backup=parsed_args.backup,
                                restore_time=parsed_args.restore_time,
                                target_instance=parsed_args.target_instance)


class CreateDatabaseFromBackup(command.ShowOne):

    _description = _("Creates a new database instance from backup.")

    def get_parser(self, prog_name):
        parser = super(CreateDatabaseFromBackup, self).get_parser(prog_name)
        parser.add_argument('instance',
                            metavar='<instance>',
                            type=str,
                            help=_('ID or name of the instance.'))
        parser.add_argument('name',
                            metavar='<name>',
                            help=_("Name of the instance."))
        parser.add_argument('flavor_ref',
                            metavar='<flavor_ref>',
                            help=_("Flavor spec_code"))
        parser.add_argument('--size',
                            metavar='<size>',
                            type=int,
                            required=True,
                            help=_("Size of the instance disk volume in GB. "))
        parser.add_argument('--volume_type',
                            metavar='<volume_type>',
                            type=str,
                            default=None,
                            choices=['COMMON', 'ULTRAHIGH'],
                            help=_("Volume type. (COMMON, ULTRAHIGH)."))
        parser.add_argument('--availability_zone',
                            metavar='<availability_zone>',
                            default=None,
                            help=_("The Zone hint to give to Nova."))
        parser.add_argument(
            '--configuration',
            dest='configuration_id',
            metavar='<configuration_id>',
            default=None,
            help=_("ID of the configuration group to attach to the instance."))
        parser.add_argument('--disk_encryption_id',
                            metavar='<disk_encryption_id>',
                            default=None,
                            help=_("key ID for disk encryption."))
        parser.add_argument('--port',
                            metavar='<port>',
                            default=None,
                            type=int,
                            help=_("Database Port"))
        parser.add_argument(
            '--password',
            metavar='<password>',
            help=_("ID of the configuration group to attach to the instance."))
        parser.add_argument('--region',
                            metavar='<region>',
                            type=str,
                            default=None,
                            help=argparse.SUPPRESS)
        parser.add_argument('--network_id',
                            dest='vpc_id',
                            metavar='<network_id>',
                            type=str,
                            help=_('Network (VPC) ID'))
        parser.add_argument('--subnet_id',
                            metavar='<subnet_id>',
                            type=str,
                            help=_('Network (VPC) ID'))
        parser.add_argument('--security_group',
                            dest='security_group_id',
                            metavar='<security_group_id>',
                            type=str,
                            help=_('Security group ID'))
        parser.add_argument(
            '--ha_mode',
            metavar='<ha_replication_mode>',
            type=str,
            default=None,
            help=_('replication mode for the standby DB instance'))
        parser.add_argument('--backup',
                            metavar='<backup>',
                            default=None,
                            type=str,
                            help=_('ID or name of the backup.'))
        parser.add_argument('--restore_time',
                            metavar='<restore_time>',
                            default=None,
                            type=str,
                            help=_('Specifies the time point of data '
                                   'restoration in the UNIX timestamp'))
        parser.add_argument('--target_instance',
                            metavar='<target_instance>',
                            default=None,
                            type=str,
                            help=_('ID or name of the target instance.'))
        return parser

    def take_action(self, parsed_args):
        # raise NotImplementedError
        # Attention: not conform password result in BadRequest with no info
        client = self.app.client_manager.rds

        attrs = {}
        args_list = [
            'name', 'availability_zone', 'configuration_id', 'region',
            'vpc_id', 'subnet_id', 'security_group_id', 'disk_encryption_id',
            'port', 'password', 'flavor_ref'
        ]
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)
        volume = {}
        if parsed_args.size:
            volume = {"size": parsed_args.size}
            if parsed_args.volume_type:
                volume['type'] = parsed_args.volume_type
            attrs['volume'] = volume
        if parsed_args.ha_mode:
            ha = {'mode': 'ha', 'replication_mode': parsed_args.ha_mode}
            attrs['ha'] = ha
        obj = client.create_instance_from_backup(
            instance=parsed_args.instance,
            backup=parsed_args.backup,
            restore_time=parsed_args.restore_time,
            **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters={})
        return (display_columns, data)
