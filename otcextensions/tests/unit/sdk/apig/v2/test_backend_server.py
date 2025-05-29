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
from otcextensions.sdk.apig.v2 import backend_server

EXAMPLE_MEMBER = {
    'gateway_id': 'gw-123',
    'vpc_chan_id': 'vpc-456',
    'host': '192.168.1.10',
    'weight': 20,
    'is_backup': True,
    'member_group_name': 'group-A',
    'status': 1,
    'port': 8080,
    'ecs_id': 'ecs-123',
    'ecs_name': 'ecs-node-A',
    'id': 'mem-001',
    'vpc_channel_id': 'vpc-456',
    'create_time': '2025-01-01T12:00:00Z',
    'member_group_id': 'mg-001'
}


class TestBackendServer(base.TestCase):

    def test_basic(self):
        sot = backend_server.BackendServer()
        self.assertEqual(
            'apigw/instances/%(gateway_id)s/vpc-channels/%(vpc_chan_id)s/'
            'members',
            sot.base_path
        )
        self.assertEqual('members', sot.resources_key)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = backend_server.BackendServer(**EXAMPLE_MEMBER)
        self.assertEqual(EXAMPLE_MEMBER['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_MEMBER['vpc_chan_id'], sot.vpc_chan_id)
        self.assertEqual(EXAMPLE_MEMBER['host'], sot.host)
        self.assertEqual(EXAMPLE_MEMBER['weight'], sot.weight)
        self.assertEqual(EXAMPLE_MEMBER['is_backup'], sot.is_backup)
        self.assertEqual(EXAMPLE_MEMBER['member_group_name'],
                         sot.member_group_name)
        self.assertEqual(EXAMPLE_MEMBER['status'], sot.status)
        self.assertEqual(EXAMPLE_MEMBER['port'], sot.port)
        self.assertEqual(EXAMPLE_MEMBER['ecs_id'], sot.ecs_id)
        self.assertEqual(EXAMPLE_MEMBER['ecs_name'], sot.ecs_name)
        self.assertEqual(EXAMPLE_MEMBER['id'], sot.id)
        self.assertEqual(EXAMPLE_MEMBER['vpc_channel_id'], sot.vpc_channel_id)
        self.assertEqual(EXAMPLE_MEMBER['create_time'], sot.create_time)
        self.assertEqual(EXAMPLE_MEMBER['member_group_id'],
                         sot.member_group_id)
