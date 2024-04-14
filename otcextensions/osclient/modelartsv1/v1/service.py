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
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

INFER_TYPE_CHOICES = ["real-time", "batch"]

SORT_BY_CHOICES = ["publish_at", "service_name"]

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


class ListServices(command.Lister):
    _description = _("Get properties of a service")
    columns = (
        "Service Id",
        "Service Name",
        "Infer Type",
        "Status",
    )

    def get_parser(self, prog_name):
        parser = super(ListServices, self).get_parser(prog_name)
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
            metavar="{asc, desc}",
            type=lambda s: s.lower(),
            choices=["asc", "desc"],
            help=_("Sorting order. Default value: desc"),
        )
        parser.add_argument(
            "--service-id",
            metavar="<service_id>",
            help=_("Service ID."),
        )
        parser.add_argument(
            "--name",
            metavar="<name>",
            help=_("Service Name."),
        )
        parser.add_argument(
            "--sort-by",
            metavar="{publish_at, service_name}",
            type=lambda s: s.lower(),
            choices=["publish_at", "service_name"],
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
            "name",
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
                "Service name. Enter 1 to 64 characters. Only letters, "
                "digits, hyphens (-), and underscores (_) are allowed."
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
            "--infer-type",
            metavar="{" + ",".join(INFER_TYPE_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=INFER_TYPE_CHOICES,
            required=True,
            help=_("Inference mode."),
        )

        network_group = parser.add_argument_group("network arguments")
        parser._action_groups.insert(2, parser._action_groups.pop())
        network_group.add_argument(
            "--router-id",
            metavar="<router_id>",
            dest="vpc_id",
            help=_(
                "ID of the VPC to which a real-time service instance "
                "is deployed. By default, this parameter is left blank."
            ),
        )
        network_group.add_argument(
            "--network-id",
            metavar="<network_id>",
            dest="subnet_network_id",
            help=_(
                "ID of a subnet. By default, this parameter is left "
                "blank. This parameter is mandatory when vpc_id is "
                "configured. Enter the network ID displayed in the "
                "subnet details on the VPC management console "
            ),
        )
        network_group.add_argument(
            "--security-group-id",
            metavar="<security_group_id>",
            help=_(
                "A security group is a virtual firewall that provides "
                "secure network access control policies for service "
                "instances. "
            ),
        )
        parser.add_argument(
            "--cluster-id",
            metavar="<cluster_id>",
            required=False,
            help=_(
                "ID of a dedicated resource pool. If this parameter "
                "is set --router-id doesnt take effect."
            ),
        )
        parser.add_argument(
            "--schedule",
            metavar="type=<type>,time_unit=<time_unit>,duration=<duration>",
            required_keys=["type", "time_unit", "duration"],
            dest="schedule",
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Service scheduling configuration, which can be "
                "configured only for real-time services."
            ),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_("Workspace ID."),
        )

        config_group = parser.add_argument_group("config arguments")
        parser._action_groups.insert(3, parser._action_groups.pop())
        config_group.add_argument(
            "--model-id",
            metavar="<model_id>",
            required=True,
            help=_("Model ID"),
        )
        config_group.add_argument(
            "--weight",
            metavar="<weight>",
            type=int,
            help=_(
                "Traffic weight allocated to a model. This parameter "
                "is mandatory only when infer_type is set to real-time. "
                "The sum of the weights must be 100."
            ),
        )
        config_group.add_argument(
            "--specification",
            metavar="<specification>",
            required=True,
            help=_(
                "Resource specifications. Select specifications based on "
                "service requirements."
            ),
        )
        config_group.add_argument(
            "--instance-count",
            metavar="<instance_count>",
            required=True,
            type=int,
            help=_(
                "Number of instances deployed in a model The value must "
                "be greater than 0."
            ),
        )
        config_group.add_argument(
            "--env",
            metavar="<key=value>",
            action=parseractions.KeyValueAction,
            dest="envs",
            help=_(
                "Environment variable key-value pair required "
                "for running a model.\n"
                "Example: --env VAR1=value1 --env VAR2=value2"
            ),
        )
        config_group.add_argument(
            "--custom-spec",
            metavar="cpu=<cpu>,memory=<memory>,gpu_p4=<gpu_p4>",
            required_keys=["cpu", "memory"],
            optional_keys=["gpu_p4"],
            dest="custom_spec",
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Custom specifications. Set this parameter when "
                "you use a dedicated resource pool."
            ),
        )
        config_group.add_argument(
            "--src-type",
            metavar="<src_type>",
            help=_("Data source type."),
        )
        config_group.add_argument(
            "--src-path",
            metavar="<src_path>",
            help=_("OBS path of the input data of a batch job."),
        )
        config_group.add_argument(
            "--dest-path",
            metavar="<dest_path>",
            help=_("OBS path of the output data of a batch job."),
        )
        config_group.add_argument(
            "--req-uri",
            metavar="<dest_path>",
            help=_(
                "API URI from the model config.json file for inference. "
                "If a ModelArts built-in inference image is used, the "
                "value of this parameter is /"
            ),
        )
        config_group.add_argument(
            "--mapping-type",
            metavar="{file, csv}",
            type=lambda s: s.lower(),
            choices=["file", "csv"],
            help=_("Mapping type of the input data."),
        )
        config_group.add_argument(
            "--mapping-rule",
            metavar="<mapping_rule>",
            help=_(
                "Mapping between input parameters and CSV data. This "
                "parameter is mandatory only when mapping_type is set to csv."
            ),
        )
        parser.add_argument(
            "--wait",
            action="store_true",
            help=("Wait for service deployment."),
        )
        parser.add_argument(
            "--timeout",
            metavar="<timeout>",
            type=int,
            default=1200,
            help=_("Timeout for the wait in seconds (default 1200 seconds)."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        attrs = {
            "service_name": parsed_args.name,
            "infer_type": parsed_args.infer_type,
            "config": [
                {
                    "model_id": parsed_args.model_id,
                    "specification": parsed_args.specification,
                    "instance_count": parsed_args.instance_count,
                }
            ],
        }
        args_list = (
            "description",
            "workspace_id",
            "vpc_id",
            "subnet_network_id",
            "security_group_id",
            "cluster_id",
            "schedule",
        )
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        if parsed_args.envs:
            attrs["config"][0].update(envs=parsed_args.envs)

        if parsed_args.infer_type == "batch":
            for arg in ("src_path", "dest_path", "req_uri", "mapping_type"):
                val = getattr(parsed_args, arg)
                if val:
                    attrs["config"][0][arg] = val
                else:
                    raise exceptions.CommandError(
                        f"For batch infer_type --{arg.replace('_', '-')} "
                        "argument is required."
                    )
            if parsed_args.mapping_rule:
                attrs["config"][0]["mapping_rule"] = parsed_args.mapping_rule
            if parsed_args.src_type:
                attrs["config"][0]["src_type"] = parsed_args.src_type
            custom_spec = parsed_args.custom_spec
            if custom_spec:
                if len(custom_spec) > 1:
                    msg = "--custom-spec argument cannot be repeated"
                    raise exceptions.CommandError(msg)
                else:
                    custom_spec = custom_spec[0]
                    for key, val in custom_spec.items():
                        if key == "memory":
                            custom_spec[key] = int(val)
                        else:
                            custom_spec[key] = float(val)
                    attrs["config"][0].update(custom_spec=custom_spec)

        elif parsed_args.infer_type == "real-time":
            if parsed_args.weight:
                attrs["config"][0]["weight"] = parsed_args.weight
            else:
                raise exceptions.CommandError(
                    "For real-time infer_type --weight argument is required."
                )

        service = client.create_service(**attrs)
        if parsed_args.wait:
            client.wait_for_service(service.id, parsed_args.timeout)

        data = client.get_service(service.id)
        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns, formatters=_formatters)

        return display_columns, data


class UpdateService(command.ShowOne):
    _description = _("Update Service Configuration")

    def get_parser(self, prog_name):
        parser = super(UpdateService, self).get_parser(prog_name)
        parser.add_argument(
            "service",
            metavar="<service>",
            help=_("Service Name or ID"),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_("Service description (max 100 characters)."),
        )
        parser.add_argument(
            "--schedule",
            metavar="type=<type>,time_unit=<time_unit>,duration=<duration>",
            required_keys=["type", "time_unit", "duration"],
            dest="schedule",
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Service scheduling configuration, which can be "
                "configured only for real-time services."
            ),
        )
        parser.add_argument(
            "--additional-property",
            metavar="<key=value>",
            action=parseractions.KeyValueAction,
            dest="additional_properties",
            help=_(
                ".Additional service attribute, which facilitates service "
                "management\n"
                "Example: --additional-property VAR1=value1 "
                "--additional-property VAR2=value2"
            ),
        )

        config_group = parser.add_argument_group("config arguments")
        parser._action_groups.insert(2, parser._action_groups.pop())
        config_group.add_argument(
            "--model-id",
            metavar="<model_id>",
            help=_("Model ID"),
        )
        config_group.add_argument(
            "--weight",
            metavar="<weight>",
            type=int,
            help=_(
                "Traffic weight allocated to a model. This parameter "
                "is mandatory only when infer_type is set to real-time. "
                "The sum of the weights must be 100."
            ),
        )
        parser.add_argument(
            "--cluster-id",
            metavar="<cluster_id>",
            help=_(
                "ID of a dedicated resource pool. By default, this parameter "
                "is left blank, indicating that no dedicated resource "
                "pool is used."
            ),
        )
        config_group.add_argument(
            "--specification",
            metavar="<specification>",
            help=_(
                "Resource specifications. Select specifications based on "
                "service requirements."
            ),
        )
        config_group.add_argument(
            "--instance-count",
            metavar="<instance_count>",
            type=int,
            help=_(
                "Number of instances deployed in a model The value must "
                "be greater than 0."
            ),
        )
        config_group.add_argument(
            "--env",
            metavar="<key=value>",
            action=parseractions.KeyValueAction,
            dest="envs",
            help=_(
                "Environment variable key-value pair required "
                "for running a model.\n"
                "Example: --env VAR1=value1 --env VAR2=value2"
            ),
        )
        config_group.add_argument(
            "--custom-spec",
            metavar="cpu=<cpu>,memory=<memory>,gpu_p4=<gpu_p4>",
            required_keys=["cpu", "memory"],
            dest="custom_spec",
            action=parseractions.MultiKeyValueAction,
            help=_(
                "Custom specifications. Set this parameter when "
                "you use a dedicated resource pool."
            ),
        )
        config_group.add_argument(
            "--src-type",
            metavar="<src_type>",
            help=_("Data source type."),
        )
        config_group.add_argument(
            "--src-path",
            metavar="<src_path>",
            help=_("OBS path of the input data of a batch job."),
        )
        config_group.add_argument(
            "--dest-path",
            metavar="<dest_path>",
            help=_("OBS path of the output data of a batch job."),
        )
        config_group.add_argument(
            "--req-uri",
            metavar="<dest_path>",
            help=_(
                "API URI from the model config.json file for inference. "
                "If a ModelArts built-in inference image is used, the "
                "value of this parameter is /"
            ),
        )
        config_group.add_argument(
            "--mapping-type",
            metavar="{file, csv}",
            type=lambda s: s.lower(),
            choices=["file", "csv"],
            help=_("Mapping type of the input data."),
        )
        config_group.add_argument(
            "--mapping-rule",
            metavar="<mapping_rule>",
            help=_(
                "Mapping between input parameters and CSV data. This "
                "parameter is mandatory only when mapping_type is set to csv."
            ),
        )

        parser.add_argument(
            "--wait",
            action="store_true",
            help=("Wait for service deployment."),
        )
        parser.add_argument(
            "--timeout",
            metavar="<timeout>",
            type=int,
            default=1200,
            help=_("Timeout for the wait in seconds (default 1200 seconds)."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        config = {}
        for arg in ("model_id", "specification", "instance_count", "envs"):
            val = getattr(parsed_args, arg)
            if val:
                config[arg] = val

        service = client.find_service(
            parsed_args.service, ignore_missing=False
        )
        if service.infer_type == "real-time":
            for arg in ("weight", "cluster_id"):
                val = getattr(parsed_args, arg)
                if val:
                    config[arg] = val

            custom_spec = parsed_args.custom_spec
            if custom_spec:
                if len(custom_spec) > 1:
                    msg = "--custom-spec argument cannot be repeated"
                    raise exceptions.CommandError(msg)
                else:
                    custom_spec = custom_spec[0]
                    for key, val in custom_spec.items():
                        if key == "memory":
                            custom_spec[key] = int(val)
                        else:
                            custom_spec[key] = float(val)
                    config.update(custom_spec=custom_spec)

        elif service.infer_type == "batch":
            for arg in (
                "src_path",
                "dest_path",
                "req_uri",
                "mapping_type",
                "mapping_value",
            ):
                val = getattr(parsed_args, arg)
                if val:
                    config[arg] = val

        attrs = {}
        for arg in ("description", "schedule", "additional_properties"):
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        attrs.update(config=[config])

        client.update_service(service.id, **attrs)
        if parsed_args.wait:
            client.wait_for_service(service.id, parsed_args.timeout)

        data = client.get_service(service.id)
        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns, formatters=_formatters)

        return display_columns, data


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

        service = client.find_service(
            parsed_args.service, ignore_missing=False
        )
        data = client.get_service(service.id)

        display_columns, columns = _get_columns(data)

        data = utils.get_item_properties(data, columns, formatters=_formatters)
        return (display_columns, data)


class StartService(command.Command):
    _description = _("Start a Service.")

    def get_parser(self, prog_name):
        parser = super(StartService, self).get_parser(prog_name)
        parser.add_argument(
            "service",
            metavar="<service>",
            help=_("Service name or ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        obj = client.find_service(parsed_args.service, ignore_missing=False)
        client.start_service(obj)


class StopService(command.Command):
    _description = _("Stop a Service.")

    def get_parser(self, prog_name):
        parser = super(StopService, self).get_parser(prog_name)
        parser.add_argument(
            "service",
            metavar="<service>",
            help=_("Service name or ID."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        obj = client.find_service(parsed_args.service, ignore_missing=False)
        client.stop_service(obj)


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
            ) % {
                "result": result,
                "total": total,
            }
            raise exceptions.CommandError(msg)
