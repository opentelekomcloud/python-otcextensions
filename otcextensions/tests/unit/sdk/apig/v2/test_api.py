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
from otcextensions.sdk.apig.v2 import api
from otcextensions.sdk.apig.v2 import api_supplements as _as

EXAMPLE = {
    "group_id": "id",
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


class TestApi(base.TestCase):

    def test_basic(self):
        sot = api.Api()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/apis',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)
        self.assertEqual('apis', sot.resources_key)

    def test_make_it(self):
        sot = api.Api(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['group_id'], sot.group_id)
        self.assertEqual(EXAMPLE['auth_type'], sot.auth_type)
        self.assertEqual(EXAMPLE['backend_type'], sot.backend_type)
        self.assertEqual(EXAMPLE['req_protocol'], sot.req_protocol)


EXAMPLE_PUB = {
    "api_id": "5f918d104dc84480a75166ba99efff21",
    "env_id": "DEFAULT_ENVIRONMENT_RELEASE_ID",
    "publish_id": "9191cdb430724d4b8586ed7f1b962ca2",
    "publish_time": "2020-08-03T01:36:00.592970615Z",
    "version_id": "ee1a5a38d3d3493abf1dc4ed6cacfa0b"
}


class TestPublishApi(base.TestCase):

    def test_basic(self):
        sot = _as.PublishApi()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/apis/action',
            sot.base_path)
        self.assertTrue(sot.allow_create)

    def test_make_it(self):
        sot = _as.PublishApi(**EXAMPLE_PUB)
        self.assertEqual(EXAMPLE_PUB['api_id'], sot.api_id)
        self.assertEqual(EXAMPLE_PUB['env_id'], sot.env_id)
        self.assertEqual(EXAMPLE_PUB['publish_id'], sot.publish_id)
        self.assertEqual(EXAMPLE_PUB['publish_time'], sot.publish_time)
        self.assertEqual(EXAMPLE_PUB['version_id'], sot.version_id)


EXAMPLE_CHECK = {
    "type": "name",
    "name": "api_demo"
}


class TestCheckApi(base.TestCase):

    def test_basic(self):
        sot = _as.CheckApi()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/apis/check',
            sot.base_path)
        self.assertTrue(sot.allow_create)

    def test_make_it(self):
        sot = _as.CheckApi(**EXAMPLE_CHECK)
        self.assertEqual(EXAMPLE_CHECK['type'], sot.type)
        self.assertEqual(EXAMPLE_CHECK['name'], sot.name)


EXAMPLE_DEBUG = {
    "request": "GET /test/mock HTTP/1.1\n"
               "Host: c77f5e81d9cb4424bf704ef2b0ac7600.apic.****.com\n"
               "User-Agent: APIGatewayDebugClient/1.0\n"
               "X-Apig-Mode: debug\n"
               "\n",
    "response": "HTTP/1.1 200 OK\n"
                "Transfer-Encoding: chunked\n"
                "Connection: keep-alive\n"
                "Content-Type: application/json\n"
                "Date: Mon, 03 Aug 2020 02:51:22 GMT\n"
                "Server: api-gateway\n"
                "X-Apig-Latency: 0\n"
                "X-Apig-Ratelimit-Api: remain:99,limit:100,time:1 minute\n"
                "X-Apig-Ratelimit-Api-Allenv: remain:14999,"
                "limit:15000,time:1 second\n"
                "X-Request-Id: d4ec6e33148bdeffe8f55b43472d1251\n"
                "\nmock success",
    "latency": 5,
    "log": ""
}


class TestDebugApi(base.TestCase):

    def test_basic(self):
        sot = _as.DebugApi()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/apis/debug/%(api_id)s',
            sot.base_path)
        self.assertTrue(sot.allow_create)

    def test_make_it(self):
        sot = _as.DebugApi(**EXAMPLE_DEBUG)
        self.assertEqual(EXAMPLE_DEBUG['request'], sot.request)
        self.assertEqual(EXAMPLE_DEBUG['response'], sot.response)
        self.assertEqual(EXAMPLE_DEBUG['latency'], sot.latency)
        self.assertEqual(EXAMPLE_DEBUG['log'], sot.log)


EXAMPLE_PUB_APIS = {
    "apis": [
        "3a955b791bd24b1c9cd94c745f8d1aad",
        "abd9c4b2ff974888b0ba79be7e6b2762"
    ],
    "env_id": "DEFAULT_ENVIRONMENT_RELEASE_ID",
    "group_id": "c77f5e81d9cb4424bf704ef2b0ac7600",
    "remark": "Published to the production environment"
}


class TestPublishApis(base.TestCase):

    def test_basic(self):
        sot = _as.PublishApis()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/apis/publish',
            sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = _as.PublishApis(**EXAMPLE_PUB_APIS)
        self.assertEqual(EXAMPLE_PUB_APIS['apis'], sot.apis)
        self.assertEqual(EXAMPLE_PUB_APIS['env_id'], sot.env_id)
        self.assertEqual(EXAMPLE_PUB_APIS['group_id'], sot.group_id)
        self.assertEqual(EXAMPLE_PUB_APIS['remark'], sot.remark)


EXAMPLE_DEF = {
    "name": "Api_http",
    "type": 1,
    "version": "V0.0.1",
    "req_protocol": "HTTPS",
    "req_method": "GET",
    "req_uri": "/test/http",
    "auth_type": "AUTHORIZER",
    "authorizer_id": "8d0443832a194eaa84244e0c1c1912ac",
    "auth_opt": {
        "app_code_auth_type": "DISABLE"
    },
    "cors": False,
    "match_mode": "NORMAL",
    "backend_type": "HTTP",
    "remark": "Web backend API",
    "group_id": "c77f5e81d9cb4424bf704ef2b0ac7600",
    "result_normal_sample": "Example success response",
    "result_failure_sample": "Example failure response",
    "id": "5f918d104dc84480a75166ba99efff21",
    "group_name": "api_group_001",
    "run_env_id": "DEFAULT_ENVIRONMENT_RELEASE_ID",
    "run_env_name": "RELEASE",
    "publish_id": "9191cdb430724d4b8586ed7f1b962ca2",
    "sl_domain": "c77f5e81d9cb4424bf704ef2b0ac7600.apic.****.com",
    "sl_domains": [
        "c77f5e81d9cb4424bf704ef2b0ac7600.apic.****.com",
        "c77f5e81d9cb4424bf704ef2b0ac7600.apic.****.cn"
    ]
}


class TestRuntimeDefinition(base.TestCase):

    def test_basic(self):
        sot = _as.RuntimeDefinitionApi()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/apis/runtime/%(api_id)s',
            sot.base_path)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = _as.RuntimeDefinitionApi(**EXAMPLE_DEF)
        self.assertEqual(EXAMPLE_DEF['name'], sot.name)
        self.assertEqual(EXAMPLE_DEF['type'], sot.type)
        self.assertEqual(EXAMPLE_DEF['version'], sot.version)
        self.assertEqual(EXAMPLE_DEF['req_protocol'], sot.req_protocol)
        self.assertEqual(EXAMPLE_DEF['req_method'], sot.req_method)
        self.assertEqual(EXAMPLE_DEF['req_uri'], sot.req_uri)
        self.assertEqual(EXAMPLE_DEF['auth_type'], sot.auth_type)
        self.assertEqual(EXAMPLE_DEF['authorizer_id'], sot.authorizer_id)
        self.assertEqual(EXAMPLE_DEF['auth_opt'], sot.auth_opt)
        self.assertEqual(EXAMPLE_DEF['cors'], sot.cors)


EXAMPLE_VERSIONS = {
    "name": "Api_http",
    "type": 1,
    "version": "V0.0.1",
    "req_protocol": "HTTPS",
    "req_method": "GET",
    "req_uri": "/test/http",
    "auth_type": "AUTHORIZER",
}


class TestVersionsApi(base.TestCase):

    def test_basic(self):
        sot = _as.VersionsApi()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/apis/versions/%(version_id)s',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = _as.VersionsApi(**EXAMPLE_VERSIONS)
        self.assertEqual(EXAMPLE_VERSIONS['name'], sot.name)
        self.assertEqual(EXAMPLE_VERSIONS['type'], sot.type)
        self.assertEqual(EXAMPLE_VERSIONS['version'], sot.version)
        self.assertEqual(EXAMPLE_VERSIONS['req_protocol'], sot.req_protocol)
        self.assertEqual(EXAMPLE_VERSIONS['req_method'], sot.req_method)
        self.assertEqual(EXAMPLE_VERSIONS['req_uri'], sot.req_uri)
        self.assertEqual(EXAMPLE_VERSIONS['auth_type'], sot.auth_type)
