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


class TestAccessControl(TestApiG):
    app = None

    def setUp(self):
        super(TestAccessControl, self).setUp()
        self.create_gateway()
        self.gateway_id = TestAccessControl.gateway.id
        self.attrs = {
            "name": "app_demo",
            "remark": "Demo app"
        }
        TestAccessControl.app = self.client.create_app(self.gateway_id,
                                                       **self.attrs)
        self.assertIsNotNone(self.app.id)
        self.addCleanup(
            self.client.delete_app,
            gateway=self.gateway_id,
            app=TestAccessControl.app.id,
        )

    def test_configure_access_control(self):
        attrs = {
            "app_acl_type": "PERMIT",
            "app_acl_values": ["192.168.0.1",
                               "192.168.0.5-192.168.0.10",
                               "192.168.0.100/28"]
        }
        configured = self.client.configure_access_control(
            gateway=TestAccessControl.gateway.id,
            app=TestAccessControl.app.id,
            **attrs)
        self.assertIsNotNone(configured.app_id)

    def test_query_access_control(self):
        found = self.client.access_controls(
            gateway=TestAccessControl.gateway.id,
            app=TestAccessControl.app.id)
        self.assertIsNotNone(found)

    def test_delete_access_control(self):
        self.client.delete_access_control(
            gateway=TestAccessControl.gateway.id,
            app=TestAccessControl.app.id)
        found = self.client.access_controls(
            gateway=TestAccessControl.gateway.id,
            app=TestAccessControl.app.id)
        self.assertIsNotNone(found)
