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


class TestApp(TestApiG):
    app = None

    def setUp(self):
        super(TestApp, self).setUp()
        self.create_gateway()
        self.gateway_id = TestApp.gateway.id
        self.attrs = {
            "name": "app_demo",
            "remark": "Demo app"
        }
        TestApp.app = self.client.create_app(self.gateway_id, **self.attrs)
        self.assertIsNotNone(self.app.id)
        self.addCleanup(
            self.client.delete_app,
            gateway=self.gateway_id,
            app=TestApp.app.id,
        )

    def test_get_app(self):
        found = self.client.get_app(
            gateway=self.gateway_id,
            app=TestApp.app.id)
        self.assertEqual(found.id, TestApp.app.id)

    def test_list_apps(self):
        found = list(self.client.apps(gateway=self.gateway_id))
        self.assertEqual(len(found), 1)

    def test_update_app(self):
        test_remark = "Demo app changed"
        attrs = {
            "name": "app_demo",
            "remark": test_remark
        }
        result = self.client.update_app(
            gateway=self.gateway_id,
            app=TestApp.app.id,
            **attrs
        )
        self.assertEqual(result.remark, test_remark)

    def test_verify_app(self):
        result = self.client.verify_app(
            gateway=self.gateway_id,
            app=TestApp.app.id,
        )
        self.assertEqual(result.id, TestApp.app.id)

    def test_reset_app_secret(self):
        self.client.reset_app_secret(
            gateway=self.gateway_id,
            app=TestApp.app.id,
        )
