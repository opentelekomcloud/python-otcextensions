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
import json


class TestExportApi(TestApiG):
    gateway = '560de602c9f74969a05ff01d401a53ed'

    def setUp(self):
        super(TestExportApi, self).setUp()

    def test_export_api(self):
        attrs = {
            "env_id": "DEFAULT_ENVIRONMENT_RELEASE_ID",
            "group_id": "ce973ff83ce54ef192c80bde884aa0ac",
            "define": "all"
        }
        self.client.export_api(
            gateway=TestExportApi.gateway,
            full_path='/mnt/c/Users/sand1/api',
            **attrs
        )

    def test_import_api(self):
        with (open('/mnt/c/Users/sand1/PycharmProjects/python-otcextensions/'
                   'otcextensions/tests/functional/sdk/apig/v2/test.json',
                   'r') as f):
            openapi_content = json.load(f)
        attrs = {
            "is_create_group": False,
            "group_id": "ce973ff83ce54ef192c80bde884aa0ac",
            "file_name": "test.json",
            "swagger": openapi_content
        }
        self.client.import_api(
            gateway=TestExportApi.gateway,
            **attrs
        )
