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

import six

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def set_attributes_for_print(instances):
    for instance in instances:
        if getattr(instance, 'volume', None):
            setattr(instance, 'size', instance.volume['size'])
        else:
            setattr(instance, 'size', '-')
        datastore = instance.datastore
        if datastore.get('version'):
            setattr(instance, 'datastore_version',
                    datastore['version'])
        if datastore.get('type'):
            setattr(instance, 'datastore_type', datastore['type'])
        yield instance


def set_attributes_for_print_detail(obj):
    info = {}  # instance._info.copy()
    attr_list = [
        'id',
        'name',
        'datastore',
        'flavor_ref',
        'disk_encryption_id',
        'region',
        'availability_zone',
        'vpc_id',
        'subnet_id',
        'security_group_id',
        'port',
        'backup_strategy',
        'configuration_id',
        'charge_info',
        'backup_strategy']
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
    columns = ['ID', 'Name', 'Datastore Type', 'Datastore Version', 'Status',
               'Flavor_ref', 'Type', 'Size', 'Region']

    def get_parser(self, prog_name):
        parser = super(ListDatabaseInstances, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            dest='limit',
            metavar='<limit>',
            type=int,
            default=None,
            help=_('Limit the number of results displayed')
        )
        parser.add_argument(
            '--id',
            dest='id',
            metavar='<id>',
            type=str,
            default=None,
            help=_('Specifies the DB instance ID.')
        )
        parser.add_argument(
            '--name',
            dest='name',
            metavar='<name>',
            type=str,
            default=None,
            help=_('Specifies the DB instance Name.')
        )
        parser.add_argument(
            '--type',
            dest='type',
            metavar='<type>',
            type=str,
            default=None,
            help=_('Specifies the instance type. Values cane be single/ha/replica')
        )
        parser.add_argument(
            '--db_type',
            dest='datastore_type',
            metavar='<datastore_type>',
            type=str,
            default=None,
            help=_('Specifies the database type. '
                    'value is MySQL, PostgreSQL, or SQLServer.')
        )
        parser.add_argument(
            '--vpc_id',
            dest='vpc_id',
            metavar='<vpc_id>',
            type=str,
            default=None,
            help=_('Indicates the VPC ID. of DB Instance.')
        )
        parser.add_argument(
            '--subnet_id',
            dest='subnet_id',
            metavar='<subnet_id>',
            type=str,
            default=None,
            help=_('Indicates the Subnet ID of DB Instance.')
        )
        parser.add_argument(
            '--offset',
            dest='offset',
            metavar='<offset>',
            type=str,
            default=None,
            help=_('Specifies the index position.')
        )
        parser.add_argument(
            '--marker',
            dest='marker',
            metavar='<marker>',
            help=_('Begin displaying the results for IDs greater than the '
                   'specified marker. When used with --limit, set this to '
                   'the last ID displayed in the previous run. '
                   '(Not supported)')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        args_list = [
            'name',
            'id',
            'vpc_id',
            'subnet_id',
            'type',
            'datastore_type',
            'offset']
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)

        data = client.instances(**attrs)
        if data:
            data = set_attributes_for_print(data)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowDatabaseInstance(command.ShowOne):
    _description = _("Show instance details")

    columns = [
        'id',
        'name',
        'datastore',
        'datastore_version',
        'flavor Ref',
        'Volume Type',
        'Size',
        'disk_encryption_id',
        'region',
        'availability_zone',
        'vpc_id',
        'subnet_id',
        'security_group_id',
        'port',
        'backup_strategy',
        'configuration_id',
        'charge mode']

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
        data = utils.get_item_properties(obj, columns, formatters={})
        return (display_columns, data)


class CreateDatabaseInstance(command.ShowOne):

    _description = _("Creates a new database instance.")

    columns = [
        'id',
        'name',
        'datastore',
        'datastore_version',
        'flavor Id',
        'Volume Type',
        'Size',
        'disk_encryption_id',
        'region',
        'availability_zone',
        'vpc_id',
        'subnet_id',
        'security_group_id',
        'port',
        'backup_strategy',
        'configuration_id',
        'charge mode']

    def get_parser(self, prog_name):
        parser = super(CreateDatabaseInstance, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_("Name of the instance."),
        )
        parser.add_argument(
            '--flavor',
            dest='flavor_ref',
            metavar='<flavor_ref>',
            help=_("flavor spec_code."),
        )
        parser.add_argument(
            '--size',
            metavar='<size>',
            type=int,
            required=True,
            help=_("Size of the instance disk volume in GB. "),
        )
        parser.add_argument(
            '--volume_type',
            metavar='<volume_type>',
            type=str,
            default=None,
            choices=['COMMON', 'ULTRAHIGH'],
            help=_("Volume type. (COMMON, ULTRAHIGH)."),
        )
        parser.add_argument(
            '--availability_zone',
            metavar='<availability_zone>',
            help=_("The Zone hint to give to Nova."),
        )
        parser.add_argument(
            '--datastore',
            metavar='<datastore>',
            help=_("datastore name"),
        )
        parser.add_argument(
            '--datastore_version',
            metavar='<datastore_version>',
            help=_("datastore version."),
        )
        parser.add_argument(
            '--configuration_id',
            metavar='<configuration_id>',
            default=None,
            help=_("ID of the configuration group to attach to the instance."),
        )
        parser.add_argument(
            '--disk_encryption_id',
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
            '--replica_of',
            metavar='<source_instance>',
            default=None,
            help=_("ID or name of an existing instance to replicate from."),
        )
        parser.add_argument(
            '--region',
            metavar='<region>',
            type=str,
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            '--vpc_id',
            dest='vpc_id',
            metavar='<vpc_id>',
            type=str,
            # required=True,
            help=_('Network (VPC) ID')
        )
        parser.add_argument(
            '--subnet_id',
            metavar='<subnet_id>',
            type=str,
            # required=True,
            help=_('Network (VPC) ID')
        )
        parser.add_argument(
            '--security_group',
            dest='security_group_id',
            metavar='<security_group_id>',
            type=str,
            # required=True,
            help=_('Security group ID')
        )
        parser.add_argument(
            '--ha_replication_mode',
            metavar='<ha_replication_mode>',
            type=str,
            help=_('replication mode for the standby DB instance')
        )
        parser.add_argument(
            '--charge_mode',
            metavar='<charge_mode>',
            type=str,
            default='postPaid',
            help=_('Specifies the billing mode')
        )
        return parser

    def take_action(self, parsed_args):
        # raise NotImplementedError
        # Attention: not conform password result in BadRequest with no info
        client = self.app.client_manager.rds

        attrs = {}
        args_list = ['name', 'availability_zone', 'configuration_id',
                     'region', 'vpc_id', 'subnet_id', 'security_group_id',
                     'disk_encryption_id', 'port', 'password', 'flavor_ref']
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
            attrs['replica_of'] = client.find_instance(parsed_args.replica_of)
        if parsed_args.datastore:
            datastore = {
                'type': parsed_args.datastore,
                'version': parsed_args.datastore_version
            }
            attrs['datastore'] = datastore
        if parsed_args.ha_replication_mode:
            ha = {
                'mode': 'ha',
                'replication_mode': parsed_args.ha_replication_mode
            }
            attrs['ha'] = ha
        if parsed_args.charge_mode:
            attrs['charge_info'] = {
                'charge_mode': parsed_args.charge_mode
            }
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
            msg = (_("Failed to delete instance %(instance)s: %(e)s")
                   % {'instance': parsed_args.instance, 'e': e})
            raise exceptions.CommandError(msg)


class ForceDeleteDatabaseInstance(command.Command):

    _description = _("Force delete an instance.")

    def get_parser(self, prog_name):
        parser = (super(ForceDeleteDatabaseInstance, self)
                  .get_parser(prog_name))
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID or name of the instance'),
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        # db_instances = self.app.client_manager.database.instances
        # instance = osc_utils.find_resource(db_instances,
        #                                    parsed_args.instance)
        # db_instances.reset_status(instance)
        # try:
        #     db_instances.delete(instance)
        # except Exception as e:
        #     msg = (_("Failed to delete instance %(instance)s: %(e)s")
        #            % {'instance': parsed_args.instance, 'e': e})
        #     raise exceptions.CommandError(msg)


class RestartDatabaseInstance(command.Command):

    _description = _("Restarts an instance.")

    def get_parser(self, prog_name):
        parser = super(RestartDatabaseInstance, self).get_parser(
            prog_name
        )
        parser.add_argument(
            'instance',
            metavar='<instance>',
            type=str,
            help=_('ID or name of the instance.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        client.restart_instance(parsed_args.instance)


class RestoreDatabaseInstance(command.Command):

    _description = _("Restores an instance from backup.")

    def get_parser(self, prog_name):
        parser = super(RestoreDatabaseInstance, self).get_parser(
            prog_name
        )
        parser.add_argument(
            'instance',
            metavar='<instance>',
            type=str,
            help=_('ID or name of the instance.')
        )
        parser.add_argument(
            '--backup',
            metavar='<backup>',
            type=str,
            help=_('ID or name of the backup.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        client.restore_instance(
            instance=parsed_args.instance,
            backup=parsed_args.backup)


class UpdateDatabaseInstance(command.Command):

    _description = _("Updates an instance: Edits name, "
                     "configuration, or replica source.")

    def get_parser(self, prog_name):
        parser = super(UpdateDatabaseInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            type=str,
            help=_('ID or name of the instance.'),
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            type=str,
            default=None,
            help=_('ID or name of the instance.'),
        )
        parser.add_argument(
            '--configuration',
            metavar='<configuration>',
            type=str,
            default=None,
            help=_('ID of the configuration reference to attach.'),
        )
        parser.add_argument(
            '--detach_replica_source',
            '--detach-replica-source',
            dest='detach_replica_source',
            action="store_true",
            default=False,
            help=_('Detach the replica instance from its replication source. '
                   '--detach-replica-source may be deprecated in the future '
                   'in favor of just --detach_replica_source'),
        )
        parser.add_argument(
            '--remove_configuration',
            dest='remove_configuration',
            action="store_true",
            default=False,
            help=_('Drops the current configuration reference.'),
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        # db_instances = self.app.client_manager.database.instances
        # instance = osc_utils.find_resource(db_instances,
        #                                    parsed_args.instance)
        # db_instances.edit(instance, parsed_args.configuration,
        #                   parsed_args.name,
        #                   parsed_args.detach_replica_source,
        #                   parsed_args.remove_configuration)
