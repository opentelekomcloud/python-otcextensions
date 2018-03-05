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
"""Flavor v1 action implementations"""

import logging

import six

# from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib.cli import parseractions
from osc_lib import exceptions
from osc_lib import utils

from otcextensions.i18n import _
# from otcextensions.sdk.rds.v1.configuration import ParameterGroup


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


class ListPG(command.Lister):
    _description = _("List Parameter Groups")

    def get_parser(self, prog_name):
        parser = super(ListPG, self).get_parser(prog_name)
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help=_('List additional fields in output'),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        data = client.parameter_groups()

        if parsed_args.long:
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
                'instance_count'
            )
            column_headers = (
                'ID',
                'Name',
                'Description',
                'Datastore VerID',
                'Datastore VerName',
                'Datastore Name',
                'Created on',
                'Updated on',
                'Allow update',
                'Instance count'
            )
        else:
            columns = (
                'id',
                'name',
                'description',
                'datastore_version_id',
                'datastore_version_name',
                'datastore_name',
                'instance_count'
            )
            column_headers = (
                'ID',
                'Name',
                'Description',
                'Datastore VerID',
                'Datastore VerName',
                'Datastore Name',
                'Instance count'
            )

        return (
            column_headers,
            (utils.get_item_properties(
                s,
                columns,
            ) for s in data)
        )


class ShowPG(command.ShowOne):
    _description = _("Display Parameter Groups details")

    def get_parser(self, prog_name):
        parser = super(ShowPG, self).get_parser(prog_name)
        parser.add_argument(
            'pg',
            metavar="<parameter_group>",
            help=_("Parameter groups to display (ID)")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.rds

        obj = client.get_parameter_group(parsed_args.pg)

        LOG.debug('object is %s' % obj)
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
            'parameters',
            'values'
        )

        # info = _format_pg(obj)
        # return zip(*sorted(six.iteritems(info)))
        # TODO(agoncharov) values and parameters are breaking the layout
        # dramatically. Maybe it make sence to create additional
        # filter to get/list only specific values/params
        data = utils.get_item_properties(
            obj, columns,
            formatters={
                'values': format_dict,
                'parameters': utils.format_list_of_dicts,
            }
        )

        return (columns, data)


class CreatePG(command.ShowOne):
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
        parser = super(CreatePG, self).get_parser(prog_name)
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
            metavar="<datastore_version",
            required=True,
            help=_("Datastore version")
        )
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

        pg_attrs = {}
        pg_attrs['datastore'] = {}
        if parsed_args.name:
            pg_attrs['name'] = parsed_args.name
        if parsed_args.description:
            pg_attrs['description'] = parsed_args.description
        if parsed_args.datastore_type and parsed_args.datastore_version:
            pg_attrs['datastore']['type'] = parsed_args.datastore_type
            pg_attrs['datastore']['version'] = parsed_args.datastore_version

        # flatten values into the proper pg_attrs
        if getattr(parsed_args, 'values', None):
            pg_attrs['values'] = {}
            for k, v in six.iteritems(parsed_args.values):
                pg_attrs['values'][k] = str(v)

        pg = client.create_parameter_group(**pg_attrs)

        data = utils.get_item_properties(
            pg, self.columns,
            formatters={
                'values': format_dict,
            }
        )

        return (self.columns, data)


class SetPG(command.ShowOne):
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
        parser = super(SetPG, self).get_parser(prog_name)
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

        pg_attrs = {}

        if parsed_args.name:
            pg_attrs['name'] = parsed_args.name
        if parsed_args.description:
            pg_attrs['description'] = parsed_args.description

        # flatten values into the proper pg_attrs
        if getattr(parsed_args, 'values', None):
            pg_attrs['values'] = {}
            for k, v in six.iteritems(parsed_args.values):
                pg_attrs['values'][k] = str(v)

        pg = client.get_parameter_group(parsed_args.parameter_group)

        if not pg:
            msg = (_("Failed to find Parameter Group by ID %s")
                   % parsed_args.parameter_group)
            raise exceptions.CommandError(msg)

        pg = pg.change_parameter_info(session=client, **pg_attrs)

        print(pg)

        data = utils.get_item_properties(
            pg, self.columns,
            formatters={
                'values': format_dict,
            }
        )

        return (self.columns, data)


class DeletePG(command.Command):
    _description = _("Delete Parameter Group(s)")

    def get_parser(self, prog_name):
        parser = super(DeletePG, self).get_parser(prog_name)
        parser.add_argument(
            "pgs",
            metavar="<pg>",
            nargs="+",
            help=_("ParameterGroup(s) to delete (name or ID)"),
        )
        return parser

    def take_action(self, parsed_args):

        del_result = 0
        client = self.app.client_manager.rds

        for pg in parsed_args.pgs:
            try:
                pg_obj = client.find_parameter_group(pg, ignore_missing=False)
                client.delete_parameter_group(pg_obj.id)
            except Exception as e:
                del_result += 1
                LOG.error(_("Failed to delete ParameterGroup with "
                            "ID or Name '%(pg)s': %(e)s"),
                          {'pg': pg, 'e': e})

        total = len(parsed_args.pgs)
        if (del_result > 0):
            msg = (_("Failed to delete %(dresult)s of %(total)s pgs.")
                   % {'dresult': del_result, 'total': total})
            raise exceptions.CommandError(msg)
