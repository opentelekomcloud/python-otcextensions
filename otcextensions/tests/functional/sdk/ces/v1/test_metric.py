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
from otcextensions.tests.functional import base

_logger = _log.setup_logging("openstack")


class TestMetric(base.BaseFunctionalTest):

    def test_list(self):
        metrics = list(self.conn.ces.metrics())
        assert len(metrics) > 0

    def test_list_with_non_existing_params(self):
        metrics = list(
            self.conn.ces.metrics(namespace='SYS.ECS',
                                  metric_name='totally_fake_metric_xyz'))
        assert len(metrics) == 0

    def test_list_with_existing_metric(self):
        metrics = list(
            self.conn.ces.metrics(namespace='SYS.ECS',)
        )
        assert len(metrics) > 0
