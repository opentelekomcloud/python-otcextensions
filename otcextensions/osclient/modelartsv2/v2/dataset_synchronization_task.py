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
"""ModelArts Dataset Synchronization v2 action implementations"""
import logging

from osc_lib import utils
from osc_lib.command import command
from otcextensions.common import sdk_utils
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _flatten_output(obj):
    data = {
        "status": obj.status,
        "dataset_id": obj.dataset_id,
        "error_code": obj.error_code,
        "error_msg": obj.error_msg,
    }
    return data


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


class SynchronizeDataset(command.Command):
    _description = _("Creating a Dataset Synchronization Task")

    def get_parser(self, prog_name):
        parser = super(SynchronizeDataset, self).get_parser(prog_name)
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            required=True,
            help=_("Dataset ID."),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        attrs = {}

        if parsed_args.dataset_id:
            attrs["dataset_id"] = parsed_args.dataset_id

        client.synchronize_dataset(**attrs)


class ListDatasetSynchronizationTasks(command.Lister):
    _description = _(
        "This API is used to query the execution status "
        "of a dataset synchronization task."
    )
    columns = ("status", "dataset_id", "error_code", "error_msg")

    table_columns = ("status", "dataset_id" "error_code", "error_msg")

    def get_parser(self, prog_name):
        parser = super(ListDatasetSynchronizationTasks, self).get_parser(
            prog_name
        )
        parser.add_argument(
            "--dataset_id",
            metavar="<dataset_id>",
            help=_("ID of the dataset to delete."),
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.modelartsv2

        query = {}
        if parsed_args.dataset_id:
            query["dataset_id"] = parsed_args.dataset_id
        data = client.list_dataset_synchronization_task(**query)

        table = (
            self.columns,
            (
                utils.get_dict_properties(_flatten_output(s), self.columns)
                for s in data
            ),
        )
        return table
