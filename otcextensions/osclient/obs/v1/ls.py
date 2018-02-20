#   Copyright 2013 Nebula Inc.
#
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
"""Bucket v1 action implementations"""

import logging

# from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import utils

from openstackclient.i18n import _

from otcextensions.osclient.obs.v1 import utils as utils_obs


logger = logging.getLogger(__name__)


class List(command.Lister):
    _description = _("List buckets")

    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        parser.add_argument(
            "url",
            metavar="<url>",
            nargs='?',
            help=_("Url"),
        )
        parser.add_argument(
            "--human-readable",
            action='store_true',
            default=False,
            help=_("Human-readable format"),
        )
        parser.add_argument(
            "--limit",
            metavar="<num-results>",
            type=int,
            help=_("Maximum number of results to show"),
        )
        parser.add_argument(
            "--marker",
            metavar="<bucket>",
            help=_("The market of previous request"),
        )
        parser.add_argument(
            "--prefix",
            metavar="<prefix>",
            help=_("The object prefix (subdir)"),
        )
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help=_('List additional fields in output'),
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.obs

        kwargs = {}
        if parsed_args.url:
            kwargs['url'] = parsed_args.url
            mode = 'Objects'
        if not parsed_args.url:
            mode = 'Buckets'
        # if parsed_args.recursive:
            # kwargs['recursive'] = parsed_args.recursive
        if parsed_args.limit:
            kwargs['limit'] = parsed_args.limit
        if parsed_args.marker:
            kwargs['marker'] = parsed_args.marker
        if parsed_args.prefix:
            kwargs['prefix'] = parsed_args.prefix

        data = self.ls(
            client=client,
            **kwargs
        )

        # print(tuple(data))

        if mode == 'Objects':
            if not parsed_args.long:
                columns = (
                    'LastModified',
                    'Key',
                    'Size'
                )
                column_headers = (
                    'Modify Date',
                    'Name',
                    'Size'
                )
            else:
                columns = (
                    'LastModified',
                    'Key',
                    'Size',
                    'etag',
                    'storageclass'
                )
                column_headers = (
                    'Modify Date',
                    'Name',
                    'Size',
                    'ETag',
                    'Storage Class'
                )

            if parsed_args.human_readable:
                data = self.humanize_size(data)
        elif mode == 'Buckets':
                columns = (
                    'CreationDate',
                    'Name'
                )
                column_headers = (
                    'Creation Date',
                    'Name'
                )

        return (
            column_headers,
            (utils.get_item_properties(
                s,
                columns,
            ) for s in data)
        )

    def ls(self, client, url=None, **kwargs):
        """s3 ls wrapper

        :param string url: url
        """
        result = None

        # if url:
        #     if url.startswith('s3://'):
        #         url = url[5:]
        #     url = url.strip('/')

        client_args = {}
        if 'limit' in kwargs:
            client_args['MaxKeys'] = kwargs.get('limit')
        if 'marker' in kwargs:
            client_args['Marker'] = kwargs.get('marker')
        if 'prefix' in kwargs:
            client_args['Prefix'] = kwargs.get('prefix')

        if url:
            # try to get bucket content
            bucket_name, path = utils_obs.parse_s3_uri(url)
            if path:
                client_args['Prefix'] = path
                if 'prefix' in kwargs:
                    logger.warn('Path contain key name, ' +
                                'This overrides the prefix')
            bucket = client.get_bucket_by_name(bucket_name)
            if bucket:
                result = client.objects(bucket, **client_args)
            else:
                logger.error('No such bucket found')

        else:
            # try to list buckets
            result = client.buckets(**client_args)

        if not result:
            result = []

        return result

    def humanize_size(self, data):
        """Humanize object size

        """
        # TODO(agoncharov): Not the nice way to simply modify value,
        # think of a different approach
        for rec in data:
            # rec = {
            #     k: utils.format_size(v) if k == 'size' else v
            #     for (k, v) in rec
            # }
            rec.size = utils.format_size(rec.size)
            yield rec
