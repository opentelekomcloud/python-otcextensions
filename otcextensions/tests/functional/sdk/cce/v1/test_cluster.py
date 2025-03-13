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

from otcextensions.tests.functional.sdk.cce import TestCce

_logger = _log.setup_logging('openstack')


class TestCluster(TestCce):
    def setUp(self):
        super(TestCluster, self).setUp()
        self.create_network()
        self.create_cluster()
        self.addCleanup(self._destroy_network)
        self.addCleanup(
            self.conn.delete_cce_cluster,
            cluster=TestCce.cluster.id
        )

    def test_list(self):

        objects = list(self.client.clusters())

        for obj in objects:
            self.assertIsNotNone(obj.id)

        self.assertGreaterEqual(len(objects), 0)
