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
"""ModelArts service v1 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def set_attributes_for_print(clusters):
    for cluster in clusters:
        cluster.allocatable_resources = {
            "cpu_cores": cluster.allocatable_cpu_cores,
            "memory": cluster.allocatable_memory,
            "gpus": cluster.allocatable_gpus,
        }
        yield cluster


class ListServiceClusters(command.Lister):
    _description = _("List dedicated clusters for service deployment.")
    columns = (
        "Cluster Id",
        "Cluster Name",
        "Created At",
        "Status",
        "Allocatable Resources",
        "Charging Mode",
        "Max Node Count",
        "Nodes",
        "Services Count",
    )

    def get_parser(self, prog_name):
        parser = super(ListServiceClusters, self).get_parser(prog_name)
        parser.add_argument(
            "--cluster-name",
            metavar="<cluster_name>",
            help=_("Cluster name."),
        )
        parser.add_argument(
            "--status",
            metavar="<status>",
            help=_("Cluster Status."),
        )
        parser.add_argument(
            "--offset",
            metavar="<offset>",
            type=int,
            help=_("Start page of the paging list. Default value: 0"),
        )
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_(
                "Maximum number of records returned on each page. "
                "Default value: 1000"
            ),
        )
        parser.add_argument(
            "--sort-by",
            metavar="<sort_by>",
            help=_(
                "Sorting field. The options are as follows:"
                "\ncreated_at: default value"
                "\ncluster_name"
            ),
        )
        parser.add_argument(
            "--order",
            metavar="<order>",
            help=_(
                "Sorting mode. The default value is desc. Options:"
                "\n`asc`: ascending order"
                "\n`desc`: descending order"
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        args_list = (
            "cluster_name",
            "limit",
            "offset",
            "order",
            "sort_by",
            "status",
        )
        query_params = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                query_params[arg] = val

        data = client.service_clusters(**query_params)
        if data:
            data = set_attributes_for_print(data)

        formatters = {
            "Created At": cli_utils.UnixTimestampFormatter,
            "Nodes": cli_utils.YamlFormat,
            "Allocatable Resources": cli_utils.YamlFormat,
            "Services Count": cli_utils.YamlFormat,
        }

        return (
            self.columns,
            (
                utils.get_item_properties(
                    s, self.columns, formatters=formatters
                )
                for s in data
            ),
        )
