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
#
import mock
from keystoneauth1 import adapter
from openstack import utils
from openstack.tests.unit import base
from otcextensions.sdk.modelartsv2.v2 import dataset_synchronization_task

class TestDatasetSynchronization(base.TestCase):
    def setUp(self):
        super(TestDatasetSynchronization, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = dataset_synchronization_task.DatasetSample()

        self.assertEqual(
            "/datasets/%(dataset_id)s/sync-data",
            sot.base_path,
        )

        self.assertTrue(sot.allow_create)

    def test_show_snychronization_task(self):
        dataset_id = "dataset-uuid"
        self.assertEqual(
            "/datasets/%(dataset_id)s/sync-data",
            sot.base_path,
        )
        self.assertTrue(sot.allow_fetch)

