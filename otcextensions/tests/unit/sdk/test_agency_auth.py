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

import copy
import json
import time
import uuid

from keystoneauth1 import _utils as ksa_utils
from keystoneauth1 import access
from keystoneauth1 import exceptions
from keystoneauth1 import fixture
from keystoneauth1.identity import v3
from keystoneauth1.identity.v3 import base as v3_base
from keystoneauth1 import session
from keystoneauth1.tests.unit.identity import utils

from otcextensions.sdk import agency_auth


class AgencyTest(utils.GenericPluginTestCase):

    PLUGIN_CLASS = agency_auth.Agency
    V3_PLUGIN_CLASS = v3.Password

    def new_plugin(self, **kwargs):
        kwargs.setdefault('username', uuid.uuid4().hex)
        kwargs.setdefault('password', uuid.uuid4().hex)
        return super(AgencyTest, self).new_plugin(**kwargs)


