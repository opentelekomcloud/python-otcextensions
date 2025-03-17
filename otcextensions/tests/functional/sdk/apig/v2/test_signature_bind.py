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
import uuid

from otcextensions.tests.functional.sdk.apig import TestApiG


class TestSignature(TestApiG):
    def setUp(self):
        super(TestSignature, self).setUp()
        self.suffix = uuid.uuid4().hex[:4]

        self.create_gateway()
        self.gateway_id = TestSignature.gateway.id
        # self.gateway_id = "be76ca6de5fe4aa7af503c03b3b44dea"

        group_attrs = {
            "name": f"api_group_{self.suffix}",
            "remark": "API group 1"
        }
        self.group = self.client.create_api_group(
            gateway=self.gateway_id,
            **group_attrs
        )
        self.assertIsNotNone(self.group.id)

        api_attrs = {
            "group_id": self.group.id,
            "name": f"test_api_{self.suffix}",
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
            **api_attrs
        )
        self.environment = self.client.create_environment(
            gateway=self.gateway_id,
            name=f"testPub{self.suffix}",
            remark="test publish"
        )
        self.publish = self.client.publish_api(
            gateway=self.gateway_id,
            api=self.api.id,
            env=self.environment,
            remark="publish"
        )

        sign_attrs = {
            "name": f"otce_signature_{self.suffix}",
            "sign_type": "aes",
            "sign_algorithm": "aes-256-cfb",
        }
        self.sign = self.client.create_signature(
            gateway=self.gateway_id,
            **sign_attrs
        )

        self.attrs = {
            "sign_id": self.sign.id,
            "publish_ids": [self.publish.publish_id]
        }
        self.bind = self.client.bind_signature(
            gateway=self.gateway_id,
            **self.attrs
        )

        self.addCleanup(
            self.client.delete_api_group,
            gateway=self.gateway_id,
            api_group=self.group.id,
        )
        self.addCleanup(
            self.client.delete_environment,
            gateway=self.gateway_id,
            environment=self.environment,
        )
        self.addCleanup(
            self.client.delete_signature,
            gateway=self.gateway_id,
            sign=self.sign
        )
        self.addCleanup(
            self.client.delete_api,
            gateway=self.gateway_id,
            api=self.api
        )
        self.addCleanup(
            self.client.offline_api,
            gateway=self.gateway_id,
            api=self.api.id,
            env=self.environment,
            remark="offline"
        )
        self.addCleanup(
            self.client.unbind_signature,
            gateway=self.gateway_id,
            bind=self.bind.bindings[0].id
        )

        self.addCleanup(self.delete_gateway())

    def test_list_bound_signatures(self):
        sign = list(self.client.bound_signatures(
            gateway=self.gateway_id,
            api_id=self.api.id
        ))
        self.assertEqual(len(sign), 1)

    def test_list_bound_apis(self):
        sign = list(self.client.bound_apis(
            gateway=self.gateway_id,
            sign_id=self.sign.id
        ))
        self.assertEqual(len(sign), 1)

    def test_list_not_bound_apis(self):
        sign = list(self.client.not_bound_apis(
            gateway=self.gateway_id,
            sign_id=self.sign.id
        ))
        self.assertEqual(len(sign), 0)
