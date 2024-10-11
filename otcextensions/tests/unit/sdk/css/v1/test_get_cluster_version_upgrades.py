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
from otcextensions.sdk.css.v1 import cluster_upgrade_status
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = {
    'id': '0249620d-1c4a-4211-943a-ced7b9a3cda5',
    'startTime': '2024-07-19T08:58:52',
    'endTime': '2024-07-19T09:16:20',
    'status': 'FAILED',
    'agencyName': 'css_upgrade_agency',
    'imageInfo': {
        'id': '5670dd9f-6399-4a2b-9faf-2a24c2a07cd3',
        'displayName': '7.10.2_23.5.1_0123',
        'imageDesc': 'The latest image of...',
        'datastoreType': 'elasticsearch',
        'datastoreVersion': '7.10.2',
        'priority': 11,
    },
    'totalNodes': 'csstest0716-ess-esn-2-1...',
    'completedNodes': '',
    'currentNodeName': 'csstest0716-ess-esn-2-1',
    'executeTimes': '1',
    'currentNodeDetail': [
        {
            'order': 0,
            'name': 'Data migration',
            'status': 'SUCCESS',
            'desc': 'Data is migrated.',
            'beginTime': '2024-07-19T08:58:54',
            'endTime': '2024-07-19T08:58:59',
        },
        {
            'order': 1,
            'name': 'Node brought offline',
            'status': 'SUCCESS',
            'desc': 'The node is brought offline.',
            'beginTime': '2024-07-19T08:59:04',
            'endTime': '2024-07-19T09:12:55',
        },
        {
            'order': 2,
            'name': 'Node creation',
            'status': 'SUCCESS',
            'desc': 'The node is rebuilt with the same specifications.',
            'beginTime': '2024-07-19T09:13:00',
            'endTime': '2024-07-19T09:14:43',
        },
        {
            'order': 3,
            'name': 'Connectivity test',
            'status': 'SUCCESS',
            'desc': 'Node creation is verified.',
            'beginTime': '2024-07-19T09:14:47',
            'endTime': '2024-07-19T09:15:19',
        },
    ],
    'failMessage': '[402c6c3]RdsBindExistPortToInstanceTask-fail:null',
}


class TestClusterUpgradeStatus(base.TestCase):
    def setUp(self):
        super(TestClusterUpgradeStatus, self).setUp()

    def test_basic(self):
        sot = cluster_upgrade_status.ClusterUpgradeStatus()

        self.assertEqual(
            '/clusters/%(cluster_id)s/upgrade/detail', sot.base_path
        )
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('detailList', sot.resources_key)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        updated_sot_attrs = {
            'startTime': 'start_time',
            'endTime': 'end_time',
            'agencyName': 'agency_name',
            'totalNodes': 'total_nodes',
            'completedNodes': 'completed_nodes',
            'currentNodeName': 'current_node_name',
            'executeTimes': 'execute_times',
            'failMessage': 'fail_message',
        }
        sot = cluster_upgrade_status.ClusterUpgradeStatus(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key in updated_sot_attrs.keys():
                self.assertEqual(
                    getattr(sot, updated_sot_attrs[key]), EXAMPLE[key]
                )
            elif key == 'imageInfo':
                pass
            elif key == 'currentNodeDetail':
                pass
            else:
                assert_attributes_equal(self, getattr(sot, key), value)
