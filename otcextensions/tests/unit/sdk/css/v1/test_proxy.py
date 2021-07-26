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

from otcextensions.sdk.css.v1 import _proxy
from otcextensions.sdk.css.v1 import flavor as _flavor
from otcextensions.sdk.css.v1 import cluster as _cluster

from openstack.tests.unit import test_proxy_base


class TestCssSProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestCssSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_clusters(self):
        self.verify_list(self.proxy.clusters, _cluster.Cluster)

    def test_get_cluster(self):
        self.verify_get(self.proxy.get_cluster, _cluster.Cluster)

    def test_create_cluster(self):
        self.verify_create(
            self.proxy.create_cluster, _cluster.Cluster,
            method_kwargs={'x': 1, 'y': 2, 'z': 3},
            expected_kwargs={
                'prepend_key': False,
                'x': 1, 'y': 2, 'z': 3
            }
        )

    def test_delete_cluster(self):
        self.verify_delete(
            self.proxy.delete_cluster, _cluster.Cluster, True
        )

    def test_flavors(self):
        self.verify_list(
            self.proxy.flavors,
            _flavor.Flavor,
        )
