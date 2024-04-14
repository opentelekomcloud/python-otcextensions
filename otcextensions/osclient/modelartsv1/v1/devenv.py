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
"""ModelArts devenv v1 action implementations"""
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

SORT_ORDER_CHOICES = ["asc", "desc"]

STATUS_CHOICES = [
    "CREATING",
    "CREATE_FAILED",
    "STARTING",
    "RESTARTING",
    "START_FAILED",
    "RUNNING",
    "STOPPING",
    "STOPPED",
    "UNAVAILABLE",
    "DELETED",
    "RESIZING",
    "RESIZE_FAILED",
]

DEVENV_PROFILE_ID_MAP = {
    1: "Multi-Engine 1.0 (python3)-cpu",
    2: "Multi-Engine 1.0 (python3)-gpu",
    3: "Multi-Engine 2.0 (python3)",
}

_formatters = {
    "auto_stop": cli_utils.YamlFormat,
    "created_at": cli_utils.UnixTimestampFormatter,
    "flavor_details": cli_utils.YamlFormat,
    "profile": cli_utils.YamlFormat,
    "spec": cli_utils.YamlFormat,
    "updated_at": cli_utils.UnixTimestampFormatter,
    "user": cli_utils.YamlFormat,
}

AUTO_STOP_CHOICES = (
    "enable",
    "disable",
)


def _get_columns(item):
    column_map = {}
    hidden = ["location", "workspace", "ai_project"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden
    )


def translate_response(func):
    def new(self, *args, **kwargs):
        obj = func(self, *args, **kwargs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    new.__name__ = func.__name__
    new.__doc__ = func.__doc__
    return new


class ListDevenvInstances(command.Lister):
    _description = _("List Devenv Instances.")
    columns = (
        "ID",
        "Name",
        "status",
        "Created At",
    )

    def get_parser(self, prog_name):
        parser = super(ListDevenvInstances, self).get_parser(prog_name)
        parser.add_argument(
            "--de-type",
            metavar="<de_type>",
            default="Notebook",
            help=_(
                "Development environment type. Only Notebook is supported. "
                "The first letter must be capitalized."
            ),
        )
        parser.add_argument(
            "--provision-type",
            dest="provision_type",
            help=_("Deployment type. Only Docker is supported."),
        )
        parser.add_argument(
            "--status",
            metavar="<status>",
            type=lambda s: s.upper(),
            choices=STATUS_CHOICES,
            help=_("Filter Devenv Instances by status."),
        )
        parser.add_argument(
            "--sort-by",
            metavar="<sort_by>",
            dest="sortby",
            type=lambda s: s.lower(),
            choices=["name", "creation_timestamp"],
            help=_(
                "Classification standard. The value can be name "
                "or creation_timestamp. By default list is sorted by name."
            ),
        )
        parser.add_argument(
            "--order",
            metavar="{" + ",".join(SORT_ORDER_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=SORT_ORDER_CHOICES,
            help=_("Sorting order. Default value: asc"),
        )
        parser.add_argument(
            "--offset",
            metavar="<offset>",
            type=int,
            help=_("Start index. The default value is 0."),
        )
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_("Number of returned result records."),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_(
                "Workspace ID. If no workspace is created, "
                "the default value is 0."
            ),
        )
        parser.add_argument(
            "--ai-project-id",
            metavar="<ai_project_id>",
            dest="ai_project",
            help=_("AI project ID."),
        )
        parser.add_argument(
            "--pool-id",
            metavar="<pool_id>",
            help=_("ID of a dedicated resource pool."),
        )
        parser.add_argument(
            "--show-self",
            action="store_true",
            help=("Only the current user's instanaces will be listed."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        args_list = (
            "de_type",
            "provision_type",
            "status",
            "sortby",
            "order",
            "offset",
            "limit",
            "workspace_id",
            "show_self",
            "ai_project",
            "pool_id",
        )
        query_params = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                query_params[arg] = val

        data = client.devenv_instances(**query_params)

        formatters = {
            "Created At": cli_utils.UnixTimestampFormatter,
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


class ShowDevenvInstance(command.ShowOne):
    _description = _("Show details of a Devenv Instance.")

    def get_parser(self, prog_name):
        parser = super(ShowDevenvInstance, self).get_parser(prog_name)
        parser.add_argument(
            "instance",
            metavar="<instance>",
            help=_("Devenv Instance ID."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        return client.find_devenv_instance(
            parsed_args.instance, ignore_missing=False
        )


class CreateDevenvInstance(command.ShowOne):
    _description = _("Create a Devenv Instance.")

    def get_parser(self, prog_name):
        parser = super(CreateDevenvInstance, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="<name>",
            help=_(
                "Instance name (max 64 characters). The value can contain "
                "letters, digits, hyphens (-), and underscores (_)."
            ),
        )
        parser.add_argument(
            "--profile-id",
            metavar="<profile_id>",
            choices=list(DEVENV_PROFILE_ID_MAP.keys()),
            required=True,
            type=int,
            help=_(
                "Configuration ID. The options are as follows:\n"
                + "\n".join(
                    [
                        f"{key}: {value}"
                        for key, value in DEVENV_PROFILE_ID_MAP.items()
                    ]
                )
            ),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_("Instance description (max 512 characters.)"),
        )
        parser.add_argument(
            "--flavor",
            metavar="<flavor>",
            required=True,
            help=_("Instance flavor."),
        )
        parser.add_argument(
            "--ai-project-id",
            metavar="<ai_project_id>",
            help=_("AI project ID. This parameter is reserved."),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_("Workspace. The default workspace ID is 0."),
        )

        parser.add_argument(
            "--storage-type",
            metavar="<storage_type>",
            required=True,
            help=_("Storage type. Only `obs` is supported."),
        )
        parser.add_argument(
            "--storage-path",
            metavar="<storage_path>",
            required=True,
            help=_(
                "The value must be a valid OBS bucket path and end with "
                "a slash (/).\nThe value must be a specific directory in "
                "an OBS bucket rather than the root directory of an OBS "
                "bucket."
            ),
        )

        extended_storage_group = parser.add_argument_group(
            "Extended Storage Parameters",
            description=_(
                "Extended storage supports only obs fs and is "
                "available only for certain dedicated resource "
                "pools."
            ),
        )
        parser._action_groups.insert(2, parser._action_groups.pop())
        extended_storage_group.add_argument(
            "--extended-storage-type",
            metavar="<extended_storage_type>",
            help=_("Storage type. Only `obs` is supported."),
        )
        extended_storage_group.add_argument(
            "--extended-storage-path",
            metavar="<extended_storage_path>",
            help=_(
                "If extended_storage_type is set to obs, this parameter is "
                "mandatory.\nThe value must be a valid OBS bucket path "
                "and end with a slash (/).\nThe value must be a specific "
                "directory in an OBS bucket rather than the root directory "
                "of an OBS bucket."
            ),
        )

        autostop_group = parser.add_argument_group("AutoStop Parameters")
        parser._action_groups.insert(3, parser._action_groups.pop())
        autostop_group.add_argument(
            "--autostop-duration",
            metavar="<autostop_duration>",
            type=int,
            help=_(
                "Running duration, in seconds. The value ranges from "
                "3600 to 86400.\nThe instance will automatically stop "
                "when the running duration is reached.\nAfter this "
                "parameter is set, it is valid for each startup."
            ),
        )
        autostop_group.add_argument(
            "--autostop-prompt",
            metavar="<autostop_prompt>",
            type=bool,
            help=_(
                "Whether to display a prompt again.\nThis parameter is "
                "provided for the console to determine whether to display "
                "a prompt again.\nThe default value is true."
            ),
        )

        pool_group = parser.add_argument_group("Resource pool Parameters")
        parser._action_groups.insert(4, parser._action_groups.pop())
        pool_group.add_argument(
            "--pool-id",
            metavar="<pool_id>",
            help=_("Resource pool ID."),
        )
        pool_group.add_argument(
            "--pool-type",
            metavar="<pool_type>",
            help=_("Resource pool Type."),
        )
        pool_group.add_argument(
            "--pool-name",
            metavar="<pool_name>",
            help=_("Resource pool Name."),
        )

        parser.add_argument(
            "--annotation",
            metavar="<annotation>",
            action=parseractions.KeyValueAction,
            help=_(
                "Custom data to be passed as Map<String:String>.\nData may "
                "be passed as <key>=<value> or JSON.\n"
                "(repeat option to set multiple annotations)"
            ),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        profile_id = DEVENV_PROFILE_ID_MAP[parsed_args.profile_id]

        attrs = {
            "name": parsed_args.name,
            "flavor": parsed_args.flavor,
            "profile_id": profile_id,
            "spec": {
                "storage": {
                    "location": {"path": parsed_args.storage_path},
                    "type": parsed_args.storage_type,
                }
            },
        }
        if parsed_args.description:
            attrs["description"] = parsed_args.description

        if parsed_args.autostop_duration:
            attrs["spec"]["auto_stop"] = {
                "enable": True,
                "duration": parsed_args.autostop_duration,
            }
            if parsed_args.autostop_prompt:
                attrs["auto_stop"]["spec"]["auto_stop"].update(
                    {"prompt": parsed_args.autostop_prompt}
                )

        if parsed_args.workspace_id:
            attrs["workspace"] = {"id": parsed_args.workspace_id}
        if parsed_args.ai_project_id:
            attrs["ai_project"] = {"id": parsed_args.ai_project_id}

        if bool(parsed_args.extended_storage_type) ^ bool(
            parsed_args.extended_storage_path
        ):
            raise exceptions.CommandError(
                "--extended-storage-type and --extended-storage-path "
                "must be given together."
            )

        if parsed_args.extended_storage_path:
            attrs["spec"]["extended_storage"] = {
                "location": {"path": parsed_args.extended_storage_path},
                "type": parsed_args.extended_storage_type,
            }

        if parsed_args.pool_id:
            attrs["pool"] = {"id": parsed_args.pool_id}
            if parsed_args.pool_type:
                attrs["pool"] = {"type": parsed_args.pool_type}
            if parsed_args.pool_name:
                attrs["pool"] = {"name": parsed_args.pool_name}

        if parsed_args.annotation:
            attrs["annotations"] = parsed_args.annotation

        return client.create_devenv_instance(**attrs)


class StartDevenvInstance(command.ShowOne):
    _description = _("Start a Devenv Instance.")

    def get_parser(self, prog_name):
        parser = super(StartDevenvInstance, self).get_parser(prog_name)
        parser.add_argument(
            "instance",
            metavar="<instance>",
            help=_("Devenv Instance name or ID."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        instance = client.find_devenv_instance(
            parsed_args.instance, ignore_missing=False
        )
        return client.start_devenv_instance(instance.id)


class StopDevenvInstance(command.ShowOne):
    _description = _("Start a Devenv Instance.")

    def get_parser(self, prog_name):
        parser = super(StopDevenvInstance, self).get_parser(prog_name)
        parser.add_argument(
            "instance",
            metavar="<instance>",
            help=_("Devenv Instance name or ID."),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1

        instance = client.find_devenv_instance(
            parsed_args.instance, ignore_missing=False
        )
        return client.stop_devenv_instance(instance.id)


class UpdateDevenvInstance(command.ShowOne):
    _description = _("Update Devenv Description")

    def get_parser(self, prog_name):
        parser = super(UpdateDevenvInstance, self).get_parser(prog_name)
        parser.add_argument(
            "instance",
            metavar="<instance>",
            help=_("Devenv Instance ID."),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_(
                "Additional service attribute, which facilitates service "
                "management."
            ),
        )
        parser.add_argument(
            "--auto-stop",
            metavar="{" + ",".join(AUTO_STOP_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=AUTO_STOP_CHOICES,
            help=_("Whether to enable or disable the auto stop function."),
        )
        parser.add_argument(
            "--duration",
            metavar="<duration>",
            type=int,
            help=_(
                "Running duration, in seconds. The value ranges from "
                "3,600 to 86,400. This parameter is mandatory when "
                "auto_stop is enabled."
            ),
        )
        parser.add_argument(
            "--prompt",
            metavar="{" + ",".join(AUTO_STOP_CHOICES) + "}",
            type=lambda s: s.lower(),
            choices=AUTO_STOP_CHOICES,
            help=_(
                "Whether to disable a display prompt again for auto_stop. "
                "This parameter is provided for the console to determine "
                "whether to display a prompt again."
            ),
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        attrs = {"auto_stop": {}}
        auto_stop = parsed_args.auto_stop
        prompt = parsed_args.prompt

        if auto_stop:
            if auto_stop == "enable":
                attrs["auto_stop"].update(enable=True)
                if not parsed_args.duration:
                    raise exceptions.CommandError(
                        "--duration is mandatory when --auto-stop is set."
                    )
            elif auto_stop == "disable":
                attrs["auto_stop"].update(enable=False)

        if prompt:
            if prompt == "enable":
                attrs["auto_stop"].update(prompt=True)
            elif prompt == "disable":
                attrs["auto_stop"].update(prompt=False)

        if parsed_args.duration:
            attrs["auto_stop"].update(duration=parsed_args.duration)

        if parsed_args.description:
            attrs.update(description=parsed_args.description)

        if not attrs["auto_stop"]:
            del attrs["auto_stop"]
        return client.update_devenv_instance(parsed_args.instance, **attrs)


class DeleteDevenvInstance(command.Command):
    _description = _("Delete Devenv Instance(s)")

    def get_parser(self, prog_name):
        parser = super(DeleteDevenvInstance, self).get_parser(prog_name)
        parser.add_argument(
            "instance",
            metavar="<instance>",
            nargs="+",
            help=_("ID or Name of the Devenv Instance(s) to be deleted."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        result = 0
        for name_or_id in parsed_args.instance:
            try:
                instance = client.find_devenv_instance(
                    name_or_id, ignore_missing=False
                )
                client.delete_devenv_instance(instance.id)
            except Exception as e:
                result += 1
                LOG.error(
                    _(
                        "Failed to delete Devenv Instance(s) with "
                        "ID or Name '%(instance)s': %(e)s"
                    ),
                    {"instance": name_or_id, "e": e},
                )
        if result > 0:
            total = len(parsed_args.instance)
            msg = _(
                "%(result)s of %(total)s Devenv Instance(s) failed "
                "to delete."
            ) % {"result": result, "total": total}
            raise exceptions.CommandError(msg)
