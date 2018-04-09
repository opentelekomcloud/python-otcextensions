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
import os
import re

# from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import exceptions
import six

from openstack import exceptions as sdk_exceptions

from otcextensions.i18n import _

from otcextensions.common import exc
from otcextensions.osclient.obs.v1 import utils as utils_obs


LOG = logging.getLogger(__name__)


class Copy(command.ShowOne):
    _description = _("Copy (Upload/Download) buckets")

    def get_parser(self, prog_name):
        parser = super(Copy, self).get_parser(prog_name)
        parser.add_argument(
            "srcurl",
            metavar="<srcurl>",
            nargs=1,
            help=_("Source Url"),
        )
        parser.add_argument(
            "dsturl",
            metavar="<dsturl>",
            nargs=1,
            help=_("Destination Url"),
        )

        return parser

    def take_action(self, parsed_args):
        result, info = {}, {}

        client = self.app.client_manager.obs
        src = parsed_args.srcurl[0]
        dest = parsed_args.dsturl[0]

        try:
            result = self.cp(client, src, dest)
        except Exception as e:
            raise exceptions.CommandError(e.message)

        # if only one attr is in the list a coma should be present
        # otherwise it is treated as array
        copy_attrs = ['Mode']
        for attr in copy_attrs:
            if attr in result:
                val = result.get(attr, None)
                if val:
                    info[attr] = val
        # info['Bucket'] = dest

        return zip(*sorted(six.iteritems(info)))

    def cp(self, client, src, dest, **kwargs):
        """s3 cp wrapper

        :param string src: source Url
        :param string dest: destination url
        """
        result = {}
        if dest.startswith('s3://') and not src.startswith('s3://'):
            # upload local file to OBS
            bucket_name, prefix = utils_obs.parse_s3_uri(dest)

            bucket = client.get_bucket_by_name(bucket_name)

            if not bucket:
                raise exc.BaseException(
                    'Target bucket is not available'
                )

            # check source
            if os.path.isfile(src) and os.access(src, os.R_OK):
                # TODO(agoncharov) check if destination exists raise an error
                # filename = os.path.basename(src)
                # if prefix and prefix != '/':
                #     key = prefix + '/' + filename
                # else:
                #     key = filename

                result['Mode'] = 'Upload %s as %s' % (src, prefix)

                client.create_object(bucket, prefix, src)

            else:
                raise exc.BaseException(
                    'Source file is not accessible'
                )

        if src.startswith('s3://') and not dest.startswith('s3://'):
            # Download from OBS to local
            # upload to OBS
            bucket_name, key = utils_obs.parse_s3_uri(src)

            if dest[-1] in ('.', '/'):
                # based on destination detect if we have only path or filename
                m = re.search('^(.*\/)?(.*)$', key)
                if dest[-1] == '.':
                    filename = m.group(2)
                else:
                    filename = dest + '/' + m.group(2)
            else:
                filename = dest

            bucket = client.get_bucket_by_name(bucket_name)
            obj = client.get_object_by_key(bucket, key)
            result['Mode'] = 'Download %s to %s' % (src, filename)

            try:
                client.download_object(obj, filename)
            except sdk_exceptions.ResourceNotFound:
                raise exceptions.CommandError(
                    _('Object with the given key is not found')
                )
        #     if result == 404:
        #         raise ObsException(
        #             ObsError.ERROR_S3_SOURCE_MISSING.get_formatted(key)
        #         )
        #     elif result != 0:
        #         raise ObsException(
        #             ObsError.ERROR_INTERNAL
        #         )

        return result
