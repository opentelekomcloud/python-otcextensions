# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
"""Configuration v3 action implementations"""

from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils


DATASTORE_TYPE_CHOICES = ['mysql', 'postgresql', 'sqlserver']


_formatters = {
}


def _get_columns(item, skip_values=True):
    column_map = {}
    hidden = ['location', 'links']
    if skip_values:
        hidden.append('configuration_parameters')
        hidden.append('values')

    return sdk_utils.get_osc_show_columns_for_sdk_resource(
        item, column_map, hidden)


class ListConfigurations(command.Lister):
    _description = _("List Configurations")
    column_headers = [
        'ID', 'Name', 'Description', 'Datastore Name',
        'Datastore Version Name', 'User Defined'
    ]

    columns = [
        'id', 'name', 'description', 'datastore_name',
        'datastore_version_name', 'is_user_defined'
    ]

    def get_parser(self, prog_name):
        parser = super(ListConfigurations, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.configurations()

        return (self.column_headers, (utils.get_item_properties(
            s,
            self.columns,
        ) for s in data))


class ShowConfiguration(command.ShowOne):
    _description = _("Show details of a database configuration")

    def get_parser(self, prog_name):
        parser = super(ShowConfiguration, self).get_parser(prog_name)
        parser.add_argument('configuration',
                            metavar="<configuration>",
                            help=_("ID or name of the configuration"))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        obj = client.find_configuration(parsed_args.configuration,
                                        ignore_missing=False)

        display_columns, columns = _get_columns(obj, skip_values=True)
        data = utils.get_item_properties(obj, columns,
                                         formatters=_formatters)

        return (display_columns, data)


class ListConfigurationParameters(command.Lister):
    _description = _("List Configuration parameters")
    column_headers = (
        'Name', 'Value', 'Type', 'Description',
        'Restart Required', 'Readonly', 'Value Range'
    )
    columns = (
        'name', 'value', 'type', 'description',
        'restart_required', 'readonly', 'value_range'
    )

    def get_parser(self, prog_name):
        parser = super(ListConfigurationParameters, self).get_parser(prog_name)
        parser.add_argument('configuration',
                            metavar="<configuration>",
                            help=_("ID or name of the configuration"))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.find_configuration(
            parsed_args.configuration,
            ignore_missing=False).configuration_parameters

        return (self.column_headers, (utils.get_dict_properties(
            s,
            self.columns,
        ) for s in data))


class CreateConfiguration(command.ShowOne):
    _description = _("Create new Configuration")

    def get_parser(self, prog_name):
        parser = super(CreateConfiguration, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar="<name>",
            help=_("Parameter group name"))
        parser.add_argument(
            '--description',
            metavar="<description>",
            help=_("Parameter group description"))
        parser.add_argument(
            '--datastore_type',
            metavar='{' + ','.join(DATASTORE_TYPE_CHOICES) + '}',
            choices=DATASTORE_TYPE_CHOICES,
            type=lambda s: s.lower(),
            required=True,
            help=_("Datastore type"))
        parser.add_argument(
            '--datastore_version',
            metavar="<datastore_version>",
            required=True,
            help=_("Datastore version"))
        parser.add_argument(
            '--value',
            dest='values',
            metavar="<key=value>",
            action=parseractions.KeyValueAction,
            help=_("Configuration value"
                   "(repeat option to set multiple values)")
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        config_attrs = {}
        config_attrs['datastore'] = {}
        if parsed_args.name:
            config_attrs['name'] = parsed_args.name
        if parsed_args.description:
            config_attrs['description'] = parsed_args.description
        if parsed_args.datastore_type and parsed_args.datastore_version:
            config_attrs['datastore'] = {
                'type': parsed_args.datastore_type,
                'version': parsed_args.datastore_version
            }

        if parsed_args.values:
            config_attrs['values'] = parsed_args.values
        obj = client.create_configuration(**config_attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class ApplyConfiguration(command.Command):
    _description = _("Apply Configuration to the instance(s)")

    columns = ('id', 'name', 'description', 'datastore_version_id',
               'datastore_version_name', 'datastore_name', 'created',
               'updated', 'allowed_updated', 'instance_count', 'values')

    def get_parser(self, prog_name):
        parser = super(ApplyConfiguration, self).get_parser(prog_name)
        parser.add_argument(
            'configuration',
            metavar="<configuration>",
            help=_("Configuration name or id")
        )
        parser.add_argument(
            '--instance',
            metavar="<instance_id>",
            dest='instances',
            action='append',
            help=_('ID of the instance the configuration '
                   'should be applied to. '
                   '(repeat option to apply to multiple instances).')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        config = client.find_configuration(parsed_args.configuration,
                                           ignore_missing=False)

        inst_ids = []

        # Ensure instance_ids are right
        for inst in parsed_args.instances:
            inst_ids.append(client.get_instance(inst).id)

        obj = client.apply_configuration(config.id, instances=inst_ids)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class SetConfiguration(command.Command):
    _description = _("Set values of the Configuration")

    columns = ('id', 'name', 'description', 'datastore_version_id',
               'datastore_version_name', 'datastore_name', 'created',
               'updated', 'allowed_updated', 'instance_count', 'values')

    def get_parser(self, prog_name):
        parser = super(SetConfiguration, self).get_parser(prog_name)
        parser.add_argument('configuration',
                            metavar="<configuration>",
                            help=_("Configuration id"))
        parser.add_argument('--name',
                            metavar="<name>",
                            help=_("New Configuration name"))
        parser.add_argument('--description',
                            metavar="<description>",
                            help=_("New Configuration description"))
        parser.add_argument(
            '--value',
            dest="values",
            metavar="<key=value>",
            required=True,
            action=parseractions.KeyValueAction,
            help=_("Configuration value"
                   "(repeat option to set multiple values)."))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        config_attrs = {}

        if parsed_args.name:
            config_attrs['name'] = parsed_args.name
        if parsed_args.description:
            config_attrs['description'] = parsed_args.description
        if parsed_args.values:
            config_attrs['values'] = parsed_args.values

        config = client.find_configuration(parsed_args.configuration,
                                           ignore_missing=False)

        client.update_configuration(config, **config_attrs)


class DeleteConfiguration(command.Command):
    _description = _("Delete a configuration")

    def get_parser(self, prog_name):
        parser = super(DeleteConfiguration, self).get_parser(prog_name)
        parser.add_argument('configuration',
                            metavar='<configuration>',
                            nargs='+',
                            help=_('ID or name of the configuration group'))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        if parsed_args.configuration:
            for cnf in parsed_args.configuration:
                resource = client.find_configuration(cnf, ignore_missing=False)
                client.delete_configuration(resource)
