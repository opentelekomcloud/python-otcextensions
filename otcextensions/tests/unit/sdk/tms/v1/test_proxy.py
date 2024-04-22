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

from otcextensions.sdk.tms.v1 import _proxy
from otcextensions.sdk.tms.v1 import predefined_tag


class TestTmsProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestTmsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestTmsPredefinedTag(TestTmsProxy):
    def test_predefined_tags(self):
        self.verify_list(self.proxy.predefined_tags, predefined_tag.PredefinedTag)

    def test_predefined_tag_create(self):
        self._verify(
            mock_method='otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag.add_tag',
            test_method=self.proxy.create_predefined_tag,
            method_kwargs={
                'key': 'key',
                'value': 'value'
            },
            expected_args=[
                self.proxy,

            ]
        )

    def test_predefined_tag_delete(self):
        self._verify(
            mock_method='otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag.delete_tag',
            test_method=self.proxy.delete_predefined_tag,
            method_kwargs={
                'key': 'key',
                'value': 'value'
            },
            expected_args=[
                self.proxy,

            ]
        )

    def test_predefined_tag_update(self):
        self.verify_update(self.proxy.update_predefined_tag,
                           predefined_tag.PredefinedTag,
                           method_kwargs={
                               "new_tag": {
                                    "key": "key",
                                    "value": "value"},
                               "old_tag": {
                                    'key': 'key',
                                    'value': 'new_value'
                               }
                           },
                           expected_kwargs={
                               "new_tag": {
                                   "key": "key",
                                   "value": "value"},
                               "old_tag": {
                                   'key': 'key',
                                   'value': 'new_value'
                               }
                           },)
