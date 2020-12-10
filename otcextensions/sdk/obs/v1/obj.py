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
# from botocore.exceptions import ClientError
import base64
import hashlib

from openstack import _log
from openstack import exceptions
from openstack import resource

# from otcextensions.i18n import _
from otcextensions.sdk.obs.v1 import _base

import xml.etree.ElementTree as ET


_logger = _log.setup_logging('openstack')


class Object(_base.BaseResource):

    base_path = '/'

    allow_create = True
    allow_get = True
    allow_commit = True
    allow_delete = True
    allow_list = True
    allow_head = True

    resources_key = ''
    resource_key = 'Contents'

    _query_mapping = resource.QueryParameters(
        'prefix', 'delimiter',
        'limit',
        prefix='prefix',
        delimiter='delimiter',
        limit='max-keys'
    )

    data = None

    name = resource.Body('Key', alternate_id=True)
    last_modified = resource.Body('LastModified')
    etag = resource.Body('ETag')
    content_length = resource.Body('Size', type=int)
    storage_class = resource.Body('StorageClass')

    content_md5 = resource.Header('Content-MD5', type=str)
    #: private, public-read, public-read-write, authenticated-read
    #: bucket-owner-read, bucket-owner-full-control
    acl = resource.Header('x-amz-acl')
    object_storage_class = resource.Header('x-amz-storage-class')
    container = resource.URI('container')

    def __init__(self, data=None, **attrs):
        super(_base.BaseResource, self).__init__(**attrs)
        self.data = data

    def _translate_response(self, response, has_body=True, error_message=None):
        """Given a KSA response, inflate this instance with its data

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        exceptions.raise_from_response(response, error_message=response.text)
        _logger.debug(response.text)
        if response:
            if has_body:
                # TODO(agoncharov): do nothing so far. Generally need
                # to parse different responses
                pass

    @classmethod
    def list(cls, session, paginated=False, requests_auth=None, **params):
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params, cls)
        uri = cls.base_path % params

        # Build additional arguments to the GET call

        while uri:

            response = session.get(
                uri,
                requests_auth=requests_auth,
                params=query_params.copy()
            )

            uri = None
            next_params = {}

            root = ET.fromstring(response.content)

            if root.tag != ET.QName(cls.OBS_NS, 'ListBucketResult'):
                _logger.warn('Namespace in the response does not match '
                             'expectation')
                cls.OBS_NS = root.tag.split('}', 1)[0][1:]

            for element in root:

                if element.tag == ET.QName(cls.OBS_NS, cls.resource_key):
                    # Convert XML part into dict
                    dict_raw_resource = cls.etree_to_dict(element)
                    # extract resource data
                    dict_resource = dict_raw_resource[cls.resource_key]
                    value = cls.existing(**dict_resource)
                    yield value

                elif element.tag == ET.QName(cls.OBS_NS, 'NextMarker'):
                    next_params['marker'] = element.text

            if 'marker' in next_params:
                uri = cls.base_path % params
                query_params.update(next_params)

        return

    def create(self, session, prepend_key=True,
               requests_auth=None, **params):

        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, 'create')

        session = self._get_session(session)

        if not self.content_md5 and self.data:
            md5 = hashlib.md5()
            md5.update(str.encode(self.data))
            self.content_md5 = base64.b64encode(md5.digest()).decode()

        request = self._prepare_request(
            requires_id=True,
            prepend_key=prepend_key)

        response = session.put(
            request.url,
            data=self.data,
            requests_auth=requests_auth,
            request_headers=request.headers,
            **params)
        self._translate_response(response)
        return self

    def download(self, session, filename=None, **params):

        session = self._get_session(session)

        request = self._prepare_request(requires_id=True)

        response = session.get(
            request.url,
            request_headers=request.headers,
            **params)
        self._translate_response(response)

        _logger.debug(response.content)

        with open(filename, 'wb') as f:
            f.write(response.content)

        return
