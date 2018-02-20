#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
import unittest

from otcextensions.osclient.obs.v1.utils import parse_s3_uri


class TestShell(unittest.TestCase):

    def test_parse_s3_uri_bucket_path(self):
        bucket, prefix = parse_s3_uri('s3://bucket/prefix/file')
        self.assertEqual('bucket', bucket)
        self.assertEqual('prefix/file', prefix)

    def test_parse_s3_uri_bucket_trailing_slash(self):
        bucket, prefix = parse_s3_uri('s3://bucket/')
        self.assertEqual('bucket', bucket)
        self.assertEqual('', prefix)

    def test_parse_s3_uri_object_trailing_slash(self):
        bucket, prefix = parse_s3_uri('s3://bucket/prefix/file/')
        self.assertEqual('bucket', bucket)
        self.assertEqual('prefix/file', prefix)

    def test_parse_s3_uri_empty(self):
        bucket, prefix = parse_s3_uri('')
        self.assertEqual('', bucket)
        self.assertEqual('', prefix)

    def test_parse_s3_uri_s4(self):
        bucket, prefix = parse_s3_uri('s4://bucket/file')
        self.assertEqual('', bucket)
        self.assertEqual('', prefix)
