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
import datetime
import functools
import hashlib
import hmac

import requests

from urllib.parse import quote
from urllib.parse import urlparse
from urllib.parse import urlsplit

from http import client as http_client


class HTTPHeaders(http_client.HTTPMessage):
    pass


def ensure_unicode(s, encoding=None, errors=None):
    # NOOP in Python 3, because every string is already unicode
    return s


EMPTY_SHA256_HASH = (
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

UNSIGNED_PAYLOAD = 'UNSIGNED-PAYLOAD'
PAYLOAD_BUFFER = 1024 * 1024

SIGNED_HEADERS_BLACKLIST = [
    'expect',
    'user-agent',
    'x-amzn-trace-id',
    'X-Auth-Token',
]
ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
SIGV4_TIMESTAMP = '%Y%m%dT%H%M%SZ'


class AKRequestsAuth(requests.auth.AuthBase):
    """
    Auth class that allows us to connect to AWS services
    via Amazon's signature version 4 signing process
    Adapted from
        https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
    """
    IDENTITY_AUTH_HEADER_NAME = 'X-Amz-Security-Token'

    def __init__(self,
                 access_key,
                 secret_access_key,
                 host,
                 region,
                 service,
                 token=None):
        """
        Example usage for talking to an AWS Elasticsearch Service:
        AKRequestsAuth(aws_access_key='YOURKEY',
               aws_secret_access_key='YOURSECRET',
               aws_host='search-service-foobar.us-east-1.es.amazonaws.com',
               aws_region='us-east-1',
               aws_service='es',
               aws_token='...')
        The aws_token is optional and is used only if you are using STS
        temporary credentials.
        """
        self.aws_access_key = access_key
        self.aws_secret_access_key = secret_access_key
        self.aws_host = host
        self.aws_region = region
        self.service = service
        self.aws_token = token

    def __call__(self, r):
        """
        Adds the authorization headers required by Amazon's signature
        version 4 signing process to the request.
        Adapted from
            https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
        """
        self.add_auth(r)
        return r

    def add_auth(self, request):
        """
        Returns a dictionary containing the necessary headers for Amazon's
        signature version 4 signing process. An example return value might
        look like
        {
            'Authorization': 'AWS4-HMAC-SHA256 Credential=YOURKEY/20160618'
                             '/us-east-1/es/aws4_request, '
                             'SignedHeaders=host;x-amz-date, '
                             'Signature=ca0a856286efce2a4bd96a978ca6c8966057e53184776c0685169d08abd74739',
            'x-amz-date': '20160618T220405Z',
        }
        """

        datetime_now = datetime.datetime.utcnow()
        self.timestamp = datetime_now.strftime(SIGV4_TIMESTAMP)
        # This could be a retry.  Make sure the previous
        # authorization header is removed first.
        self._modify_request_before_signing(request)
        canonical_request = self.canonical_request(request)
        string_to_sign = self.string_to_sign(request, canonical_request)
        signature = self.signature(string_to_sign, request)

        self._inject_signature_to_request(request, signature)

    def _modify_request_before_signing(self, request):
        if 'Authorization' in request.headers:
            del request.headers['Authorization']
        self._set_necessary_date_headers(request)
        if self.aws_token:
            if 'X-Amz-Security-Token' in request.headers:
                del request.headers['X-Amz-Security-Token']
            request.headers['X-Amz-Security-Token'] = self.aws_token

        # if not self._should_sha256_sign_payload(request):
        if 'X-Amz-Content-SHA256' in request.headers:
            del request.headers['X-Amz-Content-SHA256']
        request.headers['X-Amz-Content-SHA256'] = UNSIGNED_PAYLOAD

    def _set_necessary_date_headers(self, request):
        # The spec allows for either the Date _or_ the X-Amz-Date value to be
        # used so we check both.  If there's a Date header, we use the date
        # header.  Otherwise we use the X-Amz-Date header.
        # if 'Date' in request.headers:
        #     del request.headers['Date']
        #     datetime_timestamp = datetime.datetime.strptime(
        #         self.timestamp, SIGV4_TIMESTAMP)
        #     request.headers['Date'] = formatdate(
        #         int(calendar.timegm(datetime_timestamp.timetuple())))
        #     if 'X-Amz-Date' in request.headers:
        #         del request.headers['X-Amz-Date']
        # else:
        if 'X-Amz-Date' in request.headers:
            del request.headers['X-Amz-Date']
        request.headers['X-Amz-Date'] = self.timestamp

    def _inject_signature_to_request(self, request, signature):
        hdrs = ['AWS4-HMAC-SHA256 Credential=%s' % self.scope(request)]
        headers_to_sign = self.headers_to_sign(request)
        hdrs.append('SignedHeaders=%s' % self.signed_headers(headers_to_sign))
        hdrs.append('Signature=%s' % signature)
        request.headers['Authorization'] = ', '.join(hdrs)
        return request

    def payload(self, request):
        if not self._should_sha256_sign_payload(request):
            # When payload signing is disabled, we use this static string in
            # place of the payload checksum.
            return UNSIGNED_PAYLOAD
        if request.body and hasattr(request.body, 'seek'):
            position = request.body.tell()
            read_chunksize = functools.partial(request.body.read,
                                               PAYLOAD_BUFFER)
            checksum = hashlib.sha256()
            for chunk in iter(read_chunksize, b''):
                checksum.update(chunk)
            hex_checksum = checksum.hexdigest()
            request.body.seek(position)
            return hex_checksum
        elif request.body:
            # The request serialization has ensured that
            # request.body is a bytes() type.
            return hashlib.sha256(request.body).hexdigest()
        else:
            return EMPTY_SHA256_HASH

    def _should_sha256_sign_payload(self, request):
        # Payloads will always be signed over insecure connections.
        if not request.url.startswith('https'):
            return True

        # Certain operations may have payload signing disabled by default.
        # Since we don't have access to the operation model, we pass in this
        # bit of metadata through the request context.
        return True  # request.context.get('payload_signing_enabled', True)

    def canonical_headers(self, headers_to_sign):
        """
        Return the headers that need to be included in the StringToSign
        in their canonical form by converting all header keys to lower
        case, sorting them in alphabetical order and then joining
        them into a string, separated by newlines.
        """
        headers = []
        sorted_header_names = sorted(set(headers_to_sign))
        for key in sorted_header_names:
            value = ','.join(self._header_value(v) for v in
                             sorted(headers_to_sign.get_all(key)))
            headers.append('%s:%s' % (key, ensure_unicode(value)))
        return '\n'.join(headers)

    def _header_value(self, value):
        # From the sigv4 docs:
        # Lowercase(HeaderName) + ':' + Trimall(HeaderValue)
        #
        # The Trimall function removes excess white space before and after
        # values, and converts sequential spaces to a single space.
        return ' '.join(value.split())

    @classmethod
    def get_canonical_path(cls, r):
        """
        Create canonical URI--the part of the URI from domain to query
        string (use '/' if no path)
        """
        parsedurl = urlparse(r.url)

        # safe chars adapted from boto's use of urllib.parse.quote
        # https://github.com/boto/boto/blob/d9e5cfe900e1a58717e393c76a6e3580305f217a/boto/auth.py#L393
        return quote(parsedurl.path if parsedurl.path else '/', safe='/-_.~')

    @classmethod
    def get_canonical_querystring(cls, r):
        """
        Create the canonical query string. According to AWS, by the
        end of this function our query string values must
        be URL-encoded (space=%20) and the parameters must be sorted
        by name.
        This method assumes that the query params in `r` are *already*
        url encoded.  If they are not url encoded by the time they make
        it to this function, AWS may complain that the signature for your
        request is incorrect.
        It appears elasticsearc-py url encodes query paramaters on its own:
            https://github.com/elastic/elasticsearch-py/blob/5dfd6985e5d32ea353d2b37d01c2521b2089ac2b/elasticsearch/connection/http_requests.py#L64
        If you are using a different client than elasticsearch-py, it
        will be your responsibility to urleconde your query params before
        this method is called.
        """
        canonical_querystring = ''

        parsedurl = urlparse(r.url)
        querystring_sorted = '&'.join(sorted(parsedurl.query.split('&')))

        for query_param in querystring_sorted.split('&'):
            key_val_split = query_param.split('=', 1)

            key = key_val_split[0]
            if len(key_val_split) > 1:
                val = key_val_split[1]
            else:
                val = ''

            if key:
                if canonical_querystring:
                    canonical_querystring += "&"
                canonical_querystring += u'='.join([key, val])

        return canonical_querystring

    def headers_to_sign(self, request):
        """
        Select the headers from the request that need to be included
        in the StringToSign.
        """
        header_map = HTTPHeaders()
        for name, value in request.headers.items():
            lname = name.lower()
            if lname not in SIGNED_HEADERS_BLACKLIST:
                header_map[lname] = value
        if 'host' not in header_map:
            header_map['host'] = self._canonical_host(request.url)
        return header_map

    def canonical_request(self, request):
        cr = [request.method.upper()]
        path = self.get_canonical_path(request)
        cr.append(path)
        cr.append(self.get_canonical_querystring(request))
        headers_to_sign = self.headers_to_sign(request)
        cr.append(self.canonical_headers(headers_to_sign) + '\n')
        cr.append(self.signed_headers(headers_to_sign))
        if 'X-Amz-Content-SHA256' in request.headers:
            body_checksum = request.headers['X-Amz-Content-SHA256']
        else:
            body_checksum = self.payload(request)
        cr.append(body_checksum)
        return '\n'.join(cr)

    def _canonical_host(self, url):
        url_parts = urlsplit(url)
        default_ports = {
            'http': 80,
            'https': 443
        }
        if any(url_parts.scheme == scheme and url_parts.port == port
               for scheme, port in default_ports.items()):
            # No need to include the port if it's the default port.
            return url_parts.hostname
        # Strip out auth if it's present in the netloc.
        return url_parts.netloc.rsplit('@', 1)[-1]

    def string_to_sign(self, request, canonical_request):
        """
        Return the canonical StringToSign as well as a dict
        containing the original version of all headers that
        were included in the StringToSign.
        """
        sts = ['AWS4-HMAC-SHA256']
        sts.append(self.timestamp)
        sts.append(self.credential_scope(request))
        sts.append(
            hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        )
        return '\n'.join(sts)

    def signed_headers(self, headers_to_sign):
        hdrs = ['%s' % n.lower().strip() for n in set(headers_to_sign)]
        hdrs = sorted(hdrs)
        return ';'.join(hdrs)
    # def _normalize_url_path(self, path):
    #     normalized_path = quote(normalize_url_path(path), safe='/~')
    #     return normalized_path

    def _sign(self, key, msg, hex=False):
        if hex:
            sig = hmac.new(
                key,
                msg.encode('utf-8'),
                hashlib.sha256).hexdigest()
        else:
            sig = hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
        return sig

    def signature(self, string_to_sign, request):
        key = self.aws_secret_access_key
        k_date = self._sign(('AWS4' + key).encode('utf-8'),
                            self.timestamp[0:8])
        k_region = self._sign(k_date, self.aws_region)
        k_service = self._sign(k_region, self.service)
        k_signing = self._sign(k_service, 'aws4_request')
        return self._sign(k_signing, string_to_sign, hex=True)

    def credential_scope(self, request):
        scope = []
        scope.append(self.timestamp[0:8])
        scope.append(self.aws_region)
        scope.append(self.service)
        scope.append('aws4_request')
        return '/'.join(scope)

    def scope(self, request):
        scope = [self.aws_access_key]
        scope.append(self.timestamp[0:8])
        scope.append(self.aws_region)
        scope.append(self.service)
        scope.append('aws4_request')
        return '/'.join(scope)
