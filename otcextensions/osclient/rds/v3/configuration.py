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
"""Configuration v3 action implementations"""
import json
import logging

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

from otcextensions.i18n import _

import six
import yaml
LOG = logging.getLogger(__name__)

DATASTORE_TYPE_CHOICES = ['MySQL', 'PostgreSQL', 'SQLServer']


def format_dict(data):
    """Return a formatted string of key value pairs

    :param data: a dict
    :rtype: a string formatted to key='value'
    """

    if data is None:
        return None

    output = ""
    for s in sorted(data):
        output = output + s + "='" + six.text_type(data[s]) + "',\n "
    return output[:-2]


class ListConfigurations(command.Lister):
    _description = _("List Parameter Groups")
    columns = ['ID', 'Name', 'Description', 'Datastore Name',
               'Datastore Version Name', 'User Defined']

    def get_parser(self, prog_name):
        parser = super(ListConfigurations, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            dest='limit',
            metavar='<limit>',
            type=int,
            default=None,
            help=_('Limit the number of results displayed. (Not supported)')
        )
        parser.add_argument(
            '--marker',
            dest='marker',
            metavar='<ID>',
            help=_('Begin displaying the results for IDs greater than the '
                   'specified marker. When used with --limit, set this to '
                   'the last ID displayed in the previous run. '
                   '(Not supported)')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.configurations()

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowConfiguration(command.ShowOne):
    _description = _("Shows details of a database configuration group.")
    columns = ['ID', 'Name', 'Description', 'Datastore Name',
               'Datastore Version Name', 'Values']

    def get_parser(self, prog_name):
        parser = super(ShowConfiguration, self).get_parser(prog_name)
        parser.add_argument(
            'configuration_group',
            metavar="<configuration_group>",
            help=_("ID or name of the configuration group")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        obj = client.find_configuration(parsed_args.configuration_group)
        # TODO(agoncharov) find by name does not return parameter values

        # TODO(agoncharov) values and parameters are breaking the layout
        # dramatically. Maybe it make sence to create additional
        # filter to get/list only specific values/params
        data = utils.get_item_properties(
            obj, self.columns,
            formatters={
                'values': format_dict,
                'parameters': utils.format_list_of_dicts,
            }
        )

        return (self.columns, data)


class CreateConfiguration(command.ShowOne):
    _description = _("Create new Parameter Group")

    columns = (
        'id',
        'name',
        'description',
        'datastore_version_id',
        'datastore_version_name',
        'datastore_name',
        'created',
        'updated',
        'allowed_updated',
        'instance_count',
        'values'
    )

    def get_parser(self, prog_name):
        parser = super(CreateConfiguration, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar="<name>",
            required=True,
            help=_("Parameter group name")
        )
        parser.add_argument(
            '--description',
            metavar="<description>",
            help=_("Parameter group description")
        )
        parser.add_argument(
            '--datastore_type',
            metavar="<datastore_type>",
            choices=DATASTORE_TYPE_CHOICES,
            required=True,
            help=_("Datastore type")
        )
        parser.add_argument(
            '--datastore_version',
            metavar="<datastore_version>",
            required=True,
            help=_("Datastore version")
        )
#        parser.add_argument(
#            '--value',
#            dest="ind_values",
#            metavar="<key=value>",
#            action=parseractions.KeyValueAction,
#            help=_("Parameter group value"
#                   "(repeat option to set multiple values)")
#        )
        parser.add_argument(
            '--values',
            metavar='<values>',
            help=_('Dictionary (JSON) of the values to set.'),
            type=yaml.load
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
            datastore = {}
            datastore['type'] = parsed_args.datastore_type
            datastore['version'] = parsed_args.datastore_version
            config_attrs['datastore'] = datastore

        # flatten values into the proper config_attrs
#        values = {}
#        try:
#            values = json.loads(parsed_args.values)
#        except Exception as e:
#            msg = (_("Failed to parse configuration values: %(e)s")
#                   % {'e': e})
#            raise exceptions.CommandError(msg)
#
#        if getattr(parsed_args, 'ind_values', None):
#            for k, v in six.iteritems(parsed_args.ind_values):
#                values[k] = str(v)
#
        config_attrs['values'] = parsed_args.values
        config = client.create_configuration(**config_attrs)

        data = utils.get_item_properties(
            config, self.columns,
            formatters={
                'values': format_dict,
            }
        )

        return (self.columns, data)


class SetConfiguration(command.ShowOne):
    _description = _("Set values of the Parameter Group")

    columns = (
        'id',
        'name',
        'description',
        'datastore_version_id',
        'datastore_version_name',
        'datastore_name',
        'created',
        'updated',
        'allowed_updated',
        'instance_count',
        'values'
    )

    def get_parser(self, prog_name):
        parser = super(SetConfiguration, self).get_parser(prog_name)
        parser.add_argument(
            '--parameter-group',
            metavar="<parameter_group>",
            required=True,
            help=_("Parameter group id")
        )
        parser.add_argument(
            '--name',
            metavar="<name>",
            help=_("New ParameterGroup name")
        )
        parser.add_argument(
            '--description',
            metavar="<description>",
            help=_("New ParameterGroup description")
        )
        # parser.add_argument(
        #     '--datastore_type',
        #     metavar="<datastore_type>",
        #     choices=DATASTORE_TYPE_CHOICES,
        #     required=True,
        #     help=_("Datastore type")
        # )
        # parser.add_argument(
        #     '--datastore_version',
        #     metavar="<datastore_version",
        #     required=True,
        #     help=_("Datastore version")
        # )
        parser.add_argument(
            '--value',
            dest="values",
            metavar="<key=value>",
            required=True,
            action=parseractions.KeyValueAction,
            help=_("Parameter group value"
                   "(repeat option to set multiple values)")
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        config_attrs = {}

        if parsed_args.name:
            config_attrs['name'] = parsed_args.name
        if parsed_args.description:
            config_attrs['description'] = parsed_args.description

        # flatten values into the proper Configuration_attrs
        if getattr(parsed_args, 'values', None):
            config_attrs['values'] = {}
            for k, v in six.iteritems(parsed_args.values):
                config_attrs['values'][k] = str(v)

        config = client.get_parameter_group(parsed_args.parameter_group)

        if not config:
            msg = (_("Failed to find Parameter Group by ID %s")
                   % parsed_args.parameter_group)
            raise exceptions.CommandError(msg)

        config = config.change_parameter_info(session=client, **config_attrs)

        data = utils.get_item_properties(
            config, self.columns,
            formatters={
                'values': format_dict,
            }
        )

        return (self.columns, data)


class DeleteConfiguration(command.Command):
    _description = _("Deletes a configuration group.")

    def get_parser(self, prog_name):
        parser = super(DeleteConfiguration, self).get_parser(prog_name)
        parser.add_argument(
            'configuration',
            metavar='<configuration>',
            nargs='+',
            help=_('ID or name of the configuration group')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds
        if parsed_args.configuration:
            for cnf in parsed_args.configuration:
                client.delete_configuration(
                    cnf, ignore_missing=False)


class ListDatabaseConfigurationParameters(command.Lister):

    _description = _("Lists available parameters for a configuration group.")
    columns = ['Name', 'Type', 'Min Size', 'Max Size', 'Restart Required']

    def get_parser(self, prog_name):
        parser = super(ListDatabaseConfigurationParameters, self).\
            get_parser(prog_name)
        parser.add_argument(
            'datastore_version',
            metavar='<datastore_version>',
            help=_('Datastore version name or ID assigned'
                   'to the configuration group.')
        )
        parser.add_argument(
            '--datastore',
            metavar='<datastore>',
            default=None,
            help=_('ID or name of the datastore to list configuration'
                   'parameters for. Optional if the ID of the'
                   'datastore_version is provided.')
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        # db_configuration_parameters = self.app.client_manager.rds
        # if parsed_args.datastore:
        #     params = db_configuration_parameters.\
        #         parameters(parsed_args.datastore,
        #                    parsed_args.datastore_version)
        # elif utils.is_uuid_like(parsed_args.datastore_version):
        #     params = db_configuration_parameters.\
        #         parameters_by_version(parsed_args.datastore_version)
        # else:
        #     raise exceptions.NoUniqueMatch(_('The datastore name or id is'
        #                                      ' required to retrieve the'
        #                                      ' parameters for the'
        #                                      ' configuration group'
        #                                      ' by name.'))
        # for param in params:
        #     setattr(param, 'min_size', getattr(param, 'min', '-'))
        #     setattr(param, 'max_size', getattr(param, 'max', '-'))
        # params = [utils.get_item_properties(p, self.columns)
        #           for p in params]
        # return self.columns, params


class ShowDatabaseConfigurationParameter(command.ShowOne):
    _description = _("Shows details of a database configuration parameter.")

    def get_parser(self, prog_name):
        parser = super(ShowDatabaseConfigurationParameter, self).\
            get_parser(prog_name)
        parser.add_argument(
            'datastore_version',
            metavar='<datastore_version>',
            help=_('Datastore version name or ID assigned to the'
                   ' configuration group.'),
        )
        parser.add_argument(
            'parameter',
            metavar='<parameter>',
            help=_('Name of the configuration parameter.'),
        )
        parser.add_argument(
            '--datastore',
            metavar='<datastore>',
            default=None,
            help=_('ID or name of the datastore to list configuration'
                   ' parameters for. Optional if the ID of the'
                   ' datastore_version is provided.'),
        )
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
        # db_configuration_parameters = self.app.client_manager.database.\
        #     configuration_parameters
        # if parsed_args.datastore:
        #     param = db_configuration_parameters.get_parameter(
        #         parsed_args.datastore,
        #         parsed_args.datastore_version,
        #         parsed_args.parameter)
        # elif utils.is_uuid_like(parsed_args.datastore_version):
        #     param = db_configuration_parameters.get_parameter_by_version(
        #         parsed_args.datastore_version,
        #         parsed_args.parameter)
        # else:
        #     raise exceptions.NoUniqueMatch(_('The datastore name or id is'
        #                                      ' required to retrieve the'
        #                                      ' parameter for the'
        #                                      ' configuration group'
        #                                      ' by name.'))
        # return zip(*sorted(six.iteritems(param._info)))
