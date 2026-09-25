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
import time
from unittest.mock import MagicMock

from openstack import exceptions
from openstack.tests.unit import test_proxy_base
from otcextensions.sdk.aksk_auth import AkskRequestsAuth
from otcextensions.sdk.sfs3.v3 import _proxy
from otcextensions.sdk.sfs3.v3 import file_system as _file_system

ENDPOINT = "https://sfs3.eu-de.otc.t-systems.com"
FS_ENDPOINT = "https://fs-name.sfs3.eu-de.otc.t-systems.com"


class TestSfs3Proxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestSfs3Proxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        self.proxy._connection = self.session._sdk_connection = MagicMock()
        self.proxy.region_name = "eu-de"
        self.proxy.get_endpoint = MagicMock(return_value=ENDPOINT)
        self.proxy.get_filesystem_endpoint = MagicMock(return_value=FS_ENDPOINT)

    def _make_auth(self, **overrides):
        params = {
            "access_key": "ak",
            "secret_key": "sk",
            "bucket": "",
        }
        params.update(overrides)
        return AkskRequestsAuth(**params)

    def _mock_aksk(self, ak="ak", sk="sk", token=None):
        """Point conn.get_ak_sk at a static AK/SK pair."""
        result = (ak, sk) if token is None else (ak, sk, token)
        self.session._sdk_connection.get_ak_sk = MagicMock(
            side_effect=lambda conn: result
        )
        self.session._sdk_connection.config.config = {}

    # ======== _get_req_auth ========

    def test_get_req_auth_static_aksk(self):
        self._mock_aksk()
        auth = self.proxy._get_req_auth()
        self.assertIsInstance(auth, AkskRequestsAuth)
        self.assertEqual(auth.access_key, "ak")
        self.assertEqual(auth.secret_key, "sk")
        self.assertEqual(auth.bucket, "")
        self.assertIsNone(auth.security_token)
        # static (token-less) signers are cached
        self.assertIs(self.proxy._get_req_auth(), auth)

    def test_get_req_auth_static_aksk_with_token(self):
        self._mock_aksk(token="tok")
        auth = self.proxy._get_req_auth()
        self.assertEqual(auth.security_token, "tok")

    def test_get_req_auth_bucket_from_host(self):
        """The bucket is derived from the virtual-hosted host."""
        self._mock_aksk()
        auth = self.proxy._get_req_auth(FS_ENDPOINT)
        self.assertIsInstance(auth, AkskRequestsAuth)
        self.assertEqual(auth.bucket, "fs-name")
        # base endpoint carries no bucket
        self.assertEqual(self.proxy._get_req_auth(ENDPOINT).bucket, "")

    def test_get_req_auth_creates_temp_aksk(self):
        """Without AK/SK the proxy must create a temporary one."""
        self.session._sdk_connection.get_ak_sk = MagicMock(return_value=(None, None))
        config = {}
        self.session._sdk_connection.config.config = config
        tmp_token = MagicMock()
        tmp_token.access = "tmp-ak"
        tmp_token.secret = "tmp-sk"
        tmp_token.security_token = "tmp-token"
        self.session._sdk_connection.identity.create_security_token = MagicMock(
            return_value=tmp_token
        )

        auth = self.proxy._get_req_auth()

        self.session._sdk_connection.identity.create_security_token.assert_called_once_with(
            duration=_proxy.TMP_AKSK_DURATION
        )
        self.assertEqual(auth.access_key, "tmp-ak")
        self.assertEqual(auth.secret_key, "tmp-sk")
        self.assertEqual(auth.security_token, "tmp-token")
        # cached on the connection
        cached = config["_tmp_aksk"]
        self.assertEqual(cached["access_key"], "tmp-ak")
        self.assertEqual(cached["secret_key"], "tmp-sk")
        self.assertEqual(cached["security_token"], "tmp-token")
        self.assertGreaterEqual(cached["expires"], int(time.time()) + 800)

    def test_get_req_auth_temp_aksk_not_recreated_while_valid(self):
        """A cached, non-expiring temporary token is reused."""
        self.session._sdk_connection.get_ak_sk = MagicMock(return_value=(None, None))
        self.session._sdk_connection.config.config = {}
        tmp_token = MagicMock()
        tmp_token.access = "tmp-ak"
        tmp_token.secret = "tmp-sk"
        tmp_token.security_token = "tmp-token"
        self.session._sdk_connection.identity.create_security_token = MagicMock(
            return_value=tmp_token
        )

        self.proxy._get_req_auth()
        self.proxy._get_req_auth()
        self.proxy._get_req_auth()
        self.assertEqual(
            self.session._sdk_connection.identity.create_security_token.call_count,
            1,
        )

    def test_get_req_auth_temp_aksk_recreated_when_expiring(self):
        """An expiring cached token must trigger a new temporary token."""
        self.session._sdk_connection.get_ak_sk = MagicMock(return_value=(None, None))
        config = {}
        self.session._sdk_connection.config.config = config

        call_counter = {"n": 0}

        def make_token(duration):
            call_counter["n"] += 1
            return MagicMock(
                access="ak-%d" % call_counter["n"],
                secret="sk-%d" % call_counter["n"],
                security_token="tok-%d" % call_counter["n"],
            )

        self.session._sdk_connection.identity.create_security_token = MagicMock(
            side_effect=make_token
        )

        auth1 = self.proxy._get_req_auth()
        self.assertEqual(auth1.access_key, "ak-1")

        # mark the cached token as about to expire
        config["_tmp_aksk"]["expires"] = int(time.time()) + 1

        auth2 = self.proxy._get_req_auth()
        self.assertEqual(auth2.access_key, "ak-2")
        self.assertGreater(config["_tmp_aksk"]["expires"], int(time.time()) + 800)

    # ======== File Systems ========

    def test_file_systems(self):
        self._mock_aksk()
        auth = self.proxy._get_req_auth(ENDPOINT)
        self.verify_list(
            self.proxy.file_systems,
            _file_system.FileSystem,
            mock_method="otcextensions.sdk.sdk_proxy.Proxy._list",
            expected_kwargs={
                "endpoint_override": ENDPOINT,
                "headers": {"x-obs-bucket-type": "SFS"},
                "requests_auth": auth,
            },
        )

    def test_create_filesystem(self):
        self._mock_aksk()
        auth = self.proxy._get_req_auth(FS_ENDPOINT)
        self.verify_create(
            self.proxy.create_filesystem,
            _file_system.FileSystem,
            mock_method="otcextensions.sdk.sdk_proxy.Proxy._create",
            method_kwargs={"name": "fs-name"},
            expected_kwargs={
                "name": "fs-name",
                "location": "eu-de",
                "sfs_type": "SFS",
                "az_redundancy": "3az",
                "endpoint_override": FS_ENDPOINT,
                "requests_auth": auth,
            },
        )

    def test_get_filesystem(self):
        self._mock_aksk()
        auth = self.proxy._get_req_auth(FS_ENDPOINT)
        self._verify(
            "otcextensions.sdk.sdk_proxy.Proxy._head",
            self.proxy.get_filesystem,
            method_args=["fs-name"],
            expected_args=[_file_system.FileSystem, "fs-name"],
            expected_kwargs={
                "endpoint_override": FS_ENDPOINT,
                "requests_auth": auth,
            },
        )

    def test_delete_filesystem(self):
        self._mock_aksk()
        auth = self.proxy._get_req_auth(FS_ENDPOINT)
        self.verify_delete(
            self.proxy.delete_filesystem,
            _file_system.FileSystem,
            ignore_missing=True,
            mock_method="otcextensions.sdk.sdk_proxy.Proxy._delete",
            expected_kwargs={
                "endpoint_override": FS_ENDPOINT,
                "ignore_missing": True,
                "requests_auth": auth,
            },
        )

    def test_get_filesystem_bad_name(self):
        self._mock_aksk()
        self.assertRaises(ValueError, self.proxy.get_filesystem, 123)

    def test_get_filesystem_from_resource(self):
        """A FileSystem instance is accepted as name."""
        self._mock_aksk()
        fs = _file_system.FileSystem.existing(name="fs-name")
        self.assertEqual(self.proxy._get_filesystem_name(fs), "fs-name")

    # ======== File System ACL ========

    def _mock_get_project_id(self, pid="project-123"):
        self.session.get_project_id = MagicMock(return_value=pid)

    def test_create_acl(self):
        self._mock_aksk()
        auth = self.proxy._get_req_auth(FS_ENDPOINT)
        statements = [
            {
                "Sid": "s1",
                "Action": "FullControl",
                "Effect": "Allow",
                "Condition": {"SourceVpc": "vpc-1"},
            }
        ]
        self.proxy.create_acl("fs-name", statements)
        self.session.put.assert_called_once()
        args, kwargs = self.session.put.call_args
        self.assertEqual(args[0], FS_ENDPOINT + "/?sfsacl")
        self.assertEqual(kwargs["json"], {"Statement": statements})
        self.assertEqual(kwargs["endpoint_override"], FS_ENDPOINT)
        self.assertEqual(kwargs["requests_auth"], auth)

    def test_get_acl(self):
        self._mock_aksk()
        self.session.get.return_value = MagicMock(
            status_code=200,
            json=MagicMock(
                return_value={
                    "Statement": [
                        {
                            "Sid": "s1",
                            "Action": "Read",
                            "Effect": "Allow",
                            "Condition": {"SourceVpc": "vpc-1"},
                        }
                    ]
                }
            ),
        )
        result = self.proxy.get_acl("fs-name")
        self.session.get.assert_called_once()
        args, _ = self.session.get.call_args
        self.assertEqual(args[0], FS_ENDPOINT + "/?sfsacl")
        self.assertEqual(result[0]["Condition"], {"SourceVpc": "vpc-1"})

    def test_get_acl_empty(self):
        self._mock_aksk()
        self.session.get.return_value = MagicMock(
            status_code=204, json=MagicMock(return_value=None)
        )
        self.assertEqual(self.proxy.get_acl("fs-name"), [])

    def test_delete_acl(self):
        self._mock_aksk()
        self.proxy.delete_acl("fs-name")
        self.session.delete.assert_called_once()
        args, kwargs = self.session.delete.call_args
        self.assertEqual(args[0], FS_ENDPOINT + "/?sfsacl")
        self.assertEqual(kwargs["endpoint_override"], FS_ENDPOINT)

    # ======== Tags (TMS) ========

    def _tags_base(self, name=None):
        return (
            ENDPOINT
            + "/v3/sfs/tms/project-123/file-systems"
            + ("/%s" % name if name else "")
        )

    def test_get_project_id_raises_without_project(self):
        self.session.get_project_id = MagicMock(return_value=None)
        self.assertRaises(exceptions.ResourceFailure, self.proxy._get_project_id)

    def test_add_tags(self):
        self._mock_get_project_id()
        tags = [{"key": "k1", "value": "v1"}]
        self.proxy.add_tags("fs-name", tags)
        self.session.post.assert_called_once()
        args, kwargs = self.session.post.call_args
        self.assertEqual(args[0], self._tags_base("fs-name") + "/tags/create")
        self.assertEqual(kwargs["json"], {"tags": tags})
        self.assertEqual(kwargs["endpoint_override"], ENDPOINT)

    def test_delete_tags(self):
        self._mock_get_project_id()
        tags = [{"key": "k1", "value": "v1"}]
        self.proxy.delete_tags("fs-name", tags)
        self.session.post.assert_called_once()
        args, kwargs = self.session.post.call_args
        self.assertEqual(args[0], self._tags_base("fs-name") + "/tags/delete")
        self.assertEqual(kwargs["json"], {"tags": tags})

    def test_get_tags(self):
        self._mock_get_project_id()
        self.session.get.return_value = MagicMock(
            json=MagicMock(return_value={"tags": [{"key": "k1", "value": "v1"}]})
        )
        result = self.proxy.get_tags("fs-name")
        self.session.get.assert_called_once()
        args, _ = self.session.get.call_args
        self.assertEqual(args[0], self._tags_base("fs-name") + "/tags")
        self.assertEqual(result["tags"][0]["key"], "k1")

    def test_get_project_tags(self):
        self._mock_get_project_id()
        self.session.get.return_value = MagicMock(
            json=MagicMock(return_value={"tags": [{"key": "k1", "values": ["v1"]}]})
        )
        result = self.proxy.get_project_tags()
        self.session.get.assert_called_once()
        args, _ = self.session.get.call_args
        self.assertEqual(args[0], self._tags_base() + "/tags")
        self.assertEqual(result["tags"][0]["values"], ["v1"])

    def test_filter_resources_by_tags(self):
        self._mock_get_project_id()
        self.session.post.return_value = MagicMock(
            json=MagicMock(
                return_value={
                    "resources": [
                        {
                            "resource_id": "r1",
                            "resource_name": "fs-name",
                            "tags": [],
                        }
                    ],
                    "total_count": 1,
                }
            )
        )
        tags = [{"key": "k1", "values": ["v1"]}]
        matches = [{"key": "resource_name", "value": "prefix"}]
        result = self.proxy.filter_resources_by_tags(
            tags=tags, matches=matches, without_any_tag=False, limit=10, offset=5
        )
        self.session.post.assert_called_once()
        args, kwargs = self.session.post.call_args
        self.assertEqual(args[0], self._tags_base() + "/resource-instances/filter")
        self.assertEqual(
            kwargs["json"],
            {
                "tags": tags,
                "without_any_tag": False,
                "matches": matches,
            },
        )
        self.assertEqual(kwargs["params"], {"limit": 10, "offset": 5})
        self.assertEqual(result["total_count"], 1)

    def test_count_resources_by_tags(self):
        self._mock_get_project_id()
        self.session.post.return_value = MagicMock(
            json=MagicMock(return_value={"total_count": 2})
        )
        tags = [{"key": "k1", "values": ["v1", "v2"]}]
        result = self.proxy.count_resources_by_tags(tags=tags)
        self.session.post.assert_called_once()
        args, kwargs = self.session.post.call_args
        self.assertEqual(args[0], self._tags_base() + "/resource-instances/count")
        self.assertEqual(kwargs["json"], {"tags": tags})
        self.assertEqual(result["total_count"], 2)
