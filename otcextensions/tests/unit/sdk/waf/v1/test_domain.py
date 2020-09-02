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

from otcextensions.sdk.waf.v1 import domain


FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "id": FAKE_ID,
    "hostname": "www.b.com",
    "cname": "3249d21e5eb34d21be12fdc817fcb67d.waf.cloud.com",
    "txt_code": "3249d21e5eb34d21be12fdc817fcb67d",
    "sub_domain": "3249d21e5eb34d21be12fdc817fcb67d.www.b.com",
    "policy_id": "xxxxxxxxxxxxxx",
    "certificate_id": "xxxxxxxxxxxxxxxxxxx",
    "protect_status": 0,
    "access_status": 0,
    "protocol": "HTTP,HTTPS",
    "server": [
        {
            "client_protocol": "HTTPS",
            "server_protocol": "HTTP",
            "address": "X.X.X.X",
            "port": 443
        }, {
            "client_protocol": "HTTP",
            "server_protocol": "HTTP",
            "address": "X.X.X.X",
            "port": 80
        }
    ],
    "proxy": True,
    "sip_header_name": "default",
    "sip_header_list": ["X-Forwarded-For"],
    "timestamp": 1499817600
}


class TestDomain(base.TestCase):

    def setUp(self):
        super(TestDomain, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

    def test_basic(self):
        sot = domain.Domain()

        self.assertEqual('/waf/instance', sot.base_path)
        self.assertEqual('items', sot.resources_key)
        self.assertIsNone(sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):

        sot = domain.Domain(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['hostname'], sot.name)
        self.assertEqual(EXAMPLE['hostname'], sot.hostname)
        self.assertEqual(EXAMPLE['access_status'], sot.access_status)
        self.assertEqual(EXAMPLE['certificate_id'], sot.certificate_id)
        self.assertEqual(len(EXAMPLE['server']), len(sot.server))

        self.assertDictEqual({
            'hostname': 'hostname',
            'limit': 'limit',
            'marker': 'marker',
            'name': 'hostname',
            'offset': 'offset',
            'policy_name': 'policyname'},
            sot._query_mapping._mapping
        )
