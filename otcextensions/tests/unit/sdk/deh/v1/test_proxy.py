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
from otcextensions.sdk.deh.v1 import _proxy
from otcextensions.sdk.deh.v1 import host as _host
from otcextensions.sdk.deh.v1 import host_type as _host_type
from otcextensions.sdk.deh.v1 import server as _server

from openstack.tests.unit import test_proxy_base


class TestDehProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestDehProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_hosts(self):
        self.verify_list(
            self.proxy.hosts, _host.Host,
            expected_kwargs={
            }
        )

    def test_get_host(self):
        self.verify_get(
            self.proxy.get_host, _host.Host,
        )

    def test_find_host(self):
        self.verify_find(
            self.proxy.find_host, _host.Host,
        )

    def test_create_host(self):
        self.verify_create(
            self.proxy.create_host, _host.Host,
            method_kwargs={
                'x': 1,
                'y': '2'
            },
            expected_kwargs={
                'prepend_key': False,
                'x': 1,
                'y': '2'
            }
        )

    def test_delete_host(self):
        self.verify_delete(
            self.proxy.delete_host,
            _host.Host,
            ignore_missing=True,
        )

    def test_update_host(self):
        self.verify_update(
            self.proxy.update_host, _host.Host,
        )

    def test_servers(self):
        self.verify_list(
            self.proxy.servers, _server.Server,
            method_args=[{'id': 'host_id'}],
            method_kwargs={},
            expected_kwargs={
                'dedicated_host_id': 'host_id'
            },
            expected_args=[]
        )

    def test_host_types(self):
        self.verify_list(
            self.proxy.host_types, _host_type.HostType,
            method_args=['az'],
            method_kwargs={},
            expected_kwargs={
                'paginated': False,
                'availability_zone': 'az'
            },
            expected_args=[]
        )
