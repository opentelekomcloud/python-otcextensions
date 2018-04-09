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
from openstack import _log
# from openstack import exceptions
from otcextensions.tests.functional import base

# from otcextensions.i18n import _

_logger = _log.setup_logging('openstack')


class TestCluster(base.BaseFunctionalTest):
    TEST_CLUSTER = '5a66a449-668c-492f-8c33-5cdbdeaadd2e'

    def setUp(self):
        super(TestCluster, self).setUp()
        self.cce = self.conn.cce

    def test_list(self):

        objects = list(self.cce.clusters())

        for obj in objects:
            self.assertIsNotNone(obj.id)

        self.assertGreaterEqual(len(objects), 0)

    def test_get(self):
        obj = self.cce.get_cluster(self.TEST_CLUSTER)

        self.assertIsNotNone(obj.id)

        print(obj.to_dict())
        print('id=%s' % obj.id)
        print('name=%s' % obj.metadata.name)
        self.assertIsNotNone(obj)
