# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import re
import sys

from openstack import exceptions

import six


class BaseException(Exception):
    """An error occurred."""
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message or self.__class__.__doc__


class CommandError(BaseException):
    """Invalid usage of CLI."""


class InvalidEndpoint(BaseException):
    """The provided endpoint is invalid."""


class CommunicationError(BaseException):
    """Unable to communicate with server."""


class ClientException(Exception):
    """DEPRECATED!"""


class HTTPException(ClientException):
    """Base exception for all HTTP-derived exceptions."""
    code = 'N/A'

    def __init__(self, details=None):
        self.details = details or self.__class__.__name__

    def __str__(self):
        return "%s (HTTP %s)" % (self.details, self.code)


class HTTPMultipleChoices(HTTPException):
    code = 300

    def __str__(self):
        self.details = ("Requested version of OpenStack Images API is not "
                        "available.")
        return "%s (HTTP %s) %s" % (self.__class__.__name__, self.code,
                                    self.details)


class BadRequest(HTTPException):
    """DEPRECATED!"""
    code = 400


class HTTPBadRequest(BadRequest):
    pass


class Unauthorized(HTTPException):
    """DEPRECATED!"""
    code = 401


class HTTPUnauthorized(Unauthorized):
    pass


class Forbidden(HTTPException):
    """DEPRECATED!"""
    code = 403


class HTTPForbidden(Forbidden):
    pass


class NotFound(HTTPException):
    """DEPRECATED!"""
    code = 404


class HTTPNotFound(NotFound):
    pass


class HTTPMethodNotAllowed(HTTPException):
    code = 405


class Conflict(HTTPException):
    """DEPRECATED!"""
    code = 409


class HTTPConflict(Conflict):
    pass


class OverLimit(HTTPException):
    """DEPRECATED!"""
    code = 413


class HTTPOverLimit(OverLimit):
    pass


class HTTPInternalServerError(HTTPException):
    code = 500


class HTTPNotImplemented(HTTPException):
    code = 501


class HTTPBadGateway(HTTPException):
    code = 502


class ServiceUnavailable(HTTPException):
    """DEPRECATED!"""
    code = 503


class HTTPServiceUnavailable(ServiceUnavailable):
    pass


# NOTE(bcwaldon): Build a mapping of HTTP codes to corresponding exception
# classes
_code_map = {}
for obj_name in dir(sys.modules[__name__]):
    if obj_name.startswith('HTTP'):
        obj = getattr(sys.modules[__name__], obj_name)
        _code_map[obj.code] = obj


def from_response(response, body=None):
    """Return an instance of an HTTPException based on httplib response."""
    cls = _code_map.get(response.status_code, HTTPException)
    if body and 'json' in response.headers['content-type']:
        # Iterate over the nested objects and retrieve the "message" attribute.
        messages = [obj.get('message') for obj in response.json().values()]
        # Join all of the messages together nicely and filter out any objects
        # that don't have a "message" attr.
        details = '\n'.join(i for i in messages if i is not None)
        return cls(details=details)
    elif body and 'html' in response.headers['content-type']:
        # Split the lines, strip whitespace and inline HTML from the response.
        details = [re.sub(r'<.+?>', '', i.strip())
                   for i in response.text.splitlines()]
        details = [i for i in details if i]
        # Remove duplicates from the list.
        details_seen = set()
        details_temp = []
        for i in details:
            if i not in details_seen:
                details_temp.append(i)
                details_seen.add(i)
        # Return joined string separated by colons.
        details = ': '.join(details_temp)
        return cls(details=details)
    elif body:
        if six.PY3:
            body = body.decode('utf-8')
        details = body.replace('\n\n', '\n')
        return cls(details=details)

    return cls()


class NoTokenLookupException(Exception):
    """DEPRECATED!"""
    pass


class EndpointNotFound(Exception):
    """DEPRECATED!"""
    pass


class SSLConfigurationError(BaseException):
    pass


class SSLCertificateError(BaseException):
    pass


def raise_from_response(response, error_message=None):
    """Raise an instance of an HTTPException based on keystoneauth response."""
    if response.status_code < 400:
        return

    if response.status_code == 404:
        cls = exceptions.NotFoundException
    elif response.status_code == 400:
        cls = exceptions.BadRequestException
    else:
        cls = exceptions.HttpException

    details = None
    content_type = response.headers.get('content-type', '')
    if response.content and 'application/json' in content_type:
        # Iterate over the nested objects to retrieve "message" attribute.
        # TODO(shade) Add exception handling for times when the content type
        # is lying.

        try:
            content = response.json()
            error = content.get('error', None)
            messages = []
            if error:
                messages = [error.get('message', None)]
            else:
                messages = [obj.get('message') for obj in content.values()
                            if isinstance(obj, dict)]
            # Join all of the messages together nicely and filter out any
            # objects that don't have a "message" attr.
            details = '\n'.join(msg for msg in messages if msg)
        except Exception:
            details = response.text
    elif response.content and 'text/html' in content_type:
        # Split the lines, strip whitespace and inline HTML from the response.
        details = [re.sub(r'<.+?>', '', i.strip())
                   for i in response.text.splitlines()]
        details = list(set([msg for msg in details if msg]))
        # Return joined string separated by colons.
        details = ': '.join(details)
    if not details and response.reason:
        details = response.reason
    elif not details and response.text:
        details = response.text

    http_status = response.status_code
    request_id = response.headers.get('x-openstack-request-id')

    # sdk.exception define default for message to Error, but we need
    # have a better info
    if not error_message and details:
        error_message = details

    raise cls(
        message=error_message, response=response, details=details,
        http_status=http_status, request_id=request_id
    )
