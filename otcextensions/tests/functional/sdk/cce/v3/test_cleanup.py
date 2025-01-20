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
import unittest

from openstack import resource
from openstack import _log
from openstack import exceptions

from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')

class TestCleanup(base.BaseFunctionalTest):
    def setUp(self):
        super(TestCleanup, self).setUp()

    def test_01(self):
        clusters = list(self.conn.cce.clusters())
        self.conn.cce._service_cleanup(dry_run=False)
        clusters = list(self.conn.dws.clusters())
        self.assertEqual(len(clusters), 0)