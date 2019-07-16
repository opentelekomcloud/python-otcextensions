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
'''CTS Tracker v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

OPERATION_VALUES = ['create', 'delete', 'login']


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class ShowTracker(command.ShowOne):
    _description = _('Show details of a CTS tracker')

    def get_parser(self, prog_name):
        parser = super(ShowTracker, self).get_parser(prog_name)
        parser.add_argument(
            'tracker',
            metavar='<tracker>',
            default='system',
            help=_('Tracker name (currently only `system`)')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.cts

        data = client.get_tracker(
            tracker=parsed_args.tracker,
        )

        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns)

        return (display_columns, data)


class DeleteTracker(command.Command):
    _description = _('Delete CTS Tracker')

    def get_parser(self, prog_name):
        parser = super(DeleteTracker, self).get_parser(prog_name)
        parser.add_argument(
            'tracker',
            metavar='<tracker>',
            nargs='+',
            help=_('Name or ID of the tracker to delete.')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.tracker:
            client = self.app.client_manager.cts
            for tracker in parsed_args.tracker:
                client.delete_tracker(tracker=tracker, ignore_missing=False)


class CreateTracker(command.ShowOne):
    _description = _('Create a single CTS tracker')

    def get_parser(self, prog_name):
        parser = super(CreateTracker, self).get_parser(prog_name)
        parser.add_argument(
            '--bucket_name',
            metavar='<bucket>',
            required=True,
            help=_('Specifies the OBS bucket name. The value is a string of '
                   '0 to 64 characters and can contain uppercase and '
                   'lowercase letters (a to z and A to Z), digits (0 to '
                   '9), hyphens (-), underscores (_), and periods (.). '
                   'In addition, it must start and end with a letter.')
        )
        parser.add_argument(
            '--file_prefix_name',
            metavar='<file_prefix_name>',
            help=_('Specifies the prefix of a log that needs to be stored '
                   'in an OBS  bucket. The value is a string of 0 to 64 '
                   'characters and can contain uppercase and lowercase '
                   'letters (a to z and A to Z), digits (0 to 9), '
                   'hyphens (-), underscores (_), and periods (.)')
        )
        parser.add_argument(
            '--enable_smn',
            action='store_true',
            help=_('Specifies whether SMN is supported. When the value is '
                   '`false`, `topic_id` and `operations` can be left empty.')
        )
        parser.add_argument(
            '--topic_id',
            metavar='<topic>',
            help=_('topic_id is obtained from SMN and in the format of '
                   'urn:smn: ([A-Za-z0-9-]){1,32}:'
                   '([A-Za-z0-9]){32}:'
                   '([A-Za-z0-9]|[_\\-]){1,256}.')
        )
        parser.add_argument(
            '--operation',
            metavar='{' + ','.join(OPERATION_VALUES) + '}',
            type=lambda s: s.lower(),
            choices=OPERATION_VALUES,
            action='append',
            help=_('Specifies trigger conditions for sending a notification '
                   'when Typical is selected. You can select `Delete`, '
                   '`Create`, or `Login` or all of them via repetition. '
                   'Specifies trigger conditions for sending a notification '
                   'when `--send_all_key` is selected. All conditions '
                   'including `Delete`, `Create`, `Change`, and `OpenStack '
                   'API Event` are selected by default. '
                   'Modification is not allowed.')
        )
        parser.add_argument(
            '--send_all_key',
            action='store_true',
            help=_('You can select Typical or All for Trigger Condition.\n'
                   'When the value is `false`, `operations` cannot be left '
                   'empty. When the value is `true`, operations is not '
                   'supported.')
        )
        parser.add_argument(
            '--notify_user',
            metavar='<user>',
            action='append',
            help=_('In Typical scenario, you can specify the users using the '
                   'login function. When these users log in, notifications '
                   'will be sent.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.cts

        attrs = {}

        if parsed_args.bucket_name:
            attrs['bucket_name'] = parsed_args.bucket_name
        if parsed_args.file_prefix_name:
            attrs['file_prefix_name'] = parsed_args.file_prefix_name
        smn = {'enable': False}
        if parsed_args.enable_smn:
            smn['enable'] = True
            if parsed_args.topic_id:
                smn['topic_id'] = parsed_args.topic_id
            if parsed_args.send_all_key:
                smn['topic_id'] = parsed_args.topic_id
            if parsed_args.operation:
                smn['operations'] = parsed_args.operation
            if parsed_args.notify_user:
                smn['notify_users'] = parsed_args.notify_user
        attrs['smn'] = smn

        obj = client.create_tracker(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class SetTracker(command.ShowOne):
    _description = _('Update single CTS tracker properties')

    def get_parser(self, prog_name):
        parser = super(SetTracker, self).get_parser(prog_name)
        parser.add_argument(
            'tracker',
            metavar='<tracker>',
            help=_('Specifies the name of the tracker. Currently only '
                   '`system` is supported.')
        )
        parser.add_argument(
            '--bucket_name',
            metavar='<bucket>',
            required=True,
            help=_('Specifies the OBS bucket name. The value is a string of '
                   '0 to 64 characters and can contain uppercase and '
                   'lowercase letters (a to z and A to Z), digits (0 to '
                   '9), hyphens (-), underscores (_), and periods (.). '
                   'In addition, it must start and end with a letter.')
        )
        parser.add_argument(
            '--file_prefix_name',
            metavar='<file_prefix_name>',
            help=_('Specifies the prefix of a log that needs to be stored '
                   'in an OBS  bucket. The value is a string of 0 to 64 '
                   'characters and can contain uppercase and lowercase '
                   'letters (a to z and A to Z), digits (0 to 9), '
                   'hyphens (-), underscores (_), and periods (.)')
        )
        parser.add_argument(
            '--enable_smn',
            action='store_true',
            help=_('Specifies whether SMN is supported. When the value is '
                   '`false`, `topic_id` and `operations` can be left empty.')
        )
        parser.add_argument(
            '--topic_id',
            metavar='<topic>',
            help=_('topic_id is obtained from SMN and in the format of '
                   'urn:smn: ([A-Za-z0-9-]){1,32}:'
                   '([A-Za-z0-9]){32}:'
                   '([A-Za-z0-9]|[_\\-]){1,256}.')
        )
        parser.add_argument(
            '--operation',
            metavar='{' + ','.join(OPERATION_VALUES) + '}',
            type=lambda s: s.lower(),
            choices=OPERATION_VALUES,
            action='append',
            help=_('Specifies trigger conditions for sending a notification '
                   'when Typical is selected. You can select `Delete`, '
                   '`Create`, or `Login` or all of them via repetition. '
                   'Specifies trigger conditions for sending a notification '
                   'when `--send_all_key` is selected. All conditions '
                   'including `Delete`, `Create`, `Change`, and `OpenStack '
                   'API Event` are selected by default. '
                   'Modification is not allowed.')
        )
        parser.add_argument(
            '--send_all_key',
            action='store_true',
            help=_('You can select Typical or All for Trigger Condition.\n'
                   'When the value is `false`, `operations` cannot be left '
                   'empty. When the value is `true`, operations is not '
                   'supported.')
        )
        parser.add_argument(
            '--notify_user',
            metavar='<user>',
            action='append',
            help=_('In Typical scenario, you can specify the users using the '
                   'login function. When these users log in, notifications '
                   'will be sent.')
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--enable',
            action='store_true',
            help=_('Enable tracing into the bucket')
        )
        group.add_argument(
            '--disable',
            action='store_true',
            help=_('Disable tracing into the bucket')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.cts

        attrs = {}

        if parsed_args.bucket_name:
            attrs['bucket_name'] = parsed_args.bucket_name
        if parsed_args.file_prefix_name:
            attrs['file_prefix_name'] = parsed_args.file_prefix_name
        if parsed_args.enable:
            attrs['status'] = 'enabled'
        elif parsed_args.disable:
            attrs['status'] = 'disabled'
        smn = {'enable': False}
        if parsed_args.enable_smn:
            smn['enable'] = True
            if parsed_args.topic_id:
                smn['topic_id'] = parsed_args.topic_id
            if parsed_args.send_all_key:
                smn['topic_id'] = parsed_args.topic_id
            if parsed_args.operation:
                smn['operations'] = parsed_args.operation
            if parsed_args.notify_user:
                smn['notify_users'] = parsed_args.notify_user
        attrs['smn'] = smn

        obj = client.update_tracker(tracker=parsed_args.tracker, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
