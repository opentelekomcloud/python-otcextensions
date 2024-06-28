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

from openstack.tests.unit import base
from otcextensions.sdk.dws.v1 import snapshot

EXAMPLE = {
    'id': uuid.uuid4().hex,
    'name': 'snapshot-1',
    'description': 'snapshot description',
    'started': '2016-08-23T03:59:23Z',
    'finished': '2016-08-23T04:01:40Z',
    'size': 500,
    'status': 'AVAILABLE',
    'type': 'MANUAL',
    'cluster_id': uuid.uuid4().hex,
}

RESTORED_CLUSTER = {'id': uuid.uuid4().hex}


class TestSnapshot(base.TestCase):

    def setUp(self):
        super(TestSnapshot, self).setUp()

    def test_basic(self):
        sot = snapshot.Snapshot()

        self.assertEqual('/snapshots', sot.base_path)
        self.assertEqual('snapshots', sot.resources_key)
        self.assertEqual('snapshot', sot.resource_key)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_patch)

    def test_make_it(self):
        sot = snapshot.Snapshot(**EXAMPLE)

        updated_sot_attrs = (
            'started',
            'finished',
        )
        self.assertEqual(EXAMPLE['started'], sot.created_at)
        self.assertEqual(EXAMPLE['finished'], sot.updated_at)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)


class TestRestore(base.TestCase):

    def setUp(self):
        super(TestRestore, self).setUp()

    def test_basic(self):
        sot = snapshot.Restore()

        self.assertEqual('/snapshots/%(snapshot_id)s/actions', sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_patch)

    def test_make_it(self):
        sot = snapshot.Restore(**RESTORED_CLUSTER)

        self.assertEqual(RESTORED_CLUSTER['id'], sot.id)
