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
from otcextensions.sdk.ocr.v2 import _proxy


class TestOcrProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestOcrProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestExtractName(TestOcrProxy):

    def test_extract_name(self):
        self.assertEqual(
            ["general-text"],
            self.proxy._extract_name(
                "/v2/123/ocr/general-text",
                project_id="123",
            ),
        )
        self.assertEqual(
            ["general-table"],
            self.proxy._extract_name(
                "/v2/123/ocr/general-table",
                project_id="123",
            ),
        )
        self.assertEqual(
            ["smart-document-recognizer"],
            self.proxy._extract_name(
                "/v2/123/ocr/smart-document-recognizer",
                project_id="123",
            ),
        )
        self.assertEqual([], self.proxy._extract_name("/", project_id="123"))
        self.assertEqual([], self.proxy._extract_name("/v2", project_id="123"))
        self.assertEqual([], self.proxy._extract_name("/v2/123/ocr", project_id="123"))

    def test_extract_name_for_documented_endpoints(self):
        recognition_types = [
            "general-text",
            "general-table",
            "smart-document-recognizer",
        ]

        for recognition_type in recognition_types:
            url = f"/v2/123/ocr/{recognition_type}"
            with self.subTest(url=url):
                self.assertEqual(
                    [recognition_type],
                    self.proxy._extract_name(url, project_id="123"),
                )
