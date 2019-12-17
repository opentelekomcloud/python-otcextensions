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


class TestDS(base.BaseFunctionalTest):

    @classmethod
    def setUpClass(cls):
        super(TestDS, cls).setUpClass()
        openstack.enable_logging(debug=True, http_debug=True)
        cls.client = cls.conn.mrs

        res = cls.client.create_datasource(
            name=uuid.uuid4().hex,
            url='/simple/mapreduce/input',
            type='hdfs',
            description='test ds'
        )
        id = res.id
        cls.datasource = cls.client.get_datasource(id)

        _logger.debug("SAHARA create test ds")
        _logger.debug(cls.datasource)

    @classmethod
    def tearDownClass(cls):
        try:
            pass
            if cls.datasource.id:
                pass
                cls.client.delete_datasource(cls.datasource)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_list(self):
        self.datasources = list(self.conn.mrs.datasources())
        self.assertGreaterEqual(len(self.datasources), 0)
        for ds in self.datasources:
            _logger.debug(ds)

    def test_update(self):
        res = self.client.update_datasource(
            self.datasource,
            url='/simple/mapreduce/input',
            type='hdfs',
            description='funct_test update ds'
        )

        _logger.debug(res)
        self.datasources = list(self.conn.mrs.datasources())
        self.assertGreaterEqual(len(self.datasources), 0)
        for ds in self.datasources:
            _logger.debug(ds)
