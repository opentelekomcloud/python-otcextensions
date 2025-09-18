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

from otcextensions.sdk.ims.v2 import _proxy
from otcextensions.sdk.ims.v2 import image


class TestImsProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestImsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestImsImage(TestImsProxy):
    def test_image_create(self):
        self.verify_create(self.proxy.create_image,
                           image.Image)
