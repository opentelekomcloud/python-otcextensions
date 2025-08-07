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
import xml.etree.ElementTree as ET
from io import BufferedReader

from openstack import _log
from openstack import exceptions
from openstack import resource

# from otcextensions.i18n import _
from otcextensions.sdk.obs.v1 import _base

_logger = _log.setup_logging('openstack')


class Object(_base.BaseResource):
    _custom_metadata_prefix = "x-amz-meta-"
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

    # Data to be passed during a POST call to create an object on the server.
    data = None

    # URL parameters
    #: The unique name for the container.
    container = resource.URI("container")
    #: The unique name for the object.
    name = resource.Body('Key', alternate_id=True)
    #: The date and time that the object was created or the last
    #: time that the metadata was changed.
    last_modified = resource.Body('LastModified')
    #: size of the response body. Instead it contains the size of
    #: the object, in bytes.
    content_length = resource.Body('Size', type=int)
    # Headers for requests
    #: private, public-read, public-read-write, authenticated-read
    #: bucket-owner-read, bucket-owner-full-control
    acl = resource.Header('x-amz-acl')

    accept_ranges = resource.Header('Accept-Ranges')
    #: The MD5 digest string of the message body is calculated according
    #: to the RFC 1864 standard. That is, calculate the 128-bit binary array
    #: (the message header data encrypted with MD5) first,
    #: and then use Base 64 encoding to convert the binary data to
    #: a character string.
    content_md5 = resource.Header('Content-MD5', type=str)
    #: Indicates the content type of a requested resource, for example,
    #: text/plain.
    content_type = resource.Header('Content-Type', type=str)
    #: Indicates the hash value of an object.
    #: The entity tag (ETag) only reflects changes to the contents
    #: of an object, not its metadata.
    etag = resource.Header('ETag', type=str)
    #: Indicates the value created by OBS to uniquely identify a request.
    #: OBS uses this value to troubleshoot faults.
    request_id = resource.Header('x-amz-request-id', type=str)
    #: Indicates a special token that helps OBS troubleshoot faults.
    request_id_2 = resource.Header('x-amz-id-2', type=str)
    #: Indicates that SSE-KMS is used.
    #: Example: x-amz-server-side-encryption:aws:kms
    sse = resource.Header('x-amz-server-side-encryption')
    #: Indicates the master key ID. This header is used in SSE-KMS mode.
    #: If the customer does not provide the master key,
    #: the default master key will be used.
    sse_key_id = resource.Header('x-amz-server-side-encryption-aws-kms-key-id')
    #: Indicates a decryption algorithm. The header is used in SSE-C mode.
    #: Constraints: This header must be used together with
    #: x-amz-server-side-encryption-customer-key and
    #: x-amz-server-side-encryption-customer-key-MD5.
    sse_algorithm = resource.Header(
        'x-amz-server-side-encryption-customer-algorithm'
    )
    #: Indicates a key used to decrypt objects.
    #: The header is used in SSE-C mode.
    #: Constraints: This header is a base64-encoded 256-bit or 512-bit key and
    #: must be used together with
    # x-amz-server-side-encryption-customer-algorithm and
    # x-amz-server-side-encryption-customer-key-MD5
    sse_key = resource.Header('x-amz-server-side-encryption-customer-key')
    #: Indicates the MD5 value of a key used to decrypt objects.
    #: The header is used in SSE-C mode.
    #: The MD5 value is used to check whether any error
    #: occurs during the transmission of the key.
    #: Constraints: This header is a base64-encoded 128-bit MD5 value and
    #: must be used together with
    #: x-amz-server-side-encryption-customer-algorithm and
    #: x-amz-server-side-encryption-customer-key.
    sse_key_md5 = resource.Header(
        'x-amz-server-side-encryption-customer-key-MD5'
    )
    #: When creating an object, you can add this header in the request
    #: to set the storage class of the object. If you do not add this header,
    #: the object will use the default storage class of the bucket.
    #: Note: The storage class can be STANDARD (OBS Standard),
    #: STANDARD_IA (OBS Warm), or GLACIER (OBS Cold).
    #: Note that the three storage class values are case-sensitive.
    storage_class = resource.Header('x-amz-storage-class')
    #: Server name
    server = resource.Header('Server', type=str)
    #: If a bucket is configured as a website, redirects requests
    #: for this object to another object in the same bucket or to
    #: an external URL.
    #: OBS stores the value of this header in the object metadata.
    website_redirect = resource.Header('x-amz-website-redirect-location')

    #: Obtains the specified range bytes of an object.
    #: The value is a range starting from 0 to maximum object length minus one.
    #: If the range is invalid, all object data is returned.
    range = resource.Header("range", type=str)
    #: Returns the object only if it has been modified since
    #: the time specified by this header,
    #: otherwise 304 Not Modified is returned.
    if_modified_since = resource.Header("if-modified-since", type=str)
    #: Returns the object only if it has not been modified since
    #: the time specified by this header,
    #: otherwise 412 Precondition Failed is returned.
    #: http://www.ietf.org/rfc/rfc2616.txt.
    if_unmodified_since = resource.Header("if-unmodified-since", type=str)
    #: Returns the object only if its ETag is the same
    #: as the one specified by this header,
    #: otherwise 412 Precondition Failed is returned.
    #: http://www.ietf.org/rfc/rfc2616.txt.
    if_match = resource.Header("if-match", type=list)
    #: Returns the object only if its ETag is different from the one
    #: specified by this header,
    #: otherwise 304 Not Modified is returned.
    if_none_match = resource.Header("if-none-match", type=list)
    #: Indicates an origin specified by a pre-request.
    #: Generally, it is a domain name
    origin = resource.Header("Origin", type=bool)

    def __init__(self, data=None, **attrs):
        super(_base.BaseResource, self).__init__(**attrs)
        self.data = data

    def _translate_response(self, response, has_body=True, error_message=None,
                            resource_response_key=None):
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
        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
        self._update_location()
        dict.update(self, self.to_dict())

    @classmethod
    def list(cls, session, paginated=False,
             endpoint_override=None, headers=None, requests_auth=None,
             **params):
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params, cls)
        uri = cls.base_path % params

        # Build additional arguments to the GET call
        get_args = cls._prepare_override_args(
            endpoint_override=endpoint_override,
            additional_headers=headers)

        while uri:

            response = session.get(
                uri,
                params=query_params.copy(),
                requests_auth=requests_auth,
                **get_args
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
               endpoint_override=None, headers=None, requests_auth=None):

        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, 'create')

        session = self._get_session(session)

        if not self.content_md5 and self.data and\
                not isinstance(self.data, BufferedReader):
            md5 = hashlib.md5()
            md5.update(str.encode(self.data))
            self.content_md5 = base64.b64encode(md5.digest()).decode()

        request = self._prepare_request(
            requires_id=True,
            prepend_key=prepend_key)

        if self.id[-1] == "/":
            request.url += "/"

        req_args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            additional_headers=headers,
            requests_auth=requests_auth)

        response = session.put(
            request.url,
            data=self.data,
            **req_args)
        self._translate_response(response)
        return self

    def delete(self, session, error_message=None,
               endpoint_override=None, headers=None,
               requests_auth=None, params=None):

        if not self.allow_delete:
            raise exceptions.MethodNotSupported(self, "delete")

        request = self._prepare_request()
        if self.id[-1] == "/":
            request.url += "/"

        session = self._get_session(session)

        delete_args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            additional_headers=headers,
            requests_auth=requests_auth)
        if params:
            delete_args['params'] = params

        response = session.delete(request.url,
                                  **delete_args)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, has_body=False, **kwargs)
        return self

    def download(self, session, filename=None,
                 endpoint_override=None, requests_auth=None):

        session = self._get_session(session)

        request = self._prepare_request(requires_id=True)

        req_args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            requests_auth=requests_auth)

        response = session.get(
            request.url,
            **req_args)
        self._translate_response(response)

        _logger.debug(response.content)

        with open(filename, 'wb') as f:
            f.write(response.content)

        return

    @staticmethod
    def initiate_multipart_upload(proxy, endpoint, name, **params):
        response = proxy.post(url=f'/{name}?uploads',
                              endpoint_override=endpoint,
                              **params)
        dict_resource = {}
        root = ET.fromstring(response.content)
        for element in root:
            dict_raw_resource = _base.BaseResource.etree_to_dict(element)
            dict_raw_resource = Object.clear_element(dict_raw_resource, proxy)
            dict_resource.update(dict_raw_resource)
        return dict_resource['UploadId']

    @staticmethod
    def get_parts(proxy, endpoint, requests_auth):
        response = proxy.get(endpoint, requests_auth=requests_auth)
        dict_resource = {}
        root = ET.fromstring(response.content)
        for element in root:
            dict_raw_resource = _base.BaseResource.etree_to_dict(element)
            dict_raw_resource = Object.clear_element(dict_raw_resource, proxy)
            if element.tag.endswith('Part'):
                dict_resource.setdefault('Parts', []).append(
                    dict_raw_resource['Part']
                )
                continue
            dict_resource.update(dict_raw_resource)
        return dict_resource

    @staticmethod
    def clear_element(dict_raw_resource, proxy):
        if proxy.region_name == 'eu-ch2':
            cleaned_dict = {}
            for full_key, value in dict_raw_resource.items():
                # Strip namespace if present
                cleaned_key = full_key.split('}', 1)[1] \
                    if full_key.startswith('{') else full_key
                cleaned_dict[cleaned_key] = value
            dict_raw_resource = cleaned_dict
        return dict_raw_resource

    @staticmethod
    def complete_multipart_upload(
            proxy, endpoint, upload_id, data, headers, requests_auth):
        url = f'{endpoint}?uploadId={upload_id}'
        root = ET.Element("CompleteMultipartUpload")
        for item in data:
            item = Object.clear_element(item, proxy)
            part = ET.SubElement(root, "Part")
            ET.SubElement(part, 'PartNumber').text = item['PartNumber']
            ET.SubElement(part, 'ETag').text = item['ETag']
        tree = ET.ElementTree(root)
        data = ET.tostring(tree.getroot()).decode()
        return proxy.post(url, data=data,
                          headers=headers, requests_auth=requests_auth)
