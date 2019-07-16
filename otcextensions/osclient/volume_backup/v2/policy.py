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
'''VolumeBackup Policy v1 action implementations'''
import argparse
# import json
import logging

from cliff import columns

# from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


class BackupPolicy(columns.FormattableColumn):

    def human_readable(self):
        if self._value is None:
            return None

        return self._value.to_dict()

    def machine_readable(self):
        if self._value is None:
            return None

        return self._value.to_dict()


_formatters = {
    'scheduled_policy': BackupPolicy
}


class ListVolumeBackupPolicy(command.Lister):
    _description = _('List VolumeBackup Policies')
    columns = ('id', 'name', 'policy_resource_count', 'scheduled_policy',
               'tags')

    def get_parser(self, prog_name):
        parser = super(ListVolumeBackupPolicy, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):

        args = {}

        client = self.app.client_manager.volume_backup

        data = client.backup_policies(**args)

        return (
            self.columns,
            (utils.get_item_properties(
                s, self.columns, formatters=_formatters
            ) for s in data))


class DeleteVolumeBackupPolicy(command.Command):
    _description = _('Delete VolumeBackup Policy')

    def get_parser(self, prog_name):
        parser = super(DeleteVolumeBackupPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('id of the policy.')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.policy:
            client = self.app.client_manager.volume_backup
            client.delete_backup_policy(
                backup_policy=parsed_args.policy,
                ignore_missing=False)


class ShowVolumeBackupPolicy(command.ShowOne):
    _description = _('Show VolumeBackup Policy')
    columns = ('id', 'name', 'policy_resource_count', 'scheduled_policy',
               'tags')

    def get_parser(self, prog_name):
        parser = super(ShowVolumeBackupPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_('ID or Name of the policy.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.volume_backup

        data = client.find_backup_policy(name_or_id=parsed_args.policy)

        return (
            self.columns,
            utils.get_item_properties(
                data, self.columns, formatters=_formatters
            ))


class CreateVolumeBackupPolicy(command.ShowOne):
    _description = _('Create VolumeBackup Policy')
    columns = ('id', 'name', 'policy_resource_count', 'scheduled_policy',
               'tags')

    def get_parser(self, prog_name):
        parser = super(CreateVolumeBackupPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the policy.')
        )
        parser.add_argument(
            '--start_time',
            metavar='<start_time>',
            required=True,
            help=_('Specifies the start time of the backup job. '
                   'You need to convert the local time to the '
                   'Coordinated Universal Time (UTC), and set the '
                   'start time to an integral hour point.\n'
                   'You can set multiple time points (at integral '
                   'hours only), and use commas (,) to separate one time '
                   'point from another. The value is in the HH:mm format.')
        )
        parser.add_argument(
            '--enable',
            action='store_true',
            help=_('Specifies whether the backup policy should be enabled '
                   '`status=ON`. By default `status=OFF` is used')
        )
        parser.add_argument(
            '--frequency',
            metavar='<frequency>',
            type=int,
            choices=range(1, 15),
            required=True,
            help=_('Specifies the backup interval (1 to 14 days). '
                   'Select either this parameter or week_frequency. If '
                   'you select both, this parameter is used.')
        )
        parser.add_argument(
            '--rentention_num',
            metavar='<rentention_num>',
            type=int,
            required=True,
            help=_('Specifies the retained number (minimum: 2) of backups. '
                   'Select either this parameter or rentention_day. '
                   'If you select both, this parameter is used.')
        )
        parser.add_argument(
            '--remain_first_backup_of_curMonth',
            action='store_true',
            help=_('Indicates whether to retain the first backup in the '
                   'current month. \n')
        )
        parser.add_argument(
            '--tag',
            metavar='<tag>',
            action='append',
            help=_('User defined tags to attach to the policy.\n'
                   'format: KEY=VALUE\n'
                   'KEY: [::ALPHANUM::]{0..36}\n'
                   'VALUE: [::ALPHANUM::]{0..43}\n'
                   '(Repeat multiple times for multiple tags)')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        attrs['name'] = parsed_args.name
        policy = {}
        policy['start_time'] = parsed_args.start_time
        if parsed_args.frequency:
            policy['frequency'] = parsed_args.frequency
        if parsed_args.rentention_num:
            policy['rentention_num'] = parsed_args.rentention_num
        if parsed_args.remain_first_backup_of_curMonth:
            policy['remain_first_backup_of_curMonth'] = 'Y'
        else:
            policy['remain_first_backup_of_curMonth'] = 'N'
        policy['status'] = 'ON' if parsed_args.enable else 'OFF'

        attrs['scheduled_policy'] = policy
        if parsed_args.tag:
            attrs['tags'] = []
            for tag in parsed_args.tag:
                tag_parts = tag.split('=')
                if 2 == len(tag_parts):
                    tag_dict = {
                        'key': tag_parts[0],
                        'value': tag_parts[1]
                    }
                    attrs['tags'].append(tag_dict)
                else:
                    msg = _('Cannot parse tag information')
                    raise argparse.ArgumentTypeError(msg)

        client = self.app.client_manager.volume_backup

        data = client.create_backup_policy(**attrs)

        return (
            self.columns,
            utils.get_item_properties(
                data, self.columns, formatters=_formatters
            ))


class UpdateVolumeBackupPolicy(command.ShowOne):
    _description = _('Update VolumeBackup Policy')
    columns = ('id', 'name', 'policy_resource_count', 'scheduled_policy',
               'tags')

    def get_parser(self, prog_name):
        parser = super(UpdateVolumeBackupPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=_('id of the policy.')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('Name of the policy.')
        )
        parser.add_argument(
            '--start_time',
            metavar='<start_time>',
            help=_('Specifies the start time of the backup job. '
                   'You need to convert the local time to the '
                   'Coordinated Universal Time (UTC), and set the '
                   'start time to an integral hour point.\n'
                   'You can set multiple time points (at integral '
                   'hours only), and use commas (,) to separate one time '
                   'point from another. The value is in the HH:mm format.')
        )
        parser.add_argument(
            '--status',
            dest='status',
            type=sdk_utils.str2bool,
            nargs='?',
            help=_('Specifies whether or notthe backup policy should be '
                   'enabled (`true`, `false`)')
        )
        parser.add_argument(
            '--frequency',
            metavar='<frequency>',
            type=int,
            choices=range(1, 15),
            help=_('Specifies the backup interval (1 to 14 days). '
                   'Select either this parameter or week_frequency. If '
                   'you select both, this parameter is used.')
        )
        parser.add_argument(
            '--rentention_num',
            metavar='<rentention_num>',
            type=int,
            help=_('Specifies the retained number (minimum: 2) of backups. '
                   'Select either this parameter or rentention_day. '
                   'If you select both, this parameter is used.')
        )
        parser.add_argument(
            '--remain_first_backup_of_curMonth',
            dest='remain_first_backup_of_curMonth',
            type=sdk_utils.str2bool,
            nargs='?',
            help=_('Indicates whether or notto retain the first backup in the '
                   'current month (`true`, `false`). \n')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        policy = {}
        if parsed_args.start_time:
            policy['start_time'] = parsed_args.start_time
        if parsed_args.frequency:
            policy['frequency'] = parsed_args.frequency
        if parsed_args.rentention_num:
            policy['rentention_num'] = parsed_args.rentention_num
        if parsed_args.status is not None:
            policy['status'] = 'ON' if parsed_args.status else 'OFF'
        if parsed_args.remain_first_backup_of_curMonth is not None:
            if parsed_args.remain_first_backup_of_curMonth:
                policy['remain_first_backup_of_curMonth'] = 'Y'
            else:
                policy['remain_first_backup_of_curMonth'] = 'N'

        if policy:
            attrs['scheduled_policy'] = policy

        client = self.app.client_manager.volume_backup
        data = client.update_backup_policy(
            backup_policy=parsed_args.id,
            **attrs)

        return (
            self.columns,
            utils.get_item_properties(
                data, self.columns, formatters=_formatters
            ))


class ExecuteVolumeBackupPolicy(command.Command):
    _description = _('Execute VolumeBackup Policy')

    def get_parser(self, prog_name):
        parser = super(ExecuteVolumeBackupPolicy, self).get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<id>',
            help=_('id of the policy.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.volume_backup
        client.execute_policy(backup_policy=parsed_args.policy)
        return


class LinkResourceToVolumeBackupPolicy(command.Command):
    _description = _('Link Resources to VolumeBackup Policy')

    def get_parser(self, prog_name):
        parser = super(LinkResourceToVolumeBackupPolicy, self).\
            get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<id>',
            help=_('id of the policy.')
        )
        parser.add_argument(
            '--volume',
            metavar='<volume_id>',
            action='append',
            help=_('id of volume to attach to the policy.'
                   '(repeat multiple times)')
        )
        return parser

    def take_action(self, parsed_args):
        volumes = parsed_args.volume

        client = self.app.client_manager.volume_backup
        client.link_resources_to_policy(
            backup_policy=parsed_args.policy,
            resources=volumes)
        return


class UnlinkResourceFromVolumeBackupPolicy(command.Command):
    _description = _('Unlink Resources to VolumeBackup Policy')

    def get_parser(self, prog_name):
        parser = super(UnlinkResourceFromVolumeBackupPolicy, self).\
            get_parser(prog_name)
        parser.add_argument(
            'policy',
            metavar='<id>',
            help=_('id of the policy.')
        )
        parser.add_argument(
            '--volume',
            metavar='<volume_id>',
            action='append',
            help=_('id of volume to remove from the policy.'
                   '(repeat multiple times)')
        )
        return parser

    def take_action(self, parsed_args):
        volumes = parsed_args.volume

        client = self.app.client_manager.volume_backup
        client.unlink_resources_of_policy(
            backup_policy=parsed_args.policy,
            resources=volumes)
        return
