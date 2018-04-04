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

from otcextensions.sdk.cce.v1 import _proxy
from otcextensions.sdk.cce.v1 import cluster as _cluster


class TestCCEProxy(test_proxy_base.TestProxyBase):
    HEADERS = {
        'Content-Type': 'application/json'
    }

    def setUp(self):
        super(TestCCEProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestCCECluster(TestCCEProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.clusters, _cluster.Cluster,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={},
            paginated=True,
            expected_kwargs={
                'headers': self.HEADERS
            }
        )

    def test_get(self):
        self.verify_get(
            self.proxy.get_cluster,
            _cluster.Cluster,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={
                'headers': self.HEADERS
            }
        )

    # def test_find(self):
    #     self._verify2(
    #         'otcextensions.sdk.sdk_proxy.Proxy._find',
    #         self.proxy.find_cluster,
    #         method_args=["flavor"],
    #         expected_args=[_cluster.Cluster, "flavor"],
    #         expected_kwargs={
    #             "ignore_missing": True})

    # def test_create(self):
    #     self.verify_create(
    #         self.proxy.create_cluster, _cluster.Cluster,
    #         mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
    #         method_kwargs={
    #             'instance': 'test',
    #             'name': 'some_name'
    #         },
    #         expected_kwargs={
    #             'prepend_key': False,
    #             'instance': 'test',
    #             'name': 'some_name'
    #         }
    #     )

    def test_delete(self):
        self.verify_delete(
            self.proxy.delete_cluster,
            _cluster.Cluster, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={
                'headers': self.HEADERS
            }
        )
