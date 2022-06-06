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


import uuid

import openstack
from openstack import _log

from otcextensions.tests.functional.sdk.mrs import TestMrs

_logger = _log.setup_logging('openstack')


class TestJobbinary(TestMrs):
    jobbinary = None

    def setUp(self):
        super(TestJobbinary, self).setUp()
        res = self.client.create_jobbinary(
            name=uuid.uuid4().hex,
            url="/simple/mapreduce/program",
            description='this is the job binary template',
        )
        id = res.id
        self.jobbinary = self.client.get_jobbinary(id)

        _logger.debug("SAHARA create test jobbinary")
        _logger.debug(self.jobbinary)

    def tearDown(self):
        try:
            pass
            if self.jobbinary.id:
                pass
                self.client.delete_jobbinary(self.jobbinary)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)
        super(TestJobbinary, self).tearDown()

    def test_list(self):
        self.jb = list(self.client.jobbinaries())
        self.assertGreaterEqual(len(self.jb), 0)
        for bin in self.jb:
            _logger.debug(bin)

    def test_update(self):
        res = self.client.update_jobbinary(
            self.jobbinary,
            is_protected=False,
            is_public=False,
            description='updated'
        )

        _logger.debug(res)
        self.jbs = list(self.client.jobbinaries())
        self.assertGreaterEqual(len(self.jbs), 0)
        for jb in self.jbs:
            _logger.debug(jb)
