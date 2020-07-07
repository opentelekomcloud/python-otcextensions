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
'''Instance v1 action implementations'''
import argparse

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _


def _get_columns(item):
    column_map = {}
    hidden = ['job_id']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


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


HA_MODE_CHOICES = ['sync', 'semisync', 'async']
DISK_TYPE_CHOICES = ['common', 'ultrahigh']
HA_TYPE_CHOICES = ['ha', 'replica', 'single']
DATASTORE_TYPE_CHOICES = ['mysql', 'postgresql', 'sqlserver']


class ListDatabaseInstances(command.Lister):
    _description = _('List database instances')
    columns = (
        'ID', 'Name', 'Datastore Type', 'Datastore Version', 'Status',
        'Flavor_ref', 'Type', 'Size', 'Region'
    )

    def get_parser(self, prog_name):
        parser = super(ListDatabaseInstances, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            dest='limit',
            metavar='<limit>',
            type=int,
            help=_('Limit the number of results displayed'))
        parser.add_argument(
            '--id',
            dest='id',
            metavar='<id>',
            type=str,
            help=_('Specifies the DB instance ID.'))
        parser.add_argument(
            '--name',
            dest='name',
            metavar='<name>',
            type=str,
            help=_('Specifies the DB instance Name.'))
        parser.add_argument(
            '--type',
            dest='type',
            metavar='{' + ','.join(HA_TYPE_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=HA_TYPE_CHOICES,
            help=_(
                'Specifies the instance type. Values cane be single/ha/replica'
            ))
        parser.add_argument(
            '--datastore-type',
            metavar='{' + ','.join(DATASTORE_TYPE_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=DATASTORE_TYPE_CHOICES,
            help=_(
                'Specifies the database type. '
                'value is MySQL, PostgreSQL, or SQLServer.'))
        parser.add_argument(
            '--router-id',
            dest='router_id',
            metavar='<router_id>',
            type=str,
            help=_('Specifies the ID of Router to which '
                   'instance should be connected to.'))
        parser.add_argument(
            '--network-id',
            dest='network_id',
            metavar='<net_id>',
            type=str,
            help=_('Indicates the Neutron network ID of DB Instance.'))
        parser.add_argument(
            '--offset',
            dest='offset',
            metavar='<offset>',
            type=int,
            default=None,
            help=_('Specifies the index position.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        args_list = [
            'name', 'id', 'router_id', 'network_id', 'offset', 'limit'
        ]
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg):
                attrs[arg] = getattr(parsed_args, arg)
        if parsed_args.type:
            attrs['type'] = parsed_args.type.title()
        if parsed_args.datastore_type == 'mysql':
            attrs['datastore_type'] = 'MySQL'
        elif parsed_args.datastore_type == 'postgresql':
            attrs['datastore_type'] = 'PostgreSQL'
        elif parsed_args.datastore_type == 'sqlserver':
            attrs['datastore_type'] = 'SQLServer'
        if parsed_args.limit:
            attrs['paginated'] = False

        data = client.instances(**attrs)
        if data:
            data = set_attributes_for_print(data)

        return (self.columns, (utils.get_item_properties(
            s,
            self.columns,
        ) for s in data))


class ShowDatabaseInstance(command.ShowOne):
    _description = _("Show instance details")

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
        obj = client.find_instance(parsed_args.instance, ignore_missing=False)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class CreateDatabaseInstance(command.ShowOne):

    _description = _("Create a new database instance.")

    def get_parser(self, prog_name):
        parser = super(CreateDatabaseInstance, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_("Name of the instance.")
        )
        parser.add_argument(
            'flavor',
            metavar='<flavor>',
            help=_("Flavor spec_code")
        )
        disk_group = parser.add_argument_group('Disk data')
        disk_group.add_argument(
            '--size',
            metavar='<size>',
            dest='volume_size',
            type=int,
            required=True,
            help=_("Size of the instance disk volume in GB. ")
        )
        disk_group.add_argument(
            '--volume-type',
            metavar='{' + ','.join(DISK_TYPE_CHOICES) + '}',
            type=lambda s: s.upper(),
            required=True,
            dest='volume_type',
            choices=[s.upper() for s in DISK_TYPE_CHOICES],
            help=_("Volume type. (COMMON, ULTRAHIGH).")
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<availability_zone>',
            required=True,
            help=_("The Zone hint to give to Nova.")
        )
        parser.add_argument(
            '--region',
            metavar='<region>',
            required=True,
            help=argparse.SUPPRESS,
        )
        ds_group = parser.add_argument_group('Datasoure parameters')
        ds_group.add_argument(
            '--datastore-type',
            metavar='<datastore>',
            help=_("Name of the datastore (type).")
        )
        ds_group.add_argument(
            '--datastore-version',
            metavar='<datastore_version>',
            help=_("Datastore version.")
        )
        parser.add_argument(
            '--configuration',
            dest='configuration',
            metavar='<configuration_id>',
            default=None,
            help=_("ID of the configuration group to attach to the instance.")
        )
        parser.add_argument(
            '--disk-encryption-id',
            metavar='<disk_encryption_id>',
            default=None,
            help=_("key ID for disk encryption.")
        )
        new_instance_group = parser.add_argument_group(
            'New instance parameters',
            'Parameters to be used for the new instance creation (not when '
            'created as replica or from backup')
        new_instance_group.add_argument(
            '--port',
            metavar='<port>',
            type=int,
            help=_("Database Port")
        )
        new_instance_group.add_argument(
            '--password',
            metavar='<password>',
            help=_("ID of the configuration group to attach to the instance.")
        )
        new_instance_group.add_argument(
            '--router-id',
            metavar='<router_id>',
            dest='router',
            help=_('ID of a Router the DB should be connected to')
        )
        new_instance_group.add_argument(
            '--network-id',
            metavar='<net_id>',
            dest='network',
            help=_('ID of a Neutron network the DB should be connected to.')
        )
        new_instance_group.add_argument(
            '--security-group-id',
            dest='security_group',
            metavar='<security_group_id>',
            help=_('Security group ID')
        )
        parser.add_argument(
            '--ha-mode',
            metavar='{' + ','.join(HA_MODE_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=HA_MODE_CHOICES,
            help=_('replication mode for the standby DB instance. '
                   'This parameter is required when using `ha`flavors')
        )
        parser.add_argument(
            '--charge-mode',
            metavar='<charge_mode>',
            default='postPaid',
            help=_('Specifies the billing mode')
        )
        create_from_group = parser.add_argument_group(
            'Create FROM group',
            'Parameters to be used when creating new instance as a '
            'replica or from backup')
        create_from_group.add_argument(
            '--replica-of',
            metavar='<source_instance>',
            default=None,
            help=_("ID or name of an existing instance to replicate from.")
        )
        create_from_group.add_argument(
            '--from-instance',
            metavar='<source_instance>',
            help=_('Source instance ID or Name to create from. '
                   'It is required when recovering from backup or PITR.')
        )
        create_from_group.add_argument(
            '--backup',
            metavar='<backup>',
            help=_('Backup ID or Name to create new instance from.')
        )
        create_from_group.add_argument(
            '--backup-keepdays',
            metavar='<backup_keepday>',
            help=_('Specifies the retention days for specific backup files.')
        )
        create_from_group.add_argument(
            '--backup-timeframe',
            metavar='<HH:MM-HH:MM>',
            help=_('Specifies the backup time window. Automated backups will '
                   'be triggered during the backup time window.')
        )
        create_from_group.add_argument(
            '--restore-time',
            metavar='<time>',
            help=_('Time (UNIX timestamp in ms) to create new instance '
                   'as a PointInTime recovery.')
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for the instance to become active')
        )
        parser.add_argument(
            '--wait-interval',
            type=int,
            help=_('Interval for checking status')
        )
        return parser

    def take_action(self, parsed_args):
        # Attention: not conform password result in BadRequest with no info
        client = self.app.client_manager
        attrs = {}
        for attr in [
            'availability_zone', 'backup', 'backup_keepdays',
            'backup_timeframe', 'charge_mode', 'configuration',
            'datastore_type', 'datastore_version', 'disk_encryption_id',
            'flavor', 'from_instance', 'ha_mode', 'name', 'network',
            'password', 'port', 'region', 'replica_of', 'restore_time',
            'router', 'security_group', 'volume_size', 'volume_type', 'wait',
            'wait_interval'
        ]:
            if getattr(parsed_args, attr):
                attrs[attr] = getattr(parsed_args, attr)

        if not parsed_args.wait:
            attrs['wait'] = False

        obj = client.create_rds_instance(
            **attrs
        )

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
        parser.add_argument(
            '--wait',
            action='store_true',
            help=_('Wait for the instance to be deleted')
        )
        parser.add_argument(
            '--wait-interval',
            type=int,
            help=_('Interval for checking status')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        instance = client.find_instance(parsed_args.instance)
        try:
            response = client.delete_instance(instance.id)
            if parsed_args.wait and response.job_id:
                wait_args = {}
                if parsed_args.wait_interval:
                    wait_args['interval'] = parsed_args.wait_interval

                client.wait_for_job(response.job_id, **wait_args)
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
        parser.add_argument(
            'instance',
            metavar='<instance>',
            type=str,
            help=_('ID or name of the target instance.')
        )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--backup',
            metavar='<backup>',
            default=None,
            type=str,
            help=_('ID or name of the backup.')
        )
        group.add_argument(
            '--restore-time',
            metavar='<restore_time>',
            default=None,
            type=str,
            help=_('Specifies the time point of data '
                   'restoration in the UNIX timestamp')
        )
        parser.add_argument(
            '--wait',
            action='store_true',
            help=('Wait for the instance to become active')
        )
        parser.add_argument(
            '--wait-interval',
            type=int,
            help=_('Interval for checking status')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        instance = client.find_instance(parsed_args.instance,
                                        ignore_missing=False)
        backup = None
        if parsed_args.backup:
            backup = client.find_backup(name_or_id=parsed_args.backup,
                                        instance=instance,
                                        ignore_missing=False)

        obj = client.restore_instance(instance=instance,
                                      backup=backup,
                                      restore_time=parsed_args.restore_time)

        if obj.job_id and parsed_args.wait:
            wait_args = {}
            if parsed_args.wait_interval:
                wait_args['interval'] = parsed_args.wait_interval

            client.wait_for_job(obj.job_id, **wait_args)


class ShowBackupPolicy(command.ShowOne):
    _description = _('Show Database instance Backup Policy')

    def get_parser(self, prog_name):
        parser = super(ShowBackupPolicy, self).get_parser(prog_name)
        parser.add_argument('instance',
                            metavar='<instance>',
                            help=_('Instance ID or Name'))
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.rds

        instance = client.find_instance(parsed_args.instance,
                                        ignore_missing=False)
        obj = client.get_instance_backup_policy(instance)

        display_columns, columns = _get_columns(obj)
        data = utils.get_dict_properties(obj, columns)

        return (display_columns, data)


class SetBackupPolicy(command.Command):
    _description = _('Set Database Backup Policy')

    def get_parser(self, prog_name):
        parser = super(SetBackupPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Instance ID or Name'))
        parser.add_argument(
            '--keep-days',
            metavar='<keep_days>',
            type=int,
            required=True,
            help=_('Specifies the number of days to'
                   'retain the generated backup files.'))
        parser.add_argument(
            '--start-time',
            metavar='<start_time>',
            help=_('Specifies the backup time window.'
                   'The value must be a valid value in the'
                   '"hh:mm-HH:MM" format.'))
        parser.add_argument(
            '--period',
            metavar='<period>',
            help=_('Specifies the backup cycle'
                   'configuration. Data will be'
                   'automatically backed up on the'
                   'selected days every week.'))
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.rds
        args_list = ['keep_days', 'start_time', 'period']
        attrs = {}
        for arg in args_list:
            if getattr(parsed_args, arg) is not None:
                attrs[arg] = getattr(parsed_args, arg)

        instance = client.find_instance(parsed_args.instance,
                                        ignore_missing=False)

        client.set_instance_backup_policy(instance, **attrs)


class ShowAvailableRestoreTime(command.Lister):
    _description = _('Show Database instance recovery timeframe')

    columns = ('start_time', 'end_time')
    column_headers = ('Start time', 'End time')

    def get_parser(self, prog_name):
        parser = super(ShowAvailableRestoreTime, self).get_parser(prog_name)
        parser.add_argument('instance',
                            metavar='<instance>',
                            help=_('Instance ID or Name'))
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.rds

        instance = client.find_instance(parsed_args.instance,
                                        ignore_missing=False)
        data = client.get_instance_restore_time(instance)

        return (self.column_headers, (utils.get_dict_properties(
            s,
            self.columns,
        ) for s in data))
