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

from otcextensions.sdk.imsv1.v1 import _proxy
from otcextensions.sdk.imsv1.v1 import async_job


class TestImsProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestImsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestImsAsyncJob(TestImsProxy):

    def test_async_job_get(self):
        self._verify('openstack.proxy.Proxy._get',
                     self.proxy.get_async_job,
                     expected_args=[async_job.AsyncJob],
                     method_kwargs={
                         'job_id': '1'
                     })
