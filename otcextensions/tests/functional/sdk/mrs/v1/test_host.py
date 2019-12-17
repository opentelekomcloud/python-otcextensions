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

from otcextensions.tests.functional import base

_logger = openstack._log.setup_logging('openstack')


class TestHost(base.BaseFunctionalTest):

    @classmethod
    def setUpClass(cls):
        super(TestHost, cls).setUpClass()
        openstack.enable_logging(debug=True, http_debug=True)
        cls.client = cls.conn.mrs
        # res = cls.client.create_host(
        #     name=uuid.uuid4().hex,
        #     availability_zone='eu-de-01',
        #     host_type='general',
        #     quantity=1
        # )
        # assert len(res.dedicated_host_ids) == 1
        # host_id = res.dedicated_host_ids[0]
        # cls.host = cls.client.get_host(host_id)

    @classmethod
    def tearDownClass(cls):
        try:
            pass
            # if cls.cluster.id:
            #     pass
            #     cls.client.delete_cluster(cls.cluster)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_list(self):
        self.clusters = list(self.conn.mrs.clusters())
        self.assertGreaterEqual(len(self.clusters), 0)
        if len(self.clusters) > 0:
            cluster = self.clusters[0]
            servers = self.client.hosts(cluster_id=cluster.id)
            for server in servers:
                _logger.debug(server)

    # def test_host_types(self):
    #     mrs = self.conn.mrs
    #     host_types = list(deh.host_types('eu-de-01'))
    #     self.assertIsNotNone(host_types)
    #     _logger.debug(host_types)
