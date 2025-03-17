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


class TestAppCode(TestApiG):
    app = None
    code = None

    def setUp(self):
        super(TestAppCode, self).setUp()
        self.create_gateway()
        self.gateway_id = TestAppCode.gateway.id
        self.attrs = {
            "name": "app_demo",
            "remark": "Demo app"
        }
        TestAppCode.app = self.client.create_app(self.gateway_id, **self.attrs)
        self.addCleanup(
            self.client.delete_app,
            gateway=self.gateway_id,
            app=TestAppCode.app.id,
        )
        attrs = {
            "app_code": "GjOD3g80AABuuFeEJpVQADBlAjBh3UzC7W+gr4VJBB5BtJ4f"
                        "dVOQoSvoji3gFxUDb5pWBz9wUcw9+8/bFZ1B/4pq29wCMQC0"
                        "pQWX6zTndljDEl99As1pw+WntAU9xcq+ffagoH6zDpKUvdxV"
                        "6Ezj8LcCcPZN6BU="
        }
        TestAppCode.code = self.client.create_app_code(self.gateway_id,
                                                       TestAppCode.app.id,
                                                       **attrs)
        self.assertIsNotNone(TestAppCode.code.id)
        self.addCleanup(
            self.client.delete_app_code,
            gateway=self.gateway_id,
            app=TestAppCode.app.id,
            app_code=TestAppCode.code.id,
        )

    def test_generate_code(self):
        code = self.client.generate_app_code(gateway=TestAppCode.gateway.id,
                                             app=TestAppCode.app.id)
        self.assertIsNotNone(code.id)
        TestAppCode.code = code

    def test_get_code(self):
        code = self.client.get_app_code(gateway=TestAppCode.gateway.id,
                                        app=TestAppCode.app.id,
                                        app_code=TestAppCode.code.id)
        self.assertIsNotNone(code.app_code)

    def test_app_codes(self):
        codes = self.client.app_codes(gateway=TestAppCode.gateway.id,
                                      app=TestAppCode.app.id)
        self.assertEqual(len(list(codes)), 1)
