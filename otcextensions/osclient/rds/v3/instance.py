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
            '--subnet-id',
            dest='subnet_id',
            metavar='<subnet_id>',
            type=str,
            help=_('Indicates the Subnet ID of DB Instance.'))
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
            'name', 'id', 'router_id', 'subnet_id', 'offset', 'limit'
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
            'flavor_ref',
            metavar='<flavor_ref>',
            help=_("Flavor spec_code")
        )
        disk_group = parser.add_argument_group('Disk data')
        disk_group.add_argument(
            '--size',
            metavar='<size>',
            type=int,
            required=True,
            help=_("Size of the instance disk volume in GB. ")
        )
        disk_group.add_argument(
            '--volume-type',
            metavar='{' + ','.join(DISK_TYPE_CHOICES) + '}',
            type=lambda s: s.upper(),
            required=True,
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
            required=True,
            help=_("Name of the datastore (type).")
        )
        ds_group.add_argument(
            '--datastore-version',
            required=True,
            metavar='<datastore_version>',
            help=_("Datastore version.")
        )
        parser.add_argument(
            '--configuration',
            dest='configuration_id',
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
            help=_('ID of a Router the DB should be connected to')
        )
        new_instance_group.add_argument(
            '--subnet-id',
            metavar='<subnet_id>',
            help=_('ID of a subnet the DB should be connected to.')
        )
        new_instance_group.add_argument(
            '--security-group-id',
            dest='security_group_id',
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
        if parsed_args.datastore_type:
            datastore = {
                'type': parsed_args.datastore_type,
                'version': parsed_args.datastore_version
            }
            attrs['datastore'] = datastore
        if parsed_args.ha_mode:
            ha = {'mode': 'ha', 'replication_mode': parsed_args.ha_mode}
            attrs['ha'] = ha
        if parsed_args.charge_mode:
            attrs['charge_info'] = {'charge_mode': parsed_args.charge_mode}

        new_instance_required = [
            parsed_args.router_id,
            parsed_args.subnet_id,
            parsed_args.security_group_id,
            parsed_args.password
        ]

        if parsed_args.replica_of:
            # Create replica
            if (parsed_args.password or parsed_args.port
                    or parsed_args.router_id or parsed_args.subnet_id
                    or parsed_args.subnet_id):
                raise exceptions.CommandError(
                    _('Setting password/port/router/subnet/sg is not '
                      'supported when creating replica')
                )
            attrs['replica_of_id'] = \
                client.find_instance(parsed_args.replica_of,
                                     ignore_missing=False).id
        elif parsed_args.from_instance:
            source = client.find_instance(parsed_args.from_instance,
                                          ignore_missing=False)
            if parsed_args.backup:
                # Create from backup
                backup = client.find_backup(
                    name_or_id=parsed_args.backup,
                    instance=source,
                    ignore_missing=False)
                attrs['restore_point'] = {
                    'type': 'backup',
                    'backup_id': backup.id,
                    'instance_id': backup.instance_id
                }
            elif parsed_args.restore_time:
                attrs['restore_point'] = {
                    'type': 'timestamp',
                    'restore_time': parsed_args.restore_time,
                    'instance_id': source.id
                }
        elif parsed_args.backup or parsed_args.restore_time:
            raise exceptions.CommandError(
                _('`--from-instance` is required when restoring from '
                  'backup or using PITR.')
            )
        elif not all(new_instance_required):
            raise exceptions.CommandError(
                _('`--router-id`, `--subnet-id`, `--security-group-id`, '
                  '`--password` parameters are required when creating '
                  'new primary instance.')
            )

        flavors = list(client.flavors(
            datastore_name=parsed_args.datastore_type,
            version_name=parsed_args.datastore_version)
        )
        flavor = None
        for f in flavors:
            if f.name == parsed_args.flavor_ref:
                flavor = f
        if not flavor:
            raise exceptions.CommandError(
                _(
                    'Flavor {flavor} can not be found'.format(
                        flavor=parsed_args.flavor_ref)
                )
            )
        if flavor.instance_mode == 'ha' and not parsed_args.ha_mode:
            raise exceptions.CommandError(
                _('`--ha-mode` is required when using HA enabled flavor')
            )
        if flavor.instance_mode != 'ha' and parsed_args.ha_mode:
            raise exceptions.CommandError(
                _('`ha` enabled flavor must be '
                  'chosen when setting ha_mode')
            )
        if flavor.instance_mode != 'replica' and parsed_args.replica_of:
            raise exceptions.CommandError(
                _('`replica` enabled flavor must be '
                  'chosen when creating replica')
            )
        if parsed_args.ha_mode:
            if ',' not in parsed_args.availability_zone:
                raise exceptions.CommandError(
                    _('List of availability zones must be used when '
                      'creating ha instance')
                )
        if parsed_args.ha_mode:
            mode = parsed_args.ha_mode
            if (parsed_args.datastore_type.lower() == 'postgresql'
                    and mode not in ['async', 'sync']):
                raise exceptions.CommandError(
                    _('`async` or `sync` ha_mode can be used for '
                      'PostgreSQL isntance')
                )
            elif (parsed_args.datastore_type.lower() == 'mysql'
                    and mode not in ['async', 'semisync']):
                raise exceptions.CommandError(
                    _('`async` or `semisync` ha_mode can be used for '
                      'MySQL isntance')
                )
            elif (parsed_args.datastore_type.lower() == 'sqlserver'
                    and mode not in ['sync']):
                raise exceptions.CommandError(
                    _('Only `sync` ha_mode can be used for '
                      'SQLServer isntance')
                )
        if parsed_args.wait_interval and not parsed_args.wait:
            raise exceptions.CommandError(
                _('`--wait-interval` is only valid with `--wait`')
            )

        obj = client.create_instance(**attrs)

        if obj.job_id and parsed_args.wait:
            wait_args = {}
            if parsed_args.wait_interval:
                wait_args['interval'] = parsed_args.wait_interval

            client.wait_for_job(obj.job_id, **wait_args)
            obj = client.get_instance(obj.id)

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
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--backup',
            metavar='<backup>',
            default=None,
            type=str,
            help=_('ID or name of the backup.')
        )
        group.add_argument(
            '--restore_time',
            metavar='<restore_time>',
            default=None,
            type=str,
            help=_('Specifies the time point of data '
                   'restoration in the UNIX timestamp')
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

        client.restore_instance(instance=instance,
                                backup=backup,
                                restore_time=parsed_args.restore_time)


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
            if getattr(parsed_args, arg):
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
