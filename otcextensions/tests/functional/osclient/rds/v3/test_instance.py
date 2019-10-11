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

import uuid

from openstackclient.tests.functional import base


class TestRdsInstance(base.TestCase):
    """Functional tests for RDS Instance. """

    NAME = uuid.uuid4().hex
    OTHER_NAME = uuid.uuid4().hex

    def test_instance_list(self):
        self.openstack(
            'rds instance list -f json '
        )

    def test_instance_list_filters(self):
        self.openstack(
            'rds instance list '
            '--limit 1 --id 2 '
            '--name 3 --type Single '
            '--database PostgreSQL '
            '--router_id 123asd --subnet_id 123qwe '
            '--offset 5'
        )

        self.assertTrue(True)
