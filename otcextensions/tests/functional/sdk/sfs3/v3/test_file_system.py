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
import uuid

import keystoneauth1.exceptions.http

import openstack
from otcextensions.tests.functional import base

_logger = openstack._log.setup_logging("openstack")

#: How long to wait for the created file system to show up in the list.
# ``ListAllMyBuckets`` lags on creates (OBS eventual consistency), so the
# list assertion is best-effort.
LIST_SETTLE_TIMEOUT = 120

#: How long to wait for a newly created VPC to become ready.
VPC_READY_TIMEOUT = 120

#: Reuse this VPC for the ACL if it already exists; otherwise create and
#: tear down a dedicated one.
REUSE_VPC_NAME = "vpc-do-not-delete-pls"

#: File system name prefix used to identify resources created by this test.
FS_NAME_PREFIX = "sfs3-test-"


class TestFileSystem(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    fs_name = FS_NAME_PREFIX + uuid_v4
    fs = None

    def setUp(self):
        super(TestFileSystem, self).setUp()
        self.client = self.conn.sfs3
        self.require_service("sfs3")
        self._setup_vpc()

    def _setup_vpc(self):
        """Provide a VPC to authorize on the file system ACL.

        Reuses ``REUSE_VPC_NAME`` when it already exists; otherwise creates a
        dedicated VPC and registers a cleanup to tear it down. A file system
        is only usable (and only visible in the list/UI) once its ACL
        authorizes a VPC, so the tests need a VPC id.
        """
        for vpc in self.conn.vpc.vpcs():
            if vpc.name == REUSE_VPC_NAME:
                self.vpc_id = vpc.id
                return
        name = "sfs3-test-vpc-" + self.uuid_v4
        vpc = self.conn.vpc.create_vpc(name=name, cidr="172.16.100.0/24")
        self.vpc_id = vpc.id
        self.addCleanup(self.conn.vpc.delete_vpc, vpc.id, ignore_missing=True)
        # wait for the VPC to become ready before the ACL can reference it
        # (OTC reports "OK" for an ACTIVE VPC)
        deadline = time.time() + VPC_READY_TIMEOUT
        while time.time() < deadline:
            status = self.conn.vpc.get_vpc(vpc.id).status
            if status in ("OK", "ACTIVE"):
                return
            time.sleep(2)
        self.fail("VPC %s did not become ready within %ss" % (name, VPC_READY_TIMEOUT))

    def _create_filesystem(self):
        self.fs = self.client.create_filesystem(name=self.fs_name)
        self.assertIsNotNone(self.fs)
        self.addCleanup(self.client.delete_filesystem, self.fs_name)
        self.client.create_acl(
            self.fs_name,
            [
                {
                    "Sid": "sdk-test",
                    "Action": "FullControl",
                    "Effect": "Allow",
                    "Condition": {"SourceVpc": self.vpc_id},
                }
            ],
        )
        self.addCleanup(self.client.delete_acl, self.fs_name)
        return self.fs

    def test_01_create_filesystem(self):
        fs = self._create_filesystem()
        self.assertIsNotNone(fs)

    def test_02_file_systems(self):
        self._create_filesystem()
        deadline = time.time() + LIST_SETTLE_TIMEOUT
        names = []
        while True:
            names = [fs.name for fs in self.client.file_systems()]
            if self.fs_name in names:
                break
            self.assertLess(
                time.time(),
                deadline,
                "file system %s did not appear in the list within %ss"
                % (self.fs_name, LIST_SETTLE_TIMEOUT),
            )
            time.sleep(5)
        self.assertIn(self.fs_name, names)

    def test_03_get_filesystem(self):
        self._create_filesystem()
        fs = self.client.get_filesystem(self.fs_name)
        self.assertIsNotNone(fs)

    def test_04_acl(self):
        self._create_filesystem()
        statements = self.client.get_acl(self.fs_name)
        self.assertIsInstance(statements, list)
        self.assertTrue(statements)
        # the statement we configured should be present (the service appends
        # a suffix to the Sid, so match on SourceVpc instead)
        self.assertTrue(
            any(
                stmt.get("Condition", {}).get("SourceVpc") == self.vpc_id
                for stmt in statements
            ),
            "file system ACL does not authorize the test VPC: %s" % statements,
        )

    def test_05_tags(self):
        self._create_filesystem()
        try:
            self.client.add_tags(
                self.fs_name, [{"key": "sfs3-sdk-test", "value": "yes"}]
            )
        except keystoneauth1.exceptions.http.BadRequest:
            self.skipTest(
                "SFS file systems are not registered in TMS for this "
                "account/region (per-resource tag API returns 400)"
            )
        self.addCleanup(
            self.client.delete_tags,
            self.fs_name,
            [{"key": "sfs3-sdk-test", "value": "yes"}],
        )
        tags = self.client.get_tags(self.fs_name)
        keys = [t["key"] for t in tags.get("tags", [])]
        self.assertIn("sfs3-sdk-test", keys)

    def test_06_project_tags(self):
        # Project-level tag queries do not require a file system to exist.
        tags = self.client.get_project_tags()
        self.assertIn("tags", tags)
        self.assertIsInstance(tags["tags"], list)

    def test_07_count_resources_by_tags(self):
        result = self.client.count_resources_by_tags()
        self.assertIn("total_count", result)
        self.assertIsInstance(result["total_count"], int)

    def test_08_filter_resources_by_tags(self):
        result = self.client.filter_resources_by_tags(limit=10)
        self.assertIn("resources", result)
        self.assertIn("total_count", result)
        self.assertIsInstance(result["resources"], list)
