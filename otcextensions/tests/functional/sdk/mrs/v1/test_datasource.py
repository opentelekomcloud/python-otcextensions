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


class TestDS(TestMrs):
    data_source = None

    def setUp(self):
        super(TestDS, self).setUp()
        result = self.client.create_datasource(
            name=uuid.uuid4().hex,
            url='/simple/mapreduce/input',
            type='hdfs',
            description='test ds'
        )
        id = result.id
        self.data_source = self.client.get_datasource(id)

        _logger.debug("SAHARA create test ds")
        _logger.debug(self.data_source)

    def tearDown(self):
        try:
            if self.data_source.id:
                self.client.delete_datasource(self.data_source)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)
        super(TestDS, self).tearDown()

    def test_01_list(self):
        self.data_sources = list(self.client.datasources())
        self.assertGreaterEqual(len(self.data_sources), 0)
        for ds in self.data_sources:
            _logger.debug(ds)

    # unstable test
    # def test_02_update(self):
    #     res = self.client.update_datasource(
    #         self.data_source,
    #         description='funct_test update ds'
    #     )
    #     _logger.debug(res)
    #     self.data_source = self.client.get_datasource(res)
    #     self.assertIsNotNone(self.data_source)
    #     self.assertEqual('funct_test update ds', res.description)
    #     _logger.debug(self.data_source)
