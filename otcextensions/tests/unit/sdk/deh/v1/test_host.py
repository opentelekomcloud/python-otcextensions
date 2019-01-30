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

from otcextensions.sdk.deh.v1 import host


FAKE_ID = '68d5745e-6af2-40e4-945d-fe449be00148'
EXAMPLE = {
    'dedicated_host_id': FAKE_ID,
    'name': 'win_2008 servers',
    'auto_placement': 'off',
    'availability_zone': 'az1',
    'host_properties': {
        'vcpus': 36,
        'cores': 12,
        'sockets': 2,
        'memory': 1073741824,
        'host_type': 'h1',
        'host_type_name': 'High performance',
        'available_instance_capacities': [
            {
                'flavor': 'h1.large'
            },
            {
                'flavor': 'h1.2large'
            },
            {
                'flavor': 'h1.4large'
            },
            {
                'flavor': 'h1.8large'
            }
        ]
    },
    'state': 'available',
    'project_id': '9c53a566cb3443ab910cf0daebca90c4',
    'available_vcpus': 20,
    'available_memory': 1073201821,
    'instance_total': 2,
    'allocated_at': '2016-10-10T14:35:47Z',
    'released_at': None,
    'instance_uuids': [
        'erf5th66cb3443ab912ff0daebca3456',
        '23457h66cb3443ab912ff0daebcaer45'
    ]
}


class TestHost(base.TestCase):

    def test_basic(self):
        sot = host.Host()

        self.assertEqual('/dedicated-hosts', sot.base_path)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_update)

    def test_make_it(self):

        sot = host.Host(**EXAMPLE)
        self.assertEqual(EXAMPLE['dedicated_host_id'], FAKE_ID)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['auto_placement'], sot.auto_placement)
        self.assertEqual(EXAMPLE['availability_zone'], sot.availability_zone)
        self.assertEqual(EXAMPLE['state'], sot.state)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['available_vcpus'], sot.available_vcpus)
        self.assertEqual(EXAMPLE['available_memory'], sot.available_memory)
        self.assertEqual(EXAMPLE['instance_total'], sot.instance_total)
        self.assertEqual(EXAMPLE['released_at'], sot.released_at)
        ref = EXAMPLE['host_properties']
        actual = sot.host_properties
        self.assertEqual(ref['vcpus'], actual.vcpus)
        self.assertEqual(ref['cores'], actual.cores)
        self.assertEqual(ref['sockets'], actual.sockets)
        self.assertEqual(ref['memory'], actual.memory)
        self.assertEqual(ref['host_type'], actual.host_type)
        self.assertEqual(ref['host_type_name'], actual.host_type_name)
