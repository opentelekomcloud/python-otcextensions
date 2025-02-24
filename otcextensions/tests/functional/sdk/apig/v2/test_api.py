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


class TestApi(TestApiG):
    environment = None

    def setUp(self):
        super(TestApi, self).setUp()
        self.create_gateway()
        self.gateway_id = TestApi.gateway.id
        # self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"

        group_attrs = {
            "name": "api_group_001",
            "remark": "API group 1"
        }
        self.group = self.client.create_api_group(
            gateway=self.gateway_id,
            **group_attrs
        )
        self.assertIsNotNone(self.group.id)

        self.attrs = {
            "group_id": self.group.id,
            "name": "test_api_001",
            "auth_type": "IAM",
            "backend_type": "HTTP",
            "req_protocol": "HTTP",
            "req_uri": "/test/http",
            "remark": "Mock backend API",
            "type": 2,
            "req_method": "GET",
            "result_normal_sample": "Example success response",
            "result_failure_sample": "Example failure response",
            "tags": ["httpApi"],
            "backend_api": {
                "req_protocol": "HTTP",
                "req_method": "GET",
                "req_uri": "/test/benchmark",
                "timeout": 5000,
                "retry_count": "-1",
                "url_domain": "192.168.189.156:12346"
            },
        }
        self.api = self.client.create_api(
            gateway=self.gateway_id,
            **self.attrs
        )
        self.environment = self.client.create_environment(
            gateway=self.gateway_id,
            name="testPub",
            remark="test publish"
        )

        self.addCleanup(
            self.client.delete_api_group,
            gateway=self.gateway_id,
            api_group=self.group.id,
        )
        self.addCleanup(
            self.client.delete_api,
            gateway=self.gateway_id,
            api=self.api
        )
        self.addCleanup(
            self.client.delete_environment,
            gateway=self.gateway_id,
            environment=self.environment,
        )
        self.addCleanup(self.delete_gateway())

    def test_list_apis(self):
        a = list(self.client.apis(
            gateway=self.gateway_id))
        self.assertGreaterEqual(len(a), 1)

    def test_get_api(self):
        api = self.client.get_api(
            gateway=self.gateway_id,
            api=self.api.id)
        self.assertEqual(api.id, self.api.id)

    def test_update_api(self):
        self.attrs.update({
            "name": "test_api_001_updated",
            "type": 1,
            "req_method": "POST",
            "req_protocol": "HTTPS"
        })
        updated = self.client.update_api(
            gateway=self.gateway_id,
            api=self.api.id,
            **self.attrs
        )
        self.assertEqual(updated.name, self.attrs["name"])
        self.assertEqual(updated.type, self.attrs["type"])
        self.assertEqual(updated.req_method, self.attrs["req_method"])
        self.assertEqual(updated.req_protocol, self.attrs["req_protocol"])

    def test_online_offline_api(self):
        publish = self.client.publish_api(
            gateway=self.gateway_id,
            api=self.api.id,
            env=self.environment,
            remark="publish"
        )
        self.assertEqual(publish.api_name, self.api.name)
        self.assertEqual(publish.remark, "publish")

        offline = self.client.offline_api(
            gateway=self.gateway_id,
            api=self.api.id,
            env=self.environment,
            remark="offline"
        )
        self.assertEqual(offline.api_name, self.api.name)
        self.assertEqual(offline.remark, "offline")

    def test_check_api(self):
        attrs = {
            "type": "name",
            "name": self.api.name
        }
        check = self.client.check_api(
            gateway=self.gateway_id,
            **attrs
        )
        self.assertIsNotNone(check)

    def test_debug_api(self):
        attrs = {
            "mode": "DEVELOPER",
            "scheme": "HTTP",
            "method": "GET",
            "path": "/test/http"
        }
        debug = self.client.debug_api(
            gateway=self.gateway_id,
            api=self.api.id,
            **attrs
        )
        self.assertIsNotNone(debug)

    def test_online_offline_apis(self):
        publish = self.client.publish_apis(
            gateway=self.gateway_id,
            env=self.environment,
            remark="publish",
            apis=[self.api.id]
        )
        self.assertIsNotNone(publish)
        self.assertEqual(publish.success[0]["api_id"], self.api.id)

        offline = self.client.offline_apis(
            gateway=self.gateway_id,
            env=self.environment,
            remark="offline",
            apis=[self.api.id]
        )
        self.assertIsNotNone(offline)
        self.assertEqual(offline.success[0]["api_id"], self.api.id)

    def test_list_api_versions(self):
        versions = list(self.client.api_versions(
            gateway=self.gateway_id,
            api=self.api.id))
        self.assertIsNotNone(versions)

    def test_switch_api_versions(self):
        publish = self.client.publish_api(
            gateway=self.gateway_id,
            api=self.api.id,
            env=self.environment,
            remark="publish"
        )
        self.assertIsNotNone(publish)

        switch = self.client.switch_version(
            gateway=self.gateway_id,
            api=self.api.id,
            version_id=publish.version_id
        )
        self.assertIsNotNone(switch)

        offline = self.client.offline_api(
            gateway=self.gateway_id,
            env=self.environment,
            remark="offline",
            api=self.api.id,
        )
        self.assertIsNotNone(offline)

    # def test_list_runtime_definitions(self):
    #     definitions = list(self.client.api_runtime_definitions(
    #         gateway=self.gateway_id,
    #         api=self.api.id,
    #         env_id=self.environment.id
    #     ))
    #     self.assertIsNotNone(definitions)

    def test_list_api_version_details(self):
        publish = self.client.publish_api(
            gateway=self.gateway_id,
            api=self.api.id,
            env=self.environment,
            remark="publish"
        )
        self.assertIsNotNone(publish)

        details = list(self.client.api_version_details(
            gateway=self.gateway_id,
            version_id=publish.version_id
        ))
        self.assertIsNotNone(details)

        offline_version = self.client.take_api_version_offline(
            gateway=self.gateway_id,
            version_id=publish.version_id
        )
        self.assertIsNotNone(offline_version)
