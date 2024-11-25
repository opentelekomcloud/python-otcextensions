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

from __future__ import print_function

import collections
import hashlib
# import errno
# import functools
# import json
import os
# import re
# import sys
import re
import threading
from urllib import parse

# import uuid
#
from urllib.parse import urlsplit

if os.name == 'nt':
    pass
else:
    msvcrt = None

# from oslo_utils import encodeutils
# from oslo_utils import strutils
# import prettytable
# import wrapt


_memoized_property_lock = threading.Lock()

SENSITIVE_HEADERS = ('X-Auth-Token',)
REQUIRED_FIELDS_ON_DATA = ('disk_format', 'container_format')


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    if y:
        z.update(y)
    return z


def _calculate_data_hashes(data):
    _md5 = hashlib.md5(usedforsecurity=False)

    if hasattr(data, 'read'):
        for chunk in iter(lambda: data.read(8192), b''):
            _md5.update(chunk)
    else:
        _md5.update(data)
    return _md5.hexdigest()


def _get_file_hashes(filename):
    _md5 = None
    with open(filename, 'rb') as file_obj:
        _md5 = _calculate_data_hashes(file_obj)

    return _md5


class FileSegment:
    """File-like object to pass to requests."""

    def __init__(self, filename, offset, length):
        self.filename = filename
        self.offset = offset
        self.length = length
        self.pos = 0
        self._file = open(filename, 'rb')
        self.seek(0)

    def tell(self):
        return self._file.tell() - self.offset

    def seek(self, offset, whence=0):
        if whence == 0:
            self._file.seek(self.offset + offset, whence)
        elif whence == 1:
            self._file.seek(offset, whence)
        elif whence == 2:
            self._file.seek(self.offset + self.length - offset, 0)

    def read(self, size=-1):
        remaining = self.length - self.pos
        if remaining <= 0:
            return b''

        to_read = remaining if size < 0 else min(size, remaining)
        chunk = self._file.read(to_read)
        self.pos += len(chunk)

        return chunk

    def reset(self):
        self._file.seek(self.offset, 0)


def _get_file_segments(endpoint, filename, file_size, segment_size):
    # Use an ordered dict here so that testing can replicate things
    segments = collections.OrderedDict()
    for (index, offset) in enumerate(range(0, file_size, segment_size)):
        remaining = file_size - (index * segment_size)
        segment = FileSegment(
            filename, offset,
            segment_size if segment_size < remaining else remaining)
        name = '{endpoint}/{index}'.format(
            endpoint=endpoint, index=index + 1)
        segments[name] = segment
    return segments


def extract_region_from_url(url):
    parsed_url = urlsplit(url)
    hostname = parsed_url.hostname
    match = re.search(r'eu-[^.]+', hostname)

    if match:
        return match.group()
    return


def extract_url_parts(url: str, project_id: str) -> list:
    """
    Extracts meaningful parts of a URL, excluding the project_id,
    version identifiers, and empty segments.

    Args:
        url (str): The URL to process.
        project_id (str): The project ID to exclude from the URL parts.

    Returns:
        list: A list of meaningful URL segments.
    """
    # Parse and strip the URL path
    path = parse.urlparse(url).path.strip()

    # Remove leading '/' to keep list indexes consistent
    if path.startswith('/'):
        path = path[1:]

    # Split the path into parts, excluding the project_id
    url_parts = [x for x in path.split('/') if x != project_id]

    # Exclude parts that are version identifiers
    url_parts = list(filter(
        lambda x: len(x) > 0 and not
        (x.lower().startswith('v') and x[1:].isdigit()),
        url_parts
    ))

    # Strip out empty or None segments and return
    return [part for part in url_parts if part]
