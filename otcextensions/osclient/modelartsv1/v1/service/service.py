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

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

INFER_TYPE_CHOICES = ["real-time", "batch"]

SORT_BY_CHOICES = ["publish_at", "service_name"]

SORT_ORDER_CHOICES = ["asc", "desc"]

STATUS_CHOICES = [
    "running",
    "deploying",
    "concerning",
    "failed",
    "stopped",
    "finished",
]

_formatters = {
    "additional_properties": cli_utils.YamlFormat,
    "config": cli_utils.YamlFormat,
    "operation_time": cli_utils.UnixTimestampFormatter,
    "publish_at": cli_utils.UnixTimestampFormatter,
    "transition_at": cli_utils.UnixTimestampFormatter,
    "update_time": cli_utils.UnixTimestampFormatter,
}


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


class ListService(command.Lister):
    _description = _("Get properties of a service")
    columns = (
        "Service Id",
        "Service Name",
        "Infer Type",
        "Status",
    )

    def get_parser(self, prog_name):
        parser = super(ListService, self).get_parser(prog_name)
        parser.add_argument(
            "--cluster-id",
            metavar="<cluster_id>",
            help=_("Dedicated resource pool ID."),
        )
        parser.add_argument(
            "--infer-type",
            metavar="{" + ",".join(INFER_TYPE_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=INFER_TYPE_CHOICES,
            help=_("Inference mode."),
        )
        parser.add_argument(
            "--limit",
            type=int,
            metavar="<limit>",
            help=_("Records Limit. Default value: 1000"),
        )
        parser.add_argument(
            "--model-id",
            metavar="<model_id>",
            help=_("Model Name."),
        )
        parser.add_argument(
            "--offset",
            metavar="<offset>",
            type=int,
            help=_("Start page of the paging list. Default value: 0"),
        )
        parser.add_argument(
            "--order",
            metavar="{" + ",".join(SORT_ORDER_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=SORT_ORDER_CHOICES,
            help=_("Sorting order. Default value: desc"),
        )
        parser.add_argument(
            "--service-id",
            metavar="<service_id>",
            help=_("Service ID."),
        )
        parser.add_argument(
            "--service-name",
            metavar="<service_name>",
            help=_("Service Name."),
        )
        parser.add_argument(
            "--sort-by",
            metavar="{" + ",".join(SORT_BY_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=SORT_BY_CHOICES,
            help=_("Sorting field. Default value: publish_at"),
        )
        parser.add_argument(
            "--status",
            metavar="{" + ",".join(STATUS_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=STATUS_CHOICES,
            help=_("Service status."),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_("Workspace ID."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        args_list = (
            "cluster_id",
            "infer_type",
            "limit",
            "model_id",
            "offset",
            "order",
            "service_id",
            "service_name",
            "sort_by",
            "status",
            "workspace_id",
        )
        query_params = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val or str(val) == "0":
                query_params[arg] = val

        data = client.services(**query_params)

        return (
            self.columns,
            (utils.get_item_properties(s, self.columns) for s in data),
        )


class CreateService(command.ShowOne):
    _description = _("Create a ModelArts service")

    def get_parser(self, prog_name):
        parser = super(CreateService, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="<name>",
            help=_(
                "Service name. The value can contain 1 to 64 visible "
                "characters, including Chinese characters. Only letters, "
                "Chinese characters, digits, hyphens (-), and "
                "underscores (_) are allowed."
            ),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            required=False,
            help=_(
                "Service description, which contains a maximum of 100 "
                "characters. By default, this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            required=False,
            help=_(
                "ID of the workspace to which a service belongs. "
                "The default value is 0, indicating the default workspace."
            ),
        )
        parser.add_argument(
            "--infer-type",
            metavar="<infer_type>",
            default="real-time",
            required=True,
            help=_("Inference mode. The value can be real-time, batch."),
        )
        parser.add_argument(
            "--router-id",
            dest="vpc_id",
            required=False,
            help=_(
                "ID of the VPC to which a real-time service instance "
                "is deployed. By default, this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--network-id",
            dest="subnet_network_id",
            required=False,
            help=_(
                "ID of a subnet. By default, this parameter is left "
                "blank. This parameter is mandatory when vpc_id is "
                "configured. Enter the network ID displayed in the "
                "subnet details on the VPC management console "
            ),
        )
        parser.add_argument(
            "--security-group-id",
            metavar="<security_group_id>",
            required=False,
            help=_(
                "A security group is a virtual firewall that provides "
                "secure network access control policies for service "
                "instances. "
            ),
        )
        parser.add_argument(
            "--cluster_id",
            metavar="<cluster_id>",
            required=False,
            help=_(
                "ID of a dedicated cluster. This parameter is left blank "
                "by default, indicating that no dedicated cluster is "
                "used. When using the dedicated cluster to deploy "
                "services, ensure that the cluster status is normal."
            ),
        )
        parser.add_argument(
            "--config",
            metavar="<config>",
            required=True,
            help=_(
                "Model running configuration. If infer_type is batch, "
                "you can configure only one model.  If you upload "
                "multiple models, the first model is used for creating "
                "a service by default. "
            ),
        )
        parser.add_argument(
            "--schedule",
            metavar="<schedule>",
            required=False,
            help=_(
                "Service scheduling configuration, which can be "
                "configured only for real-time services. By default, "
                "this parameter is not used. "
            ),
        )
        parser.add_argument(
            "--model_id", metavar="<model_id>", help=_("Model ID")
        )
        parser.add_argument(
            "--weight",
            metavar="<weight>",
            required=False,
            help=_(
                "Traffic weight allocated to a model. This parameter "
                "is mandatory only when infer_type is set to real-time. "
                "The sum of the weights must be 100."
            ),
        )
        parser.add_argument(
            "--specification",
            metavar="<specification>",
            help=_(
                "Resource specifications. Select specifications based on "
                "service requirements."
            ),
        )
        parser.add_argument(
            "--instance_count",
            metavar="<instance_count>",
            required=False,
            help=_(
                "Number of instances deployed in a model The value must "
                "be greater than 0."
            ),
        )
        parser.add_argument(
            "--type",
            metavar="<type>",
            required=False,
            help=_(
                "Scheduling type. Currently, only the value stop "
                "is supported."
            ),
        )
        parser.add_argument(
            "--time_unit",
            metavar="<time_unit>",
            required=False,
            help=_(
                "Scheduling time unit. Possible values are as follows: "
                "DAYS HOURS MINUTES"
            ),
        )
        parser.add_argument(
            "--duration",
            metavar="<duration>",
            required=False,
            help=_(
                "Value that maps to the time unit. For example, "
                "if the task stops after two hours, set time_unit "
                "to HOURS and duration to 2."
            ),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        attrs = {"service_name": parsed_args.name}

        args_list = (
            "description",
            "infer_type",
            "workspace_id",
            "vpc_id",
            "subnet_network_id",
            "security_group_id",
            "cluster_id",
            "config",
            "schedule",
            "type",
            "time_unit",
            "duration",
            "instance_count",
            "model_id",
            "weight",
            "specification",
        )

        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.create_service(**attrs)
        _formatters = {}
        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns, formatters=_formatters)

        return display_columns, data


class UpdateService(command.Command):
    _description = _("Update Service Configuration")

    def get_parser(self, prog_name):
        parser = super(UpdateService, self).get_parser(prog_name)
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_(
                "Service description, which contains a maximum of 100 "
                "characters. If this parameter is not set, the service "
                "description is not updated."
            ),
        )
        parser.add_argument(
            "--status",
            metavar="<status>",
            help=_(
                "Service status. The value can be running or stopped. "
                "If this parameter is not set, the service status is "
                "not changed."
            ),
        )
        parser.add_argument(
            "--config",
            metavar="<config>",
            help=_(
                "Service configuration. If this parameter is not set, "
                "the service is not updated."
            ),
        )
        parser.add_argument(
            "--schedule",
            metavar="<schedule>",
            help=_(
                "Service scheduling configuration, which can be "
                "configured only for real-time services. By default, "
                "this parameter is not used."
            ),
        )
        parser.add_argument(
            "--additional_properties",
            metavar="<additional_properties>",
            help=_(
                "Additional service attribute, which facilitates service "
                "management."
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        attrs = {}
        if parsed_args.description:
            attrs["description"] = parsed_args.description
        if parsed_args.status:
            attrs["status"] = parsed_args.status
        if parsed_args.config:
            attrs["config"] = parsed_args.config
        if parsed_args.schedule:
            attrs["schedule"] = parsed_args.schedule
        if parsed_args.additional_properties:
            attrs["additional_properties"] = parsed_args.additional_properties
        client.update_config(**attrs)


class ShowService(command.ShowOne):
    _description = _("Show details of a Modelarts serivce")

    def get_parser(self, prog_name):
        parser = super(ShowService, self).get_parser(prog_name)
        parser.add_argument(
            "service",
            metavar="<service>",
            help=_("Service Name or ID"),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        data = client.find_service(parsed_args.service)

        display_columns, columns = _get_columns(data)

        data = utils.get_item_properties(data, columns, formatters=_formatters)
        return (display_columns, data)


class DeleteService(command.Command):
    _description = _("Delete ModelArts Service(s)")

    def get_parser(self, prog_name):
        parser = super(DeleteService, self).get_parser(prog_name)
        parser.add_argument(
            "service",
            metavar="<service>",
            nargs="+",
            help=_("ID or Name of the ModelArts service(s) to be deleted."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        result = 0
        for name_or_id in parsed_args.service:
            try:
                service = client.find_service(name_or_id, ignore_missing=False)
                client.delete_service(service.id)
            except Exception as e:
                result += 1
                LOG.error(
                    _(
                        "Failed to delete service(s) with "
                        "ID or Name '%(service)s': %(e)s"
                    ),
                    {"service": name_or_id, "e": e},
                )
        if result > 0:
            total = len(parsed_args.service)
            msg = _(
                "%(result)s of %(total)s Service(s) failed " "to delete."
            ) % {"result": result, "total": total}
            raise exceptions.CommandError(msg)
