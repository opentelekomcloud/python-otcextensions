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
import openstack

from otcextensions.tests.functional.sdk.mrs import TestMrs

_logger = openstack._log.setup_logging('openstack')


class TestHost(TestMrs):

    def test_list(self):
        self.clusters = list(self.client.clusters())
        self.assertGreaterEqual(len(self.clusters), 0)
        if len(self.clusters) > 0:
            cluster = self.clusters[0]
            servers = self.client.hosts(cluster_id=cluster.id)
            for server in servers:
                _logger.debug(server)
