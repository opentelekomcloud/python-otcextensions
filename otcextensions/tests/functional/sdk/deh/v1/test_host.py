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
import uuid
import openstack

from otcextensions.tests.functional import base

_logger = openstack._log.setup_logging('openstack')


class TestHost(base.BaseFunctionalTest):

    def setUp(self):
        super(TestHost, self).setUp()
        openstack.enable_logging(debug=True, http_debug=True)
        self.client = self.conn.deh
        res = self.client.create_host(
            name=uuid.uuid4().hex,
            availability_zone='eu-de-01',
            host_type='general',
            quantity=1
        )
        assert len(res.dedicated_host_ids) == 1
        host_id = res.dedicated_host_ids[0]
        self.host = self.client.get_host(host_id)

    def tearDown(self):
        try:
            if self.host.id:
                self.client.delete_host(self.host)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_list(self):
        self.hosts = list(self.conn.deh.hosts())
        self.assertGreaterEqual(len(self.hosts), 0)
        if len(self.hosts) > 0:
            host = self.hosts[0]
            servers = self.client.servers(host=host.id)
            for server in servers:
                _logger.debug(server)

    def test_host_types(self):
        deh = self.conn.deh

        host_types = list(deh.host_types('eu-de-01'))

        self.assertIsNotNone(host_types)
        _logger.debug(host_types)
