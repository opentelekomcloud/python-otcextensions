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
from openstack import _log
# from openstack import exceptions
from otcextensions.tests.functional import base

# from otcextensions.i18n import _

_logger = _log.setup_logging('openstack')


class TestMisc(base.BaseFunctionalTest):

    def test_instance_num(self):
        _logger.info('test_instance_num')
        num = self.conn.kms.get_instance_number()

        self.assertIsNotNone(num.instance_num)

    def test_random(self):
        _logger.info('test_random')
        obj = self.conn.kms.generate_random(512)

        self.assertIsNotNone(obj.random_data)

    def test_quotas(self):
        _logger.info('test_quotas')
        obj = list(self.conn.kms.quotas())

        self.assertIsNotNone(obj)
