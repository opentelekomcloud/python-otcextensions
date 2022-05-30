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
from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.dds.v3 import _proxy
from otcextensions.sdk.dds.v3 import datastore


class TestDdsProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestDdsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestDatastore(TestDdsProxy):
    def test_datastore_types(self):
        res = list(self.proxy.datastore_types())
        self.assertEqual('DDS-Community', res[0].name)

    def test_datastores(self):
        self.verify_list(
            self.proxy.datastores,
            datastore.Datastore,
            method_kwargs={
                'datastore_name': 'foo'},
            expected_kwargs={
                'datastore_name': 'foo'
            }
        )
