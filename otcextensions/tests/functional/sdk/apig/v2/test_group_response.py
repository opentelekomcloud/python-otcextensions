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


class TestGroupResponse(TestApiG):
    gateway_id = "560de602c9f74969a05ff01d401a53ed"
    group_id = "ce973ff83ce54ef192c80bde884aa0ac"
    response_id = '0bcaa1fd92984d2d86dfc207bd3f3bcd'

    def setUp(self):
        super(TestGroupResponse, self).setUp()
        attrs = {
            "name": "test_group_response",
            "responses": {
                "NOT_FOUND": {
                    "status": 404,
                    "body": "Bad Request",
                    "headers": [{
                        "key": "Content-Type",
                        "value": "application/json",
                    }]
                }
            }
        }
        try:
            group_response = self.client.create_group_response(
                gateway=TestGroupResponse.gateway_id,
                group=TestGroupResponse.group_id,
                **attrs
            )
            print("Created Group Response:", group_response)
            TestGroupResponse.response_id = group_response.id
            self.addCleanup(
                self.client.delete_group_response,
                gateway=TestGroupResponse.gateway_id,
                group=TestGroupResponse.group_id,
                response=group_response.id
            )
        except Exception as e:
            print("Failed to create group response:", e)

    def tearDown(self):
        super(TestGroupResponse, self).tearDown()

    def test_get_group_response_list(self):
        response_list = list(self.client.group_responses(
            gateway=TestGroupResponse.gateway_id,
            group=TestGroupResponse.group_id))
        print(response_list)

    def test_update_response(self):
        check = "response_demo"
        attrs = {
            "name": check
        }
        updated = self.client.update_group_response(
            gateway=TestGroupResponse.gateway_id,
            group=TestGroupResponse.group_id,
            response=TestGroupResponse.response_id,
            **attrs
        )
        self.assertEqual(check, updated.name)

    def test_get_response(self):
        response = self.client.get_group_response(
            gateway=TestGroupResponse.gateway_id,
            group=TestGroupResponse.group_id,
            response=TestGroupResponse.response_id
        )
        print("Fetched Group Response:", response)
        self.assertEqual(TestGroupResponse.response_id, response.id)

    def test_error_response(self):
        error_response = self.client.get_error_response(
            gateway=TestGroupResponse.gateway_id,
            group=TestGroupResponse.group_id,
            response=TestGroupResponse.response_id,
            response_type='NOT_FOUND'
        )
        print(error_response)

    def test_update_error_response(self):
        check = "response_demo"
        attrs = {
            "status": 403,
            "body": "{\"error_code\": \"$context.error.code\", "
                    "\"error_msg\": \"$context.error.message\"}"
        }
        updated = self.client.update_error_response(
            gateway=TestGroupResponse.gateway_id,
            group=TestGroupResponse.group_id,
            response=TestGroupResponse.response_id,
            response_type='NOT_FOUND',
            **attrs
        )
        self.assertEqual(check, updated.name)

    def test_delete_error_response(self):
        response = self.client.delete_error_response(
            gateway=TestGroupResponse.gateway_id,
            group=TestGroupResponse.group_id,
            response=TestGroupResponse.response_id,
            response_type='NOT_FOUND'
        )
        print("Deleted Error Response:", response)
        self.assertIsNone(response)
