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
from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestJob(base.BaseFunctionalTest):

    @classmethod
    def setUpClass(cls):
        super(TestJob, cls).setUpClass()
        openstack.enable_logging(debug=True, http_debug=True)
        cls.client = cls.conn.mrs

        res = cls.client.create_job(
            name=uuid.uuid4().hex,
            type='MapReduce',
            description='test job'
        )
        # assert len(res.id) == 1
        id = res.id
        cls.job = cls.client.get_job(id)

        _logger.debug("SAHARA create test job")
        _logger.debug(cls.job)

    @classmethod
    def tearDownClass(cls):
        try:
            pass
            if cls.job.id:
                pass
                cls.client.delete_job(cls.job)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_list(self):
        self.jobs = list(self.conn.mrs.jobs())
        self.assertGreaterEqual(len(self.jobs), 0)
        for j in self.jobs:
            _logger.debug(j)

    def test_update(self):
        res = self.client.update_job(
            self.job,
            type='MapReduce',
            description='funct_test update mapreduce'
        )

        _logger.debug(res)
        self.jobs = list(self.conn.mrs.jobs())
        self.assertGreaterEqual(len(self.jobs), 0)
        for j in self.jobs:
            _logger.debug(j)
