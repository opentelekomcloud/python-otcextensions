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

from otcextensions.sdk.vpc.v2 import _proxy
from otcextensions.sdk.vpc.v2 import peering

from openstack.tests.unit import test_proxy_base


class TestVpcProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestVpcProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestVpcPeering(TestVpcProxy):
    def test_peering_create(self):
        self.verify_create(self.proxy.create_peering, peering.Peering,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_peering_delete(self):
        self.verify_delete(self.proxy.delete_peering,
                           peering.Peering, True)

    def test_peering_get(self):
        self.verify_get(self.proxy.get_peering, peering.Peering)

    def test_peerings(self):
        self.verify_list(self.proxy.peerings, peering.Peering)

    def test_peering_update(self):
        self.verify_update(self.proxy.update_peering, peering.Peering)

    def test_set_peering(self):
        self._verify(
            'otcextensions.sdk.vpc.v2.peering.Peering._set_peering',
            self.proxy.set_peering,
            method_args=[peering.Peering],
            method_kwargs={'set_status': 'accept'},
            expected_args=['accept']
        )
