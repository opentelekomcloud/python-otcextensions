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
from openstack.tests.unit import base
from otcextensions.sdk.apig.v2 import signature_binding

EXAMPLE_BIND = {
    "sign_id": "0b0e8f456b8742218af75f945307173c",
    "publish_ids": ["40e7162dc6b94bbbbb1a60d2a24b1b0c"]
}


class TestSignatureBind(base.TestCase):

    def test_basic(self):
        sot = signature_binding.SignatureBind()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/sign-bindings',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertEqual('bindings', sot.resources_key)

    def test_make_it(self):
        sot = signature_binding.SignatureBind(**EXAMPLE_BIND)
        self.assertEqual(EXAMPLE_BIND['sign_id'], sot.sign_id)
        self.assertEqual(EXAMPLE_BIND['publish_ids'], sot.publish_ids)


EXAMPLE_NOTBOUND = {
    "run_env_name": "RELEASE",
    "group_name": "api_group_001",
    "remark": "Mock backend API",
    "publish_id": "9f27d1dc4f4242a9abf88e563dbfc33d",
    "group_id": "c77f5e81d9cb4424bf704ef2b0ac7600",
    "name": "Api_mock",
    "run_env_id": "DEFAULT_ENVIRONMENT_RELEASE_ID",
    "id": "3a955b791bd24b1c9cd94c745f8d1aad",
    "type": 1,
    "auth_type": "IAM",
    "req_uri": "/test/mock"
}


class TestNotBoundApi(base.TestCase):

    def test_basic(self):
        sot = signature_binding.NotBoundApi()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/sign-bindings/unbinded-apis',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertEqual('apis', sot.resources_key)

    def test_make_it(self):
        sot = signature_binding.NotBoundApi(**EXAMPLE_NOTBOUND)
        self.assertEqual(EXAMPLE_NOTBOUND['run_env_name'], sot.run_env_name)
        self.assertEqual(EXAMPLE_NOTBOUND['group_name'], sot.group_name)
        self.assertEqual(EXAMPLE_NOTBOUND['remark'], sot.remark)
        self.assertEqual(EXAMPLE_NOTBOUND['publish_id'], sot.publish_id)
        self.assertEqual(EXAMPLE_NOTBOUND['group_id'], sot.group_id)


EXAMPLE_BOUND = {
    "api_id": "5f918d104dc84480a75166ba99efff21",
    "group_name": "api_group_001",
    "binding_time": "2020-08-03T04:00:11Z",
    "env_id": "DEFAULT_ENVIRONMENT_RELEASE_ID",
    "env_name": "RELEASE",
    "sign_name": "signature_demo",
    "api_type": 1,
    "api_name": "Api_http",
    "id": "25082bd52f74442bb1d273993d567938",
    "api_remark": "Web backend API",
    "publish_id": "40e7162dc6b94bbbbb1a60d2a24b1b0c"
}


class TestBoundApi(base.TestCase):

    def test_basic(self):
        sot = signature_binding.BoundApi()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/sign-bindings/binded-apis',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertEqual('bindings', sot.resources_key)

    def test_make_it(self):
        sot = signature_binding.BoundApi(**EXAMPLE_BOUND)
        self.assertEqual(EXAMPLE_BOUND['api_id'], sot.api_id)
        self.assertEqual(EXAMPLE_BOUND['group_name'], sot.group_name)
        self.assertEqual(EXAMPLE_BOUND['binding_time'], sot.bind_at)
        self.assertEqual(EXAMPLE_BOUND['env_id'], sot.env_id)
        self.assertEqual(EXAMPLE_BOUND['env_name'], sot.env_name)
