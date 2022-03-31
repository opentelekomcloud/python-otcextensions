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

# import errno
# import functools
import hashlib
# import json
import os
# import re
# import sys
import threading

# import uuid
#

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
    _sha256 = hashlib.sha256()

    if hasattr(data, 'read'):
        for chunk in iter(lambda: data.read(8192), b''):
            _md5.update(chunk)
            _sha256.update(chunk)
    else:
        _md5.update(data)
        _sha256.update(data)
    return _md5.hexdigest(), _sha256.hexdigest()


def _get_file_hashes(filename):
    (_md5, _sha256) = (None, None)
    with open(filename, 'rb') as file_obj:
        (_md5, _sha256) = _calculate_data_hashes(file_obj)

    return _md5, _sha256


def _hashes_up_to_date(md5, sha256, md5_key, sha256_key):
    '''Compare md5 and sha256 hashes for being up to date
    md5 and sha256 are the current values.
    md5_key and sha256_key are the previous values.
    '''
    up_to_date = False
    if md5 and md5_key == md5:
        up_to_date = True
    if sha256 and sha256_key == sha256:
        up_to_date = True
    if md5 and md5_key != md5:
        up_to_date = False
    if sha256 and sha256_key != sha256:
        up_to_date = False
    return up_to_date
