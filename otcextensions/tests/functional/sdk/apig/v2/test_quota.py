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

from otcextensions.tests.functional.sdk.apig import TestApiG


class TestQuota(TestApiG):
    app = None

    def setUp(self):
        super(TestQuota, self).setUp()
        self.create_gateway()
        self.gateway_id = TestQuota.gateway.id
        self.attrs = {
            "name": "app_demo",
            "remark": "Demo app"
        }
        TestQuota.app = self.client.create_app(self.gateway_id, **self.attrs)
        self.assertIsNotNone(self.app.id)
        self.addCleanup(
            self.client.delete_app,
            gateway=self.gateway_id,
            app=TestQuota.app.id,
        )

    def test_quotas(self):
        found = self.client.quotas(gateway=TestQuota.gateway.id,
                                   app=TestQuota.app.id,)
        self.assertIsNotNone(found)
