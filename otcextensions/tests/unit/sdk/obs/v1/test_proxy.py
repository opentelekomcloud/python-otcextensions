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

from otcextensions.sdk.obs.v1 import _proxy
# from otcextensions.sdk.obs.v1 import bucket as _bucket
# from otcextensions.sdk.obs.v1 import object as _object


class TestObsProxy(test_proxy_base.TestProxyBase):

    PROJECT_ID = '123'

    def setUp(self):
        super(TestObsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        self.session.get_project_id.side_effect = [TestObsProxy.PROJECT_ID]

    def test_normalize_keys(self):
        # TODO(agoncharov)
        pass

    def test_set_ak(self):
        # TODO(agoncharov)
        pass

    def test_get_endpoint(self):
        # TODO(agoncharov)
        pass

    def test_establish_session(self):
        # TODO(agoncharov)
        pass

    def test_get_session(self):
        # TODO(agoncharov)
        pass

    def test_buckets(self):
        # TODO(agoncharov)
        pass

    def test_get_bucket(self):
        # TODO(agoncharov)
        pass

    def test_get_bucket_by_name(self):
        # TODO(agoncharov)
        pass

    def test_create_bucket(self):
        # TODO(agoncharov)
        pass

    def test_object(self):
        # TODO(agoncharov)
        pass

    def test_get_object_by_key(self):
        # TODO(agoncharov)
        pass

    def test_get_object(self):
        # TODO(agoncharov)
        pass

    def test_create_object(self):
        # TODO(agoncharov)
        pass

    def test_download_object(self):
        # TODO(agoncharov)
        pass

    def test_head_bucket(self):
        # TODO(agoncharov)
        pass

    def test_head_object(self):
        # TODO(agoncharov)
        pass
