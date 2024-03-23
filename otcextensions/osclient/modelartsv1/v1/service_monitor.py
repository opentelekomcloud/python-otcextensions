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

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def set_attributes_for_print(monitors):
    for monitor in monitors:
        monitor.cpu_core = f"{monitor.cpu_core_usage}/{monitor.cpu_core_total}"
        monitor.cpu_memory = (
            f"{monitor.cpu_memory_usage}/{monitor.cpu_memory_total}"
        )
        monitor.gpu = f"{monitor.gpu_usage}/{monitor.gpu_total}"
        yield monitor


class ServiceMonitor(command.Lister):
    _description = _("Get Monitoring Information of a Service.")
    columns = (
        "Model Id",
        "Model Name",
        "Model Version",
        "Invocation Times",
        "Failed Times",
        "CPU Core",
        "CPU Memory",
        "GPU",
    )

    def get_parser(self, prog_name):
        parser = super(ServiceMonitor, self).get_parser(prog_name)

        parser.add_argument(
            "service",
            metavar="<service>",
            help=_("Service ID or Name."),
        )
        parser.add_argument(
            "--node-id",
            metavar="<node_id>",
            help=_(
                "ID of the node to be queried. By default, "
                "all nodes are queried."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        query_params = {}
        if parsed_args.node_id:
            query_params["node_id"] = parsed_args.node_id

        service = client.find_service(parsed_args.service)
        data = client.service_monitor(service.id, **query_params)

        if data:
            data = set_attributes_for_print(data)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )
