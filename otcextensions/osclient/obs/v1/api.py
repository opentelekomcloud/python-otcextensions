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
import logging
import os
import re

from openstackclient.api import api

from otcextensions.common.obs_exception import ObsError
from otcextensions.common.obs_exception import ObsException

from otcextensions.obsclient.client import Client
from otcextensions.obsclient.utils import parse_s3_uri


LOG = logging.getLogger(__name__)


class API(api.BaseAPI):
    """S3 Wrapper API"""

    def __init__(self, client=None,
                 s3_hostname=None, s3_ak=None, s3_sk=None, region=None,
                 **kwargs):
        super(API, self).__init__(**kwargs)

        if client:
            self.client = client
        else:
            self.client = Client(s3_hostname, s3_ak, s3_sk, region, **kwargs)
        # self.s3 = client
        # otcsession = boto3.session.Session()
        #
        # s3client = otcsession.client(
        #     's3',
        #     region,
        #     # config=boto3.session.Config(signature_version='s3v4'),
        #     endpoint_url="https://" + s3_hostname,
        #     aws_access_key_id=s3_ak,
        #     aws_secret_access_key=s3_sk
        # )
        # self.s3 = s3client

    def ls(self, url=None, **kwargs):
        """s3 ls wrapper

        :param string url: url
        """
        result = None

        if url:
            if url.startswith('s3://'):
                url = url[5:]
            url = url.strip('/')

        client_args = {}
        if 'limit' in kwargs:
            client_args['MaxKeys'] = kwargs.get('limit')
        if 'marker' in kwargs:
            client_args['Marker'] = kwargs.get('marker')
        if 'prefix' in kwargs:
            client_args['Prefix'] = kwargs.get('prefix')

        if url:
            # try to get bucket content
            result = self.client.list_objects(url, **client_args)
        else:
            # try to list buckets
            result = self.client.list_buckets(**client_args)

        if not result:
            result = []

        return result

    def cp(self, src, dest, **kwargs):
        """s3 cp wrapper

        :param string src: source Url
        :param string dest: destination url
        """
        result = {}
        if dest.startswith('s3://') and not src.startswith('s3://'):
            # upload local file to OBS
            bucket, prefix = parse_s3_uri(dest)
            result['Mode'] = 'Upload %s to %s' % (src, dest)

            # check source
            if os.path.isfile(src) and os.access(src, os.R_OK):
                filename = os.path.basename(src)
                if prefix and prefix != '/':
                    key = prefix + '/' + filename
                else:
                    key = filename

                self.client.upload_fileobj(src, bucket, key)

            else:
                raise ObsException(
                    ObsError.ERROR_S3_LOCAL_SRC_FILE_MISSING.get_formatted(src)
                )

        if src.startswith('s3://') and not dest.startswith('s3://'):
            # Download from OBS to local
            # upload to OBS
            bucket, key = parse_s3_uri(src)

            if dest[-1] in ('.', '/'):
                # based on destination detect if we have only path or filename
                m = re.search('^(.*\/)?(.*)$', key)
                if dest[-1] == '.':
                    filename = m.group(2)
                else:
                    filename = dest + '/' + m.group(2)
            else:
                filename = dest
            result['Mode'] = 'Download %s/%s to %s' % (bucket, key, filename)

            result = self.client.download_fileobj(bucket, key, filename)
            if result == 404:
                raise ObsException(
                    ObsError.ERROR_S3_SOURCE_MISSING.get_formatted(key)
                )
            elif result != 0:
                raise ObsException(
                    ObsError.ERROR_INTERNAL
                )

        print(result['Mode'])
        return result
