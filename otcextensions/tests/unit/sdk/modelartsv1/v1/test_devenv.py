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
from openstack.tests.unit import base
from otcextensions.sdk.modelartsv1.v1 import devenv
from otcextensions.tests.unit.sdk.modelartsv1.v1.examples import \
    EXAMPLE_DEVENV as EXAMPLE


EXAMPLE_CREATE = {
    "name": "notebook-d115",
    "description": "",
    "profile_id": "Ascend-Power-Engine 1.0(python3)",
    "flavor": "modelarts.kat1.xlarge",
    "spec": {
        "storage": {"location": {"path": "/aaaaaaaaa/output/"}, "type": "obs"},
        "auto_stop": {"enable": True, "duration": 3600},
    },
    "workspace": {"id": "0"},
}


class TestDevenv(base.TestCase):
    def setUp(self):
        super(TestDevenv, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = devenv.Devenv()

        self.assertEqual("/demanager/instances", sot.base_path)
        # self.assertEqual('', sot.resource_key)
        self.assertEqual("instances", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_create_sot(self):
        updated_sot_attrs = []
        sot = devenv.Devenv(**EXAMPLE_CREATE)

        for key, value in EXAMPLE_CREATE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

    def test_response_sot(self):
        sot = devenv.Devenv(**EXAMPLE)
        updated_sot_attrs = (
            "creation_timestamp",
            "latest_update_timestamp",
        )

        self.assertEqual(EXAMPLE["creation_timestamp"], sot.created_at)
        self.assertEqual(EXAMPLE["latest_update_timestamp"], sot.updated_at)
        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

    def test_action(self):
        data = {"id": "mock-id"}
        sot = devenv.Devenv(**data)
        action = "start"
        json_body = {"action": action}
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = data
        response.headers = {}
        self.sess.post.return_value = response
        rt = sot._action(self.sess, action)
        self.sess.post.assert_called_with(
            "demanager/instances/%s/action" % sot.id,
            json=json_body,
            headers={
                "Accept": "application/json",
                "Content-type": "application/json",
            },
        )
        self.assertEqual(rt, sot)

    def test_start(self):
        sot = devenv.Devenv.existing(id=EXAMPLE["id"])
        sot._action = mock.Mock()
        sot.start(self.sess)
        sot._action.assert_called_with(self.sess, "start")

    def test_stop(self):
        sot = devenv.Devenv.existing(id=EXAMPLE["id"])
        sot._action = mock.Mock()
        sot.stop(self.sess)
        sot._action.assert_called_with(self.sess, "stop")
