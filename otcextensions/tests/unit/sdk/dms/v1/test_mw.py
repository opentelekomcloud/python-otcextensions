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
from openstack.tests.unit import base

from otcextensions.sdk.dms.v1 import maintenance_window as mw


JSON_DATA = {
    "default": False,
    "seq": 1,
    "begin": "22",
    "end": "02"
}


class TestMW(base.TestCase):

    def test_basic(self):
        sot = mw.MaintenanceWindow()

        self.assertEqual('/instances/maintain-windows', sot.base_path)
        self.assertEqual('maintain_windows', sot.resources_key)

        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = mw.MaintenanceWindow(**JSON_DATA)
        self.assertEqual(JSON_DATA['default'], sot.is_default)
        self.assertEqual(int(JSON_DATA['seq']), sot.seq)
        self.assertEqual(JSON_DATA['begin'], sot.begin)
        self.assertEqual(JSON_DATA['end'], sot.end)
