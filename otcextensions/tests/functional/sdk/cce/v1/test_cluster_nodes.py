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


class TestClusterNodes(base.BaseFunctionalTest):

    TEST_CLUSTER = '5a66a449-668c-492f-8c33-5cdbdeaadd2e'

    def setUp(self):
        super(TestClusterNodes, self).setUp()
        self.cce = self.conn.cce

    def test_list_nodes(self):
        cluster = self.cce.get_cluster(self.TEST_CLUSTER)
        nodes = list(self.cce.cluster_nodes(cluster))

        self.assertGreaterEqual(len(nodes), 0)

    def test_get_node(self):
        cluster = self.cce.get_cluster(self.TEST_CLUSTER)
        nodes = list(self.cce.cluster_nodes(cluster))
        node = self.cce.get_cluster_node(cluster, nodes[0].id)

        self.assertIsNotNone(node)
