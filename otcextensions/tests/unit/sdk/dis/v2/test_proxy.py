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

from otcextensions.sdk.dis.v2 import _proxy
from otcextensions.sdk.dis.v2 import stream

from openstack.tests.unit import test_proxy_base


class TestDisProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestDisProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestStream(TestDisProxy):

    def test_stream_create(self):
        self.verify_create(self.proxy.create_stream, stream.Stream,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})
