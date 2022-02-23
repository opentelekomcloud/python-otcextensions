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

from otcextensions.sdk.sdrs.v1 import _proxy

from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.sdrs.v1 import job as _job


class TestSDRSProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestSDRSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestSDRSJob(TestSDRSProxy):

    def test_get_job(self):
        self.verify_get(self.proxy.get_job, _job.Job)
