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
from enum import Enum

# from openstackclient.i18n import _


class ObsError(Enum):
    ERROR_INTERNAL = (1, "Internal error")
    ERROR_S3_SOURCE_MISSING = (404, 'Requested Object with key %s not found')
    ERROR_SOURCE_NOT_AVAILABLE = (123, 'Source %s is not available')

    def __init__(self, code, message, **kwargs):
        self.code = code
        self.message = message

    def get_formatted(self, args):
        self.message = self.message % args
        return self


class ObsException(Exception):
    def __init__(self, obs_error):
        self.code = obs_error.code
        self.message = obs_error.message
