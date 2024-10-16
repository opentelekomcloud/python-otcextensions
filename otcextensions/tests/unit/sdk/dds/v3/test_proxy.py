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
from otcextensions.sdk.dds.v3 import datastore as _datastore
from otcextensions.sdk.dds.v3 import instance as _instance
from otcextensions.sdk.dds.v3 import flavor as _flavor


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
            _datastore.Datastore,
            method_kwargs={
                'datastore_name': 'foo'},
            expected_kwargs={
                'datastore_name': 'foo'
            }
        )


class TestFlavor(TestDdsProxy):
    def test_flavors(self):
        self.verify_list(
            self.proxy.flavors,
            _flavor.Flavor,
            method_kwargs={
                'region': 'foo',
                'engine_name': 'engine',
            },
            expected_kwargs={
                'region': 'foo',
                'engine_name': 'engine',
            }
        )


class TestInstance(TestDdsProxy):
    def test_get_instance(self):
        self.verify_get(
            self.proxy.get_instance,
            _instance.Instance
        )

    def test_create_instance(self):
        self.verify_create(
            self.proxy.create_instance,
            _instance.Instance,)
