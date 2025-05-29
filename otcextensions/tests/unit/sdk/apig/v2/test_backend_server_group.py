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
from otcextensions.sdk.apig.v2 import backend_server_group

EXAMPLE_LABEL = {
    'label_name': 'env',
    'label_value': 'prod'
}

EXAMPLE_GROUP = {
    'gateway_id': 'gw-001',
    'vpc_channel_id': 'vpc-123',
    'member_group_name': 'backend-group',
    'member_group_remark': 'test group',
    'member_group_weight': 50,
    'dict_code': 'code-001',
    'microservice_version': '1.0.0',
    'microservice_port': 8080,
    'microservice_labels': [EXAMPLE_LABEL],
    'member_group_id': 'mg-123',
    'create_time': '2025-01-01T10:00:00Z',
    'update_time': '2025-01-02T10:00:00Z'
}


class TestBackendServerGroup(base.TestCase):

    def test_basic(self):
        sot = backend_server_group.BackendServerGroup()
        self.assertEqual(
            'apigw/instances/%(gateway_id)s/vpc-channels/'
            '%(vpc_channel_id)s/member-groups',
            sot.base_path
        )
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = backend_server_group.BackendServerGroup(**EXAMPLE_GROUP)
        self.assertEqual(EXAMPLE_GROUP['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_GROUP['vpc_channel_id'], sot.vpc_channel_id)
        self.assertEqual(EXAMPLE_GROUP['member_group_name'],
                         sot.member_group_name)
        self.assertEqual(EXAMPLE_GROUP['member_group_remark'],
                         sot.member_group_remark)
        self.assertEqual(EXAMPLE_GROUP['member_group_weight'],
                         sot.member_group_weight)
        self.assertEqual(EXAMPLE_GROUP['dict_code'], sot.dict_code)
        self.assertEqual(EXAMPLE_GROUP['microservice_version'],
                         sot.microservice_version)
        self.assertEqual(EXAMPLE_GROUP['microservice_port'],
                         sot.microservice_port)
        self.assertEqual(EXAMPLE_GROUP['member_group_id'],
                         sot.member_group_id)
        self.assertEqual(EXAMPLE_GROUP['create_time'], sot.create_time)
        self.assertEqual(EXAMPLE_GROUP['update_time'], sot.update_time)

        self.assertEqual(1, len(sot.microservice_labels))
        self.assertEqual('env', sot.microservice_labels[0].label_name)
        self.assertEqual('prod', sot.microservice_labels[0].label_value)
