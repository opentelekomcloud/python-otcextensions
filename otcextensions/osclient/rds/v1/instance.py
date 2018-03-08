#   Licensed under the Apache License, Version 2.0 (the 'License'); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''Instance v1 action implementations'''

import logging

import argparse

# import json
import six

# from osc_lib.cli import parseractions
from osc_lib.command import command
# from osc_lib.cli import parseractions
from osc_lib import exceptions
from osc_lib import utils

from otcextensions.osclient.rds import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


# def _get_columns(item):
#     column_map = {
#         'flavor.id': 'flavor_id',
#         'tenant_id': 'project_id',
#     }
#     return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def set_attributes_for_print(instances):
    for instance in instances:
        setattr(instance, 'flavor_id', instance.flavor['id'])
        if getattr(instance, 'volume', None):
            setattr(instance, 'size', instance.volume['size'])
        else:
            setattr(instance, 'size', '-')
        if getattr(instance, 'datastore', None):
            if instance.datastore.get('version'):
                setattr(instance, 'datastore_version',
                        instance.datastore['version'])
            if instance.datastore.get('type'):
                setattr(instance, 'datastore_type', instance.datastore['type'])
        yield instance


def set_attributes_for_print_detail(instance):
    info = {}  # instance._info.copy()
    info['flavor'] = instance.flavor['id']
    if getattr(instance, 'volume', None):
        info['volume'] = instance.volume['size']
        if 'used' in instance.volume:
            info['volume_used'] = instance.volume['used']
    if getattr(instance, 'ip', None):
        info['ip'] = ', '.join(instance.ip)
    if getattr(instance, 'datastore', None):
        info['datastore'] = instance.datastore['type']
        info['datastore_version'] = instance.datastore['version']
    if getattr(instance, 'configuration', None):
        info['configuration'] = instance.configuration['id']
    if getattr(instance, 'replica_of', None):
        info['replica_of'] = instance.replica_of['id']
    if getattr(instance, 'replicas', None):
        replicas = [replica['id'] for replica in instance.replicas]
        info['replicas'] = ', '.join(replicas)
    if getattr(instance, 'networks', None):
        info['networks'] = instance.networks['name']
        info['networks_id'] = instance.networks['id']
    if getattr(instance, 'fault', None):
        info.pop('fault', None)
        info['fault'] = instance.fault['message']
        info['fault_date'] = instance.fault['created']
        if 'details' in instance.fault and instance.fault['details']:
            info['fault_details'] = instance.fault['details']
    info.pop('links', None)
    return info


class ListDatabaseInstances(command.Lister):
    _description = _('List database instances')
    columns = ['ID', 'Name', 'Datastore Type', 'Datastore Version', 'Status',
               'Flavor ID', 'Size', 'Region']

    def get_parser(self, prog_name):
        parser = super(ListDatabaseInstances, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            dest='limit',
            metavar='<limit>',
            type=int,
            default=None,
            help=_('Limit the number of results displayed. (Not supported)')
        )
        parser.add_argument(
            '--marker',
            dest='marker',
            metavar='<ID>',
            help=_('Begin displaying the results for IDs greater than the '
                   'specified marker. When used with --limit, set this to '
                   'the last ID displayed in the previous run. '
                   '(Not supported)')
        )
        parser.add_argument(
            '--include_clustered', '--include-clustered',
            dest='include_clustered',
            action='store_true',
            default=False,
            help=_('Include instances that are part of a cluster '
                   '(default %(default)s).  --include-clustered may be '
                   'deprecated in the future, retaining just '
                   '--include_clustered.'
                   '(Not supported)')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.instances()

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

        # display_columns, columns = _get_columns(obj)
        # data = utils.get_item_properties(obj, columns, formatters={})
        #
        # return (display_columns, data)

        #
        # print(instance)
        instance = set_attributes_for_print_detail(obj)
        return zip(*sorted(six.iteritems(instance)))


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
            'flavor',
            metavar='<flavor>',
            help=_("A flavor ID or name."),
        )
        parser.add_argument(
            '--size',
            metavar='<size>',
            type=int,
            required=True,
            help=_("Size of the instance disk volume in GB. "
                   "Required when volume support is enabled."),
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
            '--databases',
            metavar='<database>',
            nargs="+",
            default=[],
            help=_("Optional list of databases. Not Supported"),
        )
        parser.add_argument(
            '--users',
            metavar='<user:password>',
            nargs="+",
            required=True,
            help=_("list of users."),
        )
        parser.add_argument(
            '--backup',
            metavar='<backup>',
            default=None,
            help=_("A backup name or ID."),
        )
        parser.add_argument(
            '--availability_zone',
            metavar='<availability_zone>',
            default=None,
            help=_("The Zone hint to give to Nova."),
        )
        parser.add_argument(
            '--datastore',
            metavar='<datastore>',
            default=None,
            help=_("A datastore name or ID."),
        )
        parser.add_argument(
            '--datastore_version',
            metavar='<datastore_version>',
            default=None,
            help=_("A datastore version name or ID."),
        )
        parser.add_argument(
            '--nic',
            metavar='<net-id=<net-uuid>,v4-fixed-ip=<ip-addr>,'
                    'port-id=<port-uuid>>',
            action='append',
            dest='nics',
            default=[],
            help=_("Create a NIC on the instance. Specify option multiple "
                   "times to create multiple NICs. net-id: attach NIC to "
                   "network with this ID (either port-id or net-id must be "
                   "specified), v4-fixed-ip: IPv4 fixed address for NIC "
                   "(optional), port-id: attach NIC to port with this ID "
                   "(either port-id or net-id must be specified)."),
        )
        parser.add_argument(
            '--configuration',
            metavar='<configuration>',
            default=None,
            help=_("ID of the configuration group to attach to the instance."),
        )
        parser.add_argument(
            '--replica_of',
            metavar='<source_instance>',
            default=None,
            help=_("ID or name of an existing instance to replicate from."),
        )
        parser.add_argument(
            '--replica_count',
            metavar='<count>',
            type=int,
            default=None,
            help=_("Number of replicas to create (defaults to 1 if "
                   "replica_of specified)."
                   "(None or 1 is allowed)"),
        )
        parser.add_argument(
            '--module',
            metavar='<module>',
            type=str,
            dest='modules',
            action='append',
            default=[],
            help=_("ID or name of the module to apply.  Specify multiple "
                   "times to apply multiple modules."
                   "(Not supported)"),
        )
        parser.add_argument(
            '--locality',
            metavar='<policy>',
            default=None,
            choices=['affinity', 'anti-affinity'],
            help=_("Locality policy to use when creating replicas. Choose "
                   "one of %(choices)s."
                   "(Not supported)"),
        )
        parser.add_argument(
            '--region',
            metavar='<region>',
            type=str,
            default=None,
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            '--router',
            metavar='<router_id>',
            type=str,
            # required=True,
            help=_('Router (VPC) ID')
        )
        parser.add_argument(
            '--subnet_id',
            metavar='<subnet_id>',
            type=str,
            # required=True,
            help=_('Subnet ID')
        )
        parser.add_argument(
            '--security_group',
            metavar='<security_group>',
            type=str,
            # required=True,
            help=_('Security group ID')
        )
        return parser

    def take_action(self, parsed_args):
        # raise NotImplementedError
        # Attention: not conform password result in BadRequest with no info
        client = self.app.client_manager.rds

        attrs = {}
        attrs['flavorRef'] = client.find_flavor(parsed_args.flavor).str_id
        volume = None
        if parsed_args.size is not None and parsed_args.size <= 0:
            raise exceptions.ValidationError(
                _("Volume size '%s' must be an integer and greater than 0.")
                % parsed_args.size)
        elif parsed_args.size:
            volume = {"size": parsed_args.size}
            if parsed_args.volume_type:
                volume['type'] = parsed_args.volume_type
            attrs['volume'] = volume
        # restore_point = None
        if parsed_args.backup:
            pass
            # TODO(agoncharov)
        #     restore_point = {"backupRef": osc_utils.find_resource(
        #         database.backups, parsed_args.backup).id}
        replica_of = None
        replica_count = parsed_args.replica_count
        if parsed_args.replica_of:
            pass
            # TODO(agoncharov)
            attrs['replica_of'] = client.find_instance(parsed_args.replica_of)
            attrs['replica_count'] = replica_count or 1
        # locality = None
        # if parsed_args.locality:
        #     locality = parsed_args.locality
        #     if replica_of:
        #         raise exceptions.ValidationError(
        #             _('Cannot specify locality when adding replicas '
        #               'to existing master.'))
        # databases = [{'name': value} for value in parsed_args.databases]
        # users = [{'name': n, 'password': p, 'databases': databases} for (n, p)
        attrs['users'] = [{'name': n, 'password': p} for (n, p) in
            [z.split(':')[:2] for z in parsed_args.users]]
        # nics = []
        # for nic_str in parsed_args.nics:
        #     nic_info = dict([(k, v) for (k, v) in [z.split("=", 1)[:2] for z in
        #                                            nic_str.split(",")]])
        #     # need one or the other, not both, not none (!= ~ XOR)
        #     if not (bool(nic_info.get('net-id')) != bool(
        #             nic_info.get('port-id'))):
        #         raise exceptions.\
        #             ValidationError(_("Invalid NIC argument: %s. Must specify "
        #                               "either net-id or port-id but not both. "
        #                               "Please refer to help.")
        #                             % (_("nic='%s'") % nic_str))
        #     nics.append(nic_info)
        # modules = []
        # for module in parsed_args.modules:
        #     modules.append(osc_utils.find_resource(database.modules,
        #                                            module).id)

        # instance = db_instances.create(parsed_args.name,
        #                                flavor_id,
        #                                volume=volume,
        #                                databases=databases,
        #                                users=users,
        #                                restorePoint=restore_point,
        #                                availability_zone=(parsed_args.
        #                                                   availability_zone),
        #                                datastore=parsed_args.datastore,
        #                                datastore_version=(parsed_args.
        #                                                   datastore_version),
        #                                nics=nics,
        #                                configuration=parsed_args.configuration,
        #                                replica_of=replica_of,
        #                                replica_count=replica_count,
        #                                modules=modules,
        #                                locality=locality,
        #                                region_name=parsed_args.region)

        datastore = {
            'type': parsed_args.datastore,
            'version': parsed_args.datastore_version
        }
        attrs['datastore'] = datastore
        attrs['name'] = parsed_args.name
        if parsed_args.availability_zone:
            attrs['availability_zone'] = parsed_args.availability_zone
        if parsed_args.configuration:
            attrs['configuration'] = parsed_args.configuration
        if parsed_args.region:
            attrs['region_name'] = parsed_args.region
        if parsed_args.router:
            attrs['vpc'] = parsed_args.router
        if parsed_args.security_group:
            attrs['securityGroup'] = parsed_args.security_group
        if parsed_args.subnet_id:
            attrs['subnetid'] = parsed_args.subnet_id
        instance = client.create_instance(**attrs)
        instance = set_attributes_for_print_detail(instance)
        return zip(*sorted(six.iteritems(instance)))


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
        try:
            client.delete_instance(parsed_args.instance)
        except Exception as e:
            msg = (_("Failed to delete instance %(instance)s: %(e)s")
                   % {'instance': parsed_args.instance, 'e': e})
            raise exceptions.CommandError(msg)


class ResetDatabaseInstanceStatus(command.Command):

    _description = _("Set the task status of an instance to NONE if the "
                     "instance is in BUILD or ERROR state. Resetting task "
                     "status of an instance in BUILD state will allow "
                     "the instance to be deleted.")

    def get_parser(self, prog_name):
        parser = super(ResetDatabaseInstanceStatus, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID or name of the instance'),
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        db_instances = self.app.client_manager.database.instances
        instance = osc_utils.find_resource(db_instances,
                                           parsed_args.instance)
        db_instances.reset_status(instance)


class ResizeDatabaseInstanceFlavor(command.Command):

    _description = _("Resize an instance with a new flavor")

    def get_parser(self, prog_name):
        parser = super(ResizeDatabaseInstanceFlavor, self).get_parser(
            prog_name
        )
        parser.add_argument(
            'instance',
            metavar='<instance>',
            type=str,
            help=_('ID or name of the instance')
        )
        parser.add_argument(
            'flavor_id',
            metavar='<flavor_id>',
            type=str,
            help=_('New flavor of the instance')
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        db_instances = self.app.client_manager.database.instances
        db_flavor = self.app.client_manager.database.flavors
        instance = osc_utils.find_resource(db_instances,
                                           parsed_args.instance)
        flavor = osc_utils.find_resource(db_flavor,
                                         parsed_args.flavor_id)
        db_instances.resize_instance(instance, flavor)


class UpgradeDatabaseInstance(command.Command):

    _description = _("Upgrades an instance to a new datastore version.")

    def get_parser(self, prog_name):
        parser = super(UpgradeDatabaseInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            type=str,
            help=_('ID or name of the instance.'),
        )
        parser.add_argument(
            'datastore_version',
            metavar='<datastore_version>',
            help=_('ID or name of the instance.'),
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        db_instances = self.app.client_manager.database.instances
        instance = osc_utils.find_resource(db_instances,
                                           parsed_args.instance)
        db_instances.upgrade(instance, parsed_args.datastore_version)


class EnableDatabaseInstanceLog(command.ShowOne):

    _description = _("Instructs Trove guest to start collecting log details.")

    def get_parser(self, prog_name):
        parser = super(EnableDatabaseInstanceLog, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            type=str,
            help=_('Id or Name of the instance.')
        )
        parser.add_argument(
            'log_name',
            metavar='<log_name>',
            type=str,
            help=_('Name of log to publish.')
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        db_instances = self.app.client_manager.database.instances
        instance = osc_utils.find_resource(db_instances,
                                           parsed_args.instance)
        log_info = db_instances.log_enable(instance, parsed_args.log_name)
        result = log_info._info
        return zip(*sorted(six.iteritems(result)))


class ResizeDatabaseInstanceVolume(command.Command):

    _description = _("Resizes the volume size of an instance.")

    def get_parser(self, prog_name):
        parser = super(ResizeDatabaseInstanceVolume, self).get_parser(
            prog_name
        )
        parser.add_argument(
            'instance',
            metavar='<instance>',
            type=str,
            help=_('ID or name of the instance.')
        )
        parser.add_argument(
            'size',
            metavar='<size>',
            type=int,
            default=None,
            help=_('New size of the instance disk volume in GB.')
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        db_instances = self.app.client_manager.database.instances
        instance = osc_utils.find_resource(db_instances,
                                           parsed_args.instance)
        db_instances.resize_volume(instance, parsed_args.size)


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
        db_instances = self.app.client_manager.database.instances
        instance = osc_utils.find_resource(db_instances,
                                           parsed_args.instance)
        db_instances.reset_status(instance)
        try:
            db_instances.delete(instance)
        except Exception as e:
            msg = (_("Failed to delete instance %(instance)s: %(e)s")
                   % {'instance': parsed_args.instance, 'e': e})
            raise exceptions.CommandError(msg)


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
        raise NotImplementedError
        db_instances = self.app.client_manager.database.instances
        instance = osc_utils.find_resource(db_instances,
                                           parsed_args.instance)
        db_instances.restart(instance)


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
        db_instances = self.app.client_manager.database.instances
        instance = osc_utils.find_resource(db_instances,
                                           parsed_args.instance)
        db_instances.edit(instance, parsed_args.configuration,
                          parsed_args.name,
                          parsed_args.detach_replica_source,
                          parsed_args.remove_configuration)
