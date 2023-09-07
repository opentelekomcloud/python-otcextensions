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
from otcextensions.sdk.dis.v2 import app


EXAMPLE = {
    "app_id": "bd6IPpvgiIflQPMpi9M",
    "app_name": "newapp",
    "create_time": 1593569685875,
    "commit_checkpoint_stream_names": ["newstream"]
}


class TestApp(base.TestCase):

    def test_basic(self):
        sot = app.App()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('apps', sot.resources_key)
        path = '/apps'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_patch)

    def test_make_it(self):
        sot = app.App(**EXAMPLE)
        updated_sot_attrs = (
            'app_name',
            'create_time',
        )
        self.assertEqual(EXAMPLE['create_time'], sot.created_at)
        self.assertEqual(EXAMPLE['app_id'], sot.id)
        self.assertEqual(EXAMPLE['app_name'], sot.name)
        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
