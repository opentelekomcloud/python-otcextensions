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
'''DCS Instance v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

STATUS_VALUES = ['CREATING', 'CREATEFAILED', 'RUNNING', 'ERROR', 'STARTING',
                 'RESTARTING', 'CLOSING', 'CLOSED', 'EXTENDING']

PRODUCT_ID_VALUES = ['OTC_DCS_SINGLE', 'OTC_DCS_CL', 'OTC_DCS_MS']

_formatters = {
}


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ListInstance(command.Lister):
    _description = _('List DCS Instances')
    columns = ('id', 'name', 'engine', 'status', 'error_code')

    def get_parser(self, prog_name):
        parser = super(ListInstance, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Limit number of records to return.')
        )
        parser.add_argument(
            '--start',
            metavar='<start>',
            type=int,
            help=_('Start number for querying.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('DCS instance name.')
        )
        parser.add_argument(
            '--status',
            metavar='{' + ','.join(STATUS_VALUES) + '}',
            type=lambda s: s.upper(),
            choices=STATUS_VALUES,
            help=_('DCS instance status value to query.')
        )
        parser.add_argument(
            '--include_failure',
            action='store_true',
            help=_('An indicator of whether the number of DCS instances '
                   'that failed to be created will be returned to the API '
                   'caller.')
        )
        parser.add_argument(
            '--exact_match',
            action='store_true',
            help=_('An indicator of whether to perform an exact or fuzzy '
                   'match based on instance name.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dcs

        query = {}
        if parsed_args.limit:
            query['limit'] = parsed_args.limit
        if parsed_args.start:
            query['start'] = parsed_args.start
        if parsed_args.name:
            query['name'] = parsed_args.name
        if parsed_args.status:
            query['status'] = parsed_args.status
        if parsed_args.include_failure:
            query['includeFailure'] = parsed_args.include_failure
        if parsed_args.exact_match:
            query['exactMatchName'] = parsed_args.exact_match

        data = client.instances(
            **query
        )

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns,
                 ) for s in data))
        return table


class DeleteInstance(command.Command):
    _description = _('Delete DCS Instance')

    def get_parser(self, prog_name):
        parser = super(DeleteInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            nargs='+',
            help=_('Name or ID of the instance to delete.')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.instance:
            client = self.app.client_manager.dcs
            for instance in parsed_args.instance:
                client.delete_instance(instance=instance)


class ShowInstance(command.ShowOne):
    _description = _('Show the details of a single instance')

    def get_parser(self, prog_name):
        parser = super(ShowInstance, self).get_parser(prog_name)

        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('Name or UUID of the instance.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        obj = client.find_instance(
            name_or_id=parsed_args.instance)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class CreateInstance(command.ShowOne):
    _description = _('Create a single DCS instance')

    def get_parser(self, prog_name):
        parser = super(CreateInstance, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=True,
            help=_('DCS instance name. An instance name is a string of '
                   '4-64 characters that contain letters, digits, underscores '
                   '(_), and hyphens (-). An instance name must start '
                   'with letters.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Brief description of the DCS instance. A brief '
                   'description supports up to 1024 characters. NOTE "\\" '
                   'is defined as an escape character in the queue '
                   'description. If you need to enter a backward slash (\\) '
                   'or a double quotation mark (") in the queue description, '
                   'enter \\ or \\\"')
        )
        parser.add_argument(
            '--engine',
            metavar='<engine>',
            default='redis',
            help=_('Cache engine, which is Redis.')
        )
        parser.add_argument(
            '--engine_version',
            metavar='<version>',
            default='3.0.7',
            help=_('Cache engine version, which is 3.0.7.')
        )
        parser.add_argument(
            '--capacity',
            metavar='<size>',
            type=int,
            required=True,
            choices=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512],
            help=_('Cache capacity. Unit: GB. For a single-node DCS instance '
                   'and master/standby DCS instance, the cache capacity can '
                   'be: 1, 2, 4, 8, 16, 32, or 64 GB. For a DCS instance in '
                   'cluster mode, the cache capacity can be 64, 128, 256, '
                   'or 512 GB.')
        )
        parser.add_argument(
            '--password',
            metavar='<password>',
            required=True,
            help=_('Password of a DCS instance. Password complexity '
                   'requirements:\n'
                   '* A string of 8-32 characters.\n'
                   '* Contains at least three types of the following '
                   'characters:\n'
                   '* Uppercase letters\n'
                   '* Lowercase letters\n'
                   '* Digits\n'
                   '* Special characters, such as '
                   '~!@#$%%^&*()-_=+\\|[{}]:\'",<.>/?')
        )
        parser.add_argument(
            '--vpc_id',
            metavar='<id>',
            required=True,
            help=_('Tenant\'s Virtual Private Cloud (VPC) ID.')
        )
        parser.add_argument(
            '--security_group_id',
            metavar='<id>',
            required=True,
            help=_('Tenant\'s security group ID.')
        )
        parser.add_argument(
            '--subnet_id',
            metavar='<id>',
            required=True,
            help=_('Subnet ID.')
        )
        parser.add_argument(
            '--az',
            metavar='<az>',
            required=True,
            help=_('Availability zone.')
        )
        parser.add_argument(
            '--product_id',
            metavar='{' + ','.join(PRODUCT_ID_VALUES) + '}',
            type=lambda s: s.upper(),
            choices=PRODUCT_ID_VALUES,
            required=True,
            help=_('Product ID used to differentiate DCS instance types. '
                   'Values:\n'
                   '* OTC_DCS_SINGLE: indicates a single-node DCS instance.\n'
                   '* OTC_DCS_MS: indicates a master/standby DCS instance.\n'
                   '* OTC_DCS_CL: indicates a DCS instance in cluster mode.')
        )
        parser.add_argument(
            '--backup_policy',
            metavar='<json>',
            help=_('Backup policy JSON.\n'
                   '{\n'
                   '"save_days" - retention time [1-7]\n'
                   '"backup_type" - [auto,manual]\n'
                   '"periodical_backup_plan": {\n'
                   '"begin_at" - time when backup starts\n'
                   '"period_type" - [weekly]\n'
                   '"backup_at" - array of days [1-7]\n'
                   '}\n'
                   '}')
        )
        parser.add_argument(
            '--maintain_begin',
            metavar='<HH:mm:ss>',
            help=_('Time at which the maintenance time window starts.\n'
                   'The start time must be set to 22:00:00, 02:00:00,'
                   '06:00:00, 10:00:00, 14:00:00, or 18:00:00.\n'
                   'Parameters maintain_begin and maintain_end must be '
                   'set in pairs. If parameter maintain_start is left blank, '
                   'parameter maintain_end is also blank. In this case, the '
                   'system automatically allocates the default start time '
                   '02:00:00.')
        )
        parser.add_argument(
            '--maintain_end',
            metavar='<HH:mm:ss>',
            help=_('Time at which the maintenance time window starts.\n'
                   'The end time is four hours later than the start time. '
                   'For example, if the start time is 22:00:00, the end time '
                   'is 02:00:00.\n'
                   'Parameters maintain_begin and maintain_end must be '
                   'set in pairs. If parameter maintain_end is left blank, '
                   'parameter maintain_start is also blank. In this case, the '
                   'system automatically allocates the default end time '
                   '06:00:00.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.engine:
            attrs['engine'] = parsed_args.engine
        if parsed_args.engine_version:
            attrs['engine_version'] = parsed_args.engine_version
        if parsed_args.capacity:
            attrs['capacity'] = parsed_args.capacity
        if parsed_args.password:
            attrs['password'] = parsed_args.password
        if parsed_args.vpc_id:
            attrs['vpc_id'] = parsed_args.vpc_id
        if parsed_args.security_group_id:
            attrs['security_group_id'] = parsed_args.security_group_id
        if parsed_args.subnet_id:
            attrs['subnet_id'] = parsed_args.subnet_id
        if parsed_args.az:
            attrs['az'] = parsed_args.az
        if parsed_args.product_id:
            attrs['product_id'] = parsed_args.product_id
        if parsed_args.backup_policy:
            attrs['backup_policy'] = parsed_args.backup_policy
        if parsed_args.maintain_begin and parsed_args.maintain_end:
            attrs['maintain_begin'] = parsed_args.maintain_begin
            attrs['maintain_end'] = parsed_args.maintain_end

        obj = client.create_instance(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class SetInstance(command.ShowOne):
    _description = _('Update a single DCS instance')

    def get_parser(self, prog_name):
        parser = super(SetInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID or Name of the instance to modify')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('DCS instance name. An instance name is a string of '
                   '4-64 characters that contain letters, digits, underscores '
                   '(_), and hyphens (-). An instance name must start '
                   'with letters.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Brief description of the DCS instance. A brief '
                   'description supports up to 1024 characters. NOTE "\\" '
                   'is defined as an escape character in the queue '
                   'description. If you need to enter a backward slash (\\) '
                   'or a double quotation mark (") in the queue description, '
                   'enter \\ or \\\"')
        )
        parser.add_argument(
            '--security_group_id',
            metavar='<id>',
            help=_('Tenant\'s security group ID.')
        )
        parser.add_argument(
            '--backup_policy',
            metavar='<json>',
            help=_('Backup policy JSON.\n'
                   '{\n'
                   '"save_days" - retention time [1-7]\n'
                   '"backup_type" - [auto,manual]\n'
                   '"periodical_backup_plan": {\n'
                   '"begin_at" - time when backup starts\n'
                   '"period_type" - [weekly]\n'
                   '"backup_at" - array of days [1-7]\n'
                   '}\n'
                   '}')
        )
        parser.add_argument(
            '--maintain_begin',
            metavar='<HH:mm:ss>',
            help=_('Time at which the maintenance time window starts.\n'
                   'The start time must be set to 22:00:00, 02:00:00,'
                   '06:00:00, 10:00:00, 14:00:00, or 18:00:00.\n'
                   'Parameters `maintain_begin` and `maintain_end` must be '
                   'set in pairs. If parameter `maintain_start` is left '
                   'blank, parameter `maintain_end` is also blank. In this '
                   'case, the system automatically allocates the default '
                   'start time 02:00:00.')
        )
        parser.add_argument(
            '--maintain_end',
            metavar='<HH:mm:ss>',
            help=_('Time at which the maintenance time window starts.\n'
                   'The end time is four hours later than the start time. '
                   'For example, if the start time is 22:00:00, the end time '
                   'is 02:00:00.\n'
                   'Parameters `maintain_begin` and `maintain_end` must be '
                   'set in pairs. If parameter `maintain_end` is left blank, '
                   'parameter `maintain_start` is also blank. In this case, '
                   'the system automatically allocates the default end time '
                   '06:00:00.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.security_group_id:
            attrs['security_group_id'] = parsed_args.security_group_id
        if parsed_args.backup_policy:
            attrs['backup_policy'] = parsed_args.backup_policy
        if parsed_args.maintain_begin and parsed_args.maintain_end:
            attrs['maintain_begin'] = parsed_args.maintain_begin
            attrs['maintain_end'] = parsed_args.maintain_end

        obj = client.update_instance(instance=parsed_args.instance, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class ExtendInstance(command.ShowOne):
    _description = _('Extend capacity of a single DCS instance')

    def get_parser(self, prog_name):
        parser = super(ExtendInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID or Name of the instance to modify')
        )
        parser.add_argument(
            '--capacity',
            metavar='<size>',
            type=int,
            required=True,
            choices=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512],
            help=_('Value in GB for the new instance capacity.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        inst = client.find_instance(
            name_or_id=parsed_args.instance,
            ignore_missing=False)

        obj = client.extend_instance(
            instance=inst.id,
            capacity=parsed_args.capacity)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class _OperationInstance(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super(_OperationInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID or Name of the instance to modify')
        )
        return parser


class StopInstance(_OperationInstance):
    _description = _('Stop a single DCS instance')

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        obj = client.stop_instance(instance=parsed_args.instance)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class StartInstance(_OperationInstance):
    _description = _('Start a single DCS instance')

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        obj = client.start_instance(instance=parsed_args.instance)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)


class RestartInstance(_OperationInstance):
    _description = _('Restart a single DCS instance')

    def take_action(self, parsed_args):

        client = self.app.client_manager.dcs

        obj = client.restart_instance(instance=parsed_args.instance)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)

        return (display_columns, data)
