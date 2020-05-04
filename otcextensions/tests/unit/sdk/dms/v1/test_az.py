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
from keystoneauth1 import adapter

from unittest import mock

from openstack.tests.unit import base

from otcextensions.sdk.dms.v1 import az


JSON_DATA = {
    'id': '1d7b939b382c4c3bb3481a8ca10da768',
    'name': 'az10.dc1',
    'code': 'az10.dc1',
    'port': '8002',
    'resource_availability': True
}

JSON_LIST = {
    'regionId': 'fake_region',
    'available_zones': [{
        'id': '1d7b939b382c4c3bb3481a8ca10da768',
        'name': 'az10.dc1',
        'code': 'az10.dc1',
        'port': '8002',
        'resource_availability': 'true'
    }, {
        'id': '1d7b939b382c4c3bb3481a8ca10da769',
        'name': 'az10.dc2',
        'code': 'az10.dc2',
        'port': '8002',
        'resource_availability': 'true'
    }]
}


class TestAZ(base.TestCase):

    def setUp(self):
        super(TestAZ, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.endpoint_override = 'fake/%(project_id)s'
        self.sess._get_connection = mock.Mock()

    def test_basic(self):
        sot = az.AvailabilityZone()

        self.assertEqual('/availableZones', sot.base_path)
        self.assertEqual('available_zones', sot.resources_key)

        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = az.AvailabilityZone(**JSON_DATA)
        self.assertEqual(JSON_DATA['id'], sot.id)
        self.assertEqual(JSON_DATA['name'], sot.name)
        self.assertEqual(JSON_DATA['code'], sot.code)
        self.assertEqual(JSON_DATA['port'], sot.port)
        self.assertEqual(JSON_DATA['resource_availability'],
                         sot.has_available_resources)

    def test_list(self):
        sot = az.AvailabilityZone()

        response = mock.Mock()
        response.status_code = 200
        response.json = mock.Mock(return_value=JSON_LIST)
        self.sess.get.return_value = response

        rsp = list(sot.list(self.sess))

        self.sess.get.assert_called_with(
            '/availableZones',
            endpoint_override='fake/',
            headers={'Accept': 'application/json'},
            params={}
        )

        self.assertIsInstance(rsp[0], az.AvailabilityZone)
        self.assertEqual(JSON_LIST['regionId'], rsp[0].region_id)
