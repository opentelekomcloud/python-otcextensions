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
"""ModelArts model v1 action implementations"""
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import cli_utils
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


_formatters = {
    "input_params": cli_utils.YamlFormat,
    "output_params": cli_utils.YamlFormat,
    "dependencies": cli_utils.YamlFormat,
    "model_metrics": cli_utils.YamlFormat,
    "specification": cli_utils.YamlFormat,
    "apis": cli_utils.YamlFormat,
    "config": cli_utils.YamlFormat,
    "install_type": cli_utils.YamlFormat,
    "created_at": cli_utils.UnixTimestampFormatter,
}


def _get_columns(item):
    column_map = {}
    hidden = ["location"]
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


class DeleteModel(command.Command):
    _description = _("Delete ModelArts Model(s)")

    def get_parser(self, prog_name):
        parser = super(DeleteModel, self).get_parser(prog_name)
        parser.add_argument(
            "model",
            metavar="<model>",
            nargs="+",
            help=_("ID or Name of the ModelArts model(s) to be deleted."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        result = 0
        for name_or_id in parsed_args.model:
            try:
                model = client.find_model(name_or_id, ignore_missing=False)
                client.delete_model(model.id)
            except Exception as e:
                result += 1
                LOG.error(
                    _(
                        "Failed to delete model(s) with "
                        "ID or Name '%(model)s': %(e)s"
                    ),
                    {"model": name_or_id, "e": e},
                )
        if result > 0:
            total = len(parsed_args.model)
            msg = _(
                "%(result)s of %(total)s Model(s) failed " "to delete."
            ) % {"result": result, "total": total}
            raise exceptions.CommandError(msg)


class CreateModel(command.ShowOne):
    _description = _("Create a ModelArts model")

    def get_parser(self, prog_name):
        parser = super(CreateModel, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="<name>",
            help=_(
                "Model name. The value can contain 1 to 64 visible "
                "characters, including Chinese characters. Only letters, "
                "Chinese characters, digits, hyphens (-), and "
                "underscores (_) are allowed."
            ),
        )
        parser.add_argument(
            "--model-version",
            metavar="<model_version>",
            required=True,
            help=_(
                "Model version in the format of Digit.Digit.Digit. "
                "The value range of the digits is [1, 99]. "
                "Note that no part of the version number can start with 0. "
                "For example, 01.01.01 is not allowed."
            ),
        )
        parser.add_argument(
            "--source-location",
            metavar="<source_location>",
            required=True,
            help=_(
                "OBS path where the model is located or the template "
                "address of the SWR image."
            ),
        )
        parser.add_argument(
            "--source-job-id",
            metavar="<source_job_id>",
            help=_(
                "ID of the source training job. If the model is generated "
                "from a training job, input this parameter for source "
                "tracing. If the model is imported from a third-party meta "
                "model, leave this parameter blank. "
                "By default, this parameter is left blank. "
            ),
        )
        parser.add_argument(
            "--source-job-version",
            metavar="<source_job_version>",
            help=_(
                "Version of the source training job. If the model is "
                "generated from a training job, input this parameter "
                "for source tracing. If the model is imported from a "
                "third-party meta model, leave this parameter blank. "
                "By default, this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--source-type",
            metavar="<source_type>",
            help=_(
                "Model source type. Currently, the value can only be "
                "auto, which indicates ExeML models (model download is "
                "not supported). If the model is deployed by a training "
                "job, leave this parameter blank. By default, this "
                "parameter is left blank."
            ),
        )
        parser.add_argument(
            "--model-type",
            metavar="<model_type>",
            required=True,
            help=_(
                "Model type. The value can be TensorFlow, MXNet, Caffe, "
                "Spark_MLlib, Scikit_Learn, XGBoost, Image, or PyTorch, "
                "which is read from the configuration file."
            ),
        )
        parser.add_argument(
            "--runtime",
            metavar="<runtime>",
            help=_(
                "Model running environment. The possible values of "
                "runtime are related to model_type."
            ),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_(
                "Model remarks. The value contains a maximum of 100 "
                "characters and cannot contain the following special "
                "characters and more: &!'\"<>= "
            ),
        )
        parser.add_argument(
            "--execution-code",
            metavar="<execution_code>",
            help=_(
                "OBS path for storing the execution code. By default, "
                "this parameter is left blank. The name of the execution "
                "code file is fixed to customize_service.py. "
            ),
        )
        parser.add_argument(
            "--input-params",
            metavar="<input_params>",
            help=_(
                "Collection of input parameters of a model. By default, "
                "this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--output-params",
            metavar="<output_params>",
            help=_(
                "Collection of output parameters of a model. By default, "
                "this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--dependencies",
            metavar="<dependencies>",
            help=_(
                "Package required for inference code and model. "
                "By default, this parameter is left blank."
            ),
        )
        parser.add_argument(
            "--model-algorithm",
            metavar="<model_algorithm>",
            help=_(
                "Model algorithm. If the algorithm is read from the "
                "configuration file, this parameter can be left blank. "
                "For example, the value can be predict_analysis, "
                "object_detection, or image_classification."
            ),
        )
        parser.add_argument(
            "--model-metrics",
            metavar="<model_metrics>",
            help=_(
                "Model precision, which is read from the "
                "configuration file."
            ),
        )
        parser.add_argument(
            "--apis",
            metavar="<apis>",
            help=_(
                "All apis input and output parameters of the model. "
                "If the parameters are read from the configuration file, "
                "this parameter can be left blank."
            ),
        )
        parser.add_argument(
            "--initial-config",
            metavar="<initial_config>",
            help=_(
                "Character string converted from the final model "
                "configuration file. It is recommended that the "
                "initial_config file be used to provide information "
                "about the fields such as apis, dependencies, "
                "input_params, and output_params."
            ),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_("Workspace ID. Default value: 0"),
        )
        parser.add_argument(
            "--model-docs",
            metavar="<model_docs>",
            help=_(
                "List of model description documents. A maximum of three "
                "documents are supported."
            ),
        )
        parser.add_argument(
            "--install-type",
            metavar="<install_type>",
            help=_(
                "Deployment type. Only lowercase letters are supported. "
                "The value can be real-time, or batch. "
                'Default value: ["real-time","batch"]'
            ),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        attrs = {"model_name": parsed_args.name}

        args_list = (
            "model_version",
            "source_location",
            "source_job_id",
            "source_job_version",
            "source_type",
            "model_type",
            "runtime",
            "description",
            "execution_code",
            "input_params",
            "output_params",
            "dependencies",
            "model_algorithm",
            "model_metrics",
            "apis",
            "initial_config",
            "workspace_id",
            "model_docs",
            "install_type",
        )
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                attrs[arg] = val

        data = client.create_model(**attrs)
        display_columns, columns = _get_columns(data)
        data = utils.get_item_properties(data, columns, formatters=_formatters)

        return display_columns, data


class ShowModel(command.ShowOne):
    _description = _("Show details of a modelartsv1 model")

    def get_parser(self, prog_name):
        parser = super(ShowModel, self).get_parser(prog_name)
        parser.add_argument(
            "model", metavar="<model>", help=_("Enter model id or name")
        )
        return parser

    @translate_response
    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        data = client.find_model(parsed_args.model)
        if not data.image_address:
            data = client.get_model(data.id)
        return data


class ListModels(command.Lister):
    _description = _("List models")
    columns = ("Id", "Name", "Version", "Model Size")

    def get_parser(self, prog_name):
        parser = super(ListModels, self).get_parser(prog_name)
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help=_(
                "Maximum number of records returned on each page. "
                "The default value is 100. The recommended value ranges "
                "from 10 to 50."
            ),
        )
        parser.add_argument(
            "--offset",
            metavar="<offset>",
            type=int,
            help=_("Index of the page to be queried. Default value: 0."),
        )
        parser.add_argument(
            "--order",
            metavar="<order>",
            help=_(
                "Sorting order. The value can be asc or desc, "
                "indicating ascending or descending order. "
                "Default value: desc"
            ),
        )
        parser.add_argument(
            "--workspace-id",
            metavar="<workspace_id>",
            help=_(
                "ID of the workspace to which a service belongs. The "
                "default value is 0, indicating the default workspace."
            ),
        )
        parser.add_argument(
            "--sort-by",
            metavar="<sort_by>",
            help=_(
                "Sorting mode. The value can be create_at, model_"
                "version, or model_size. Default value: create_at."
            ),
        )
        parser.add_argument(
            "--name",
            metavar="<name>",
            help=_("Model name. Fuzzy match is supported."),
        )
        parser.add_argument(
            "--model-version",
            metavar="<model_version>",
            help=_("Model version."),
        )
        parser.add_argument(
            "--status", metavar="<status>", help=_("Model status.")
        )
        parser.add_argument(
            "--model-type",
            metavar="<model_type>",
            help=_(
                "Model type. The models of this type are queried. "
                "model_type and not_model_type are mutually exclusive "
                "and cannot co-exist."
            ),
        )
        parser.add_argument(
            "--not-model-type",
            metavar="<not_model_type>",
            help=_(
                "Model type. A list of models of types except "
                "for this type are queried."
            ),
        )
        parser.add_argument(
            "--description",
            metavar="<description>",
            help=_("Description. Fuzzy match is supported."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv1
        args_list = (
            "name",
            "model_version",
            "status",
            "model_type",
            "not_model_type",
            "description",
            "offset",
            "limit",
            "sort_by",
            "order",
            "workspace_id",
        )
        query_params = {}
        for arg in args_list:
            val = getattr(parsed_args, arg)
            if val:
                query_params[arg] = val

        data = client.models(**query_params)

        table = (
            self.columns,
            (utils.get_dict_properties(s, self.columns) for s in data),
        )
        return table
