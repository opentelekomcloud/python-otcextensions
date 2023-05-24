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

from otcextensions.sdk.sfsturbo.v1 import _proxy
from otcextensions.sdk.sfsturbo.v1 import share

from openstack.tests.unit import test_proxy_base


class TestSfstProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestSfstProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_peering_create(self):
        self.verify_create(self.proxy.create_share, share.Share,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_share_get(self):
        self.verify_get(self.proxy.get_share, share.Share)

    def test_shares(self):
        self.verify_list(self.proxy.shares, share.Share)

    def test_share_delete(self):
        self.verify_delete(
            self.proxy.delete_share, share.Share, True,
            mock_method='otcextensions.sdk.sfsturbo.v1._proxy.Proxy._delete',
            expected_kwargs={
                'ignore_missing': True
            })
