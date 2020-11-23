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

LOG = logging.getLogger(__name__)


class ListMetrics(command.Lister):
    _description = _('List CES Metrics')
    columns = (
        'namespace',
        'dimensions',
        'metric_name',
        'unit',
    )

    table_columns = (
        'namespace',
        'dimensions.name',
        'dimensions.value',
        'metric_name',
        'unit',
    )

    def get_parser(self, prog_name):
        parser = super(ListMetrics, self).get_parser(prog_name)

        parser.add_argument(
            '--namespace',
            metavar='<namespace>',
            help=_('Namespace of the monitored object, e.g.\n'
                   'SYS.ECS, SYS.VPC')
        )
        parser.add_argument(
            '--metric-name',
            metavar='<metric_name>',
            help=_('Name of the metrics object.')
        )
        parser.add_argument(
            '--unit',
            metavar='<unit>',
            help=_('Unit which is measured.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.ces

        query = {}

        if parsed_args.namespace:
            query['namespace'] = parsed_args.namespace
        if parsed_args.metric_name:
            query['metric_name'] = parsed_args.metric_name
        if parsed_args.unit:
            query['unit'] = parsed_args.unit

        data = client.metrics(**query)

        # Modify table output to provide a better metric overview.
        # Given data set is taken, splitted and flattened to build the table.
        table = ()
        temp_list = []
        big_list = []
        for s in data:
            for item in utils.get_dict_properties(s, self.columns):
                if isinstance(item, (list)):
                    temp_list.append(item[0].name)
                    temp_list.append(item[0].value)
                else:
                    temp_list.append(item)
            big_list.append(tuple(temp_list))
            temp_list = []

        table = (self.table_columns, big_list)

        return table
