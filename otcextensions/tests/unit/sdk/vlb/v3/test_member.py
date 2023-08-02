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

from otcextensions.sdk.vlb.v3 import member

EXAMPLE = {
    'address': 'address',
    'created_at': 'created-at',
    'ip_version': 'ip-version',
    'instance_id': 'instance-id',
    'admin_state_up': True,
    'name': 'name',
    'member_type': 'member-type',
    'subnet_cidr_id': 'subnet-id',
    'operating_status': 'operating-status',
    'project_id': 'project-id',
    'protocol_port': 80,
    'status': [],
    'weight': 5,
    'updated_at': 'updated-at'
}


class TestLoadBalancer(base.TestCase):

    def test_basic(self):
        sot = member.Member()
        path = '/elb/pools/%(pool_id)s/members'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = member.Member(**EXAMPLE)
        self.assertEqual(EXAMPLE['address'], sot.address)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['ip_version'], sot.ip_version)
        self.assertEqual(EXAMPLE['instance_id'], sot.instance_id)
        self.assertEqual(EXAMPLE['admin_state_up'], sot.is_admin_state_up)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['member_type'], sot.member_type)
        self.assertEqual(EXAMPLE['subnet_id'], sot.subnet_cidr_id)
        self.assertEqual(EXAMPLE['operating_status'], sot.operating_status)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['protocol_port'], sot.protocol_port)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['weight'], sot.weight)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
