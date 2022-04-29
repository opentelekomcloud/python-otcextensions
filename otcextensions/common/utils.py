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

import hashlib
# import errno
# import functools
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
