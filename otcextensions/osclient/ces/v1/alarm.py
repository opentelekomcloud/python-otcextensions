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
'''CES Alarm v1 action implementations'''
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _translate_alarm_level(level):
    case = {
        1: '1: Critical',
        2: '2: Major',
        3: '3: Minor',
        4: '4: Informational'
    }
    return case.get(level)


def _flatten_output(obj):
    data = {
        'id': obj.id,
        'name': obj.name,
        'metric.resource_type': obj.metric.namespace,
        # The return value of obj.metric.dimensions is a list. The list has
        # only one value. It is not possible to have several items inside.
        'metric.monitored_obj': obj.metric.dimensions[0].value,
        'alarm_level': _translate_alarm_level(obj.alarm_level),
        'enabled': obj.alarm_enabled,
        'action_enabled': obj.alarm_action_enabled,
        'state': obj.alarm_state,
    }
    return data


def _get_columns(item):
    column_map = {
    }
    inv_columns = ['']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           inv_columns)


# TODO(undefined): Implement query arguments -> SDK not working
class ListAlarms(command.Lister):
    _description = _('List CES alarms')
    columns = (
        'id',
        'name',
        'metric.resource_type',
        'metric.monitored_obj',
        'alarm_level',
        'enabled',
        'action_enabled',
        'state'
    )

    def get_parser(self, prog_name):
        parser = super(ListAlarms, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.ces

        data = client.alarms()

        table = (self.columns,
                 (utils.get_dict_properties(
                     _flatten_output(s), self.columns
                 ) for s in data))
        return table


class ShowAlarm(command.ShowOne):
    _description = _('Show CloudEye alarm rule details')

    def get_parser(self, prog_name):
        parser = super(ShowAlarm, self).get_parser(prog_name)

        parser.add_argument(
            'alarm',
            metavar='<alarm>',
            help=_('UUID or name of the alarm rule.')
        )
        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.ces

        obj = client.find_alarm(
            parsed_args.alarm,
            ignore_missing=False
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteAlarm(command.Command):
    _description = _('Delete CES alarm')

    def get_parser(self, prog_name):
        parser = super(DeleteAlarm, self).get_parser(prog_name)

        parser.add_argument(
            'alarm',
            metavar='<alarm>',
            nargs='+',
            help=_('UUID or name of the alarm.')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.alarm:
            client = self.app.client_manager.ces
            for alarm in parsed_args.alarm:
                alarm = client.find_alarm(alarm, ignore_missing=False)
                client.delete_alarm(alarm=alarm)


class SetAlarm(command.ShowOne):
    _description = _('Switch Alarm status.')

    def get_parser(self, prog_name):
        parser = super(SetAlarm, self).get_parser(prog_name)

        parser.add_argument(
            'alarm',
            metavar='<alarm>',
            help=_('UUID or name of the alarm.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.ces

        alarm = client.find_alarm(parsed_args.alarm, ignore_missing=False)

        if alarm:
            client.update_alarm_enabled(
                alarm=alarm
            )

            # instance of alarm needs to be found again due to missing
            # return body of alarm rule update function
            obj = client.find_alarm(
                parsed_args.alarm,
                ignore_missing=False
            )
            display_columns, columns = _get_columns(obj)
            data = utils.get_item_properties(obj, columns)
            return (display_columns, data)


class CreateAlarm(command.ShowOne):
    _description = _('Create CloudEye alarm rule')

    def get_parser(self, prog_name):
        parser = super(CreateAlarm, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Alarm name')
        )
        parser.add_argument(
            '--enabled',
            metavar='<enabled>',
            help=_('State of the alarm.'
                   'True: enable alarm (default)'
                   'False: disable alarm')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description of the alarm')
        )
        parser.add_argument(
            '--action-enabled',
            default=False,
            required=True,
            help=_('Specifies whether the alarm action is triggered')
        )
        parser.add_argument(
            '--level',
            metavar='<level>',
            type=int,
            help=_('Indicates the alarm level'
                   '1: critical'
                   '2: major'
                   '3: minor'
                   '4: informational')
        )

        # AlarmActions
        parser.add_argument(
            '--alarm-action-type',
            metavar='<alarm_action_type>',
            help=_('Specifies the alarms action type'
                   'notification: notification will be sent to user'
                   'autoscaling: scaling action will be triggered')
        )
        parser.add_argument(
            '--alarm-action-notification-list',
            metavar='<alarm_action_notification_list>',
            action='append',
            help=_('Specifies the list of objects being notified when'
                   'alarm status changes.'
                   'URN example structure:'
                   'urn:smn:region:68438a86d98e427e907e0097b7e35d48:sd'
                   'The parameter can be given multiple times to'
                   'notify multiple targets')
        )

        # OkActions
        parser.add_argument(
            '--ok-action-type',
            metavar='<ok_action_type>',
            help=_('Specifies the alarms action type'
                   'notification: notification will be sent to user'
                   'autoscaling: scaling action will be triggered')
        )
        parser.add_argument(
            '--ok-action-notification-list',
            metavar='<ok_action_notification_list>',
            action='append',
            help=_('Specifies the list of objects being notified when'
                   'alarm status changes.'
                   'URN example structure:'
                   'urn:smn:region:68438a86d98e427e907e0097b7e35d48:sd'
                   'The parameter can be given multiple times to'
                   'notify multiple targets')
        )

        # ConditionSpec
        parser.add_argument(
            '--comparison-operator',
            metavar='<comparison_operator>',
            required=True,
            help=_('Specifies the conditions comparison operator'
                   'Values: >, =, <, ≥, or ≤')
        )
        parser.add_argument(
            '--count',
            metavar='<count>',
            type=int,
            required=True,
            help=_('Specifies how many times the alarm condition has to'
                   'triggered until Alarm raises'
                   'Value range: 1 to 5')
        )
        parser.add_argument(
            '--filter',
            metavar='<filter>',
            required=True,
            help=_('Specifies the data rollup method.'
                   'Values: max, min, average, sum, variance')
        )
        parser.add_argument(
            '--period',
            metavar='<period>',
            required=True,
            help=_('Indicates the interval (in seconds) for checking'
                   'whether the configured alarm rules are met')
        )
        parser.add_argument(
            '--unit',
            metavar='<unit>',
            help=_('Specifies data unit'
                   'Values: B/s, %')
        )
        parser.add_argument(
            '--value',
            metavar='<value>',
            required=True,
            help=_('Specifies the alarm threshold'
                   'Values: 0 to max(int)')
        )

        # DimensionsSpec for Metrics
        # This is a list of dictionaries
        # IMPROVEMENT NEEDED
        parser.add_argument(
            '--dimension-name',
            action='append',
            metavar='<dimension_name>',
            required=True,
            help=_('dimension.name: object type e.g. ECS')
        )
        parser.add_argument(
            '--dimension-value',
            action='append',
            required=True,
            metavar='<dimension_value>',
            help=_('dimension.value: object id e.g. ECS ID')
        )

        # MetricSpec
        parser.add_argument(
            '--metric-name',
            metavar='<metric_name>',
            required=True,
            help=_('Specifies the metric name')
        )
        parser.add_argument(
            '--namespace',
            metavar='<namespace>',
            required=True,
            help=_('Specifies the namespace of the metric such as SYS.ECS')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.ces

        attrs = {}

        attrs['name'] = parsed_args.name
        if parsed_args.enabled:
            attrs['alarm_enabled'] = parsed_args.enabled
        if parsed_args.description:
            attrs['alarm_description'] = parsed_args.description
        attrs['alarm_action_enabled'] = parsed_args.action_enabled
        if parsed_args.level:
            attrs['alarm_level'] = parsed_args.level

        if parsed_args.action_enabled is True:
            if (parsed_args.ok_action_type
                    and parsed_args.ok_action_notification_list):

                nl = parsed_args.ok_action_notification_list
                ok_actions = {
                    'type': parsed_args.ok_action_type,
                    'notificationList': nl
                }
                attrs['ok_actions'] = ok_actions

            if (parsed_args.alarm_action_type
                    and parsed_args.alarm_action_notification_list):

                nl = parsed_args.alarm_action_notification_list
                alarm_actions = {
                    'type': parsed_args.alarm_action_type,
                    'notificationList': nl
                }
                attrs['alarm_actions'] = alarm_actions

        condition = {
            'comparison_operatur': parsed_args.comparison_operator,
            'count': parsed_args.count,
            'filter': parsed_args.filter,
            'period': parsed_args.period,
            'value': parsed_args.value
        }
        if parsed_args.unit:
            condition = {
                'unit': parsed_args.unit
            }
        attrs['condition'] = condition

        dimensions = {
            'name': parsed_args.dimension_name,
            'value': parsed_args.dimension_value
        }
        metric = {
            'dimensions': dimensions,
            'metric_name': parsed_args.metric_name,
            'namespace': parsed_args.namespace
        }
        attrs['metric'] = metric

        obj = client.create_alarm(
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)
