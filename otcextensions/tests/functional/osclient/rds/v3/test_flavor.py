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

import json
import uuid

from openstackclient.tests.functional import base


class TestRdsFlavor(base.TestCase):
    """Functional tests for RDS Flavor. """

    NAME = uuid.uuid4().hex
    OTHER_NAME = uuid.uuid4().hex

    def test_flavor_list(self):
        json_output = json.loads(self.openstack(
            'rds datastore version list postgresql -f json '
        ))
        ver = json_output[0]['Name']

        json_output = json.loads(self.openstack(
            'rds flavor list postgresql {ver} -f json '.format(
                ver=ver)
        ))

        self.assertIsNotNone(json_output)
