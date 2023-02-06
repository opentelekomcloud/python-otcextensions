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
import mock

from keystoneauth1 import adapter
from openstack.tests.unit import base

from otcextensions.sdk.vpc.v1 import bandwidth

EXAMPLE = {
    'id': 'bandwidth-id',
    'name': 'bandwidth123',
    'size': 10,
    'share_type': 'WHOLE',
    'publicip_info': [
        {
            'publicip_id': 'publicip-id',
            'publicip_type': '5_bgp'
        }
    ],
    'bandwidth_type': 'share',
    'charge_mode': 'traffic',
    'billing_info': '',
    'enterprise_project_id': '0',
    'status': 'NORMAL',
    'created_at': '2020-04-21T07:58:02Z',
    'updated_at': '2020-04-21T07:58:02Z',
}


class TestBandwidth(base.TestCase):

    def setUp(self):
        super(TestBandwidth, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.default_microversion = None
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.retriable_status_codes = ()
        self.sot = bandwidth.Bandwidth()

    def test_basic(self):
        sot = bandwidth.Bandwidth()
        self.assertEqual('bandwidth', sot.resource_key)
        self.assertEqual('bandwidths', sot.resources_key)
        self.assertEqual('/v2.0/%(project_id)s/bandwidths', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = bandwidth.Bandwidth.existing(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['size'], sot.size)
        self.assertEqual(EXAMPLE['share_type'], sot.share_type)
        self.assertEqual(
            EXAMPLE['publicip_info'][0]['publicip_id'],
            sot.publicip_info[0]['publicip_id'])
        self.assertEqual(
            EXAMPLE['publicip_info'][0]['publicip_type'],
            sot.publicip_info[0]['publicip_type'])
        self.assertEqual(EXAMPLE['bandwidth_type'], sot.bandwidth_type)
        self.assertEqual(EXAMPLE['charge_mode'], sot.charge_mode)
        self.assertEqual(EXAMPLE['billing_info'], sot.billing_info)
        self.assertEqual(EXAMPLE['enterprise_project_id'],
                         sot.enterprise_project_id)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
