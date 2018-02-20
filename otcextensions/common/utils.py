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
# import hashlib
# import json
import os
# import re
# import six.moves.urllib.parse as urlparse
# import sys
import threading
# import uuid
#
# import six

if os.name == 'nt':
    import msvcrt
else:
    msvcrt = None

# from oslo_utils import encodeutils
# from oslo_utils import strutils
# import prettytable
# import wrapt


_memoized_property_lock = threading.Lock()

SENSITIVE_HEADERS = ('X-Auth-Token', )
REQUIRED_FIELDS_ON_DATA = ('disk_format', 'container_format')
