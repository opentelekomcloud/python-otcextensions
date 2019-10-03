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

from otcextensions.sdk.rds.v3 import _proxy
from otcextensions.sdk.rds.v3 import flavor

from openstack.tests.unit import test_proxy_base


class TestRdsProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestRdsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestRdsFlavor(TestRdsProxy):
    def test_flavors(self):
        self.verify_list(self.proxy.flavors,
                         flavor.Flavor,
                         method_kwargs={
                             'datastore_name': 'MySQL',
                             'version_name': '5.7'
                         },
                         expected_kwargs={
                             'datastore_name': 'MySQL',
                             'version_name': '5.7'
                         })
