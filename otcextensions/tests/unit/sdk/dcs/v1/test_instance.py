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

from otcextensions.sdk.dcs.v1 import instance

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "name": "dcs-a11e",
    "engine": "Redis",
    "capacity": 2,
    "ip": "192.168.3.100",
    "port": 6379,
    "status": "RUNNING",
    "description": "Create a instance",
    "instance_id": FAKE_ID,
    "resource_spec_code": "dcs.single_node",
    "engine_version": "3.0.7",
    "internal_version": None,
    "charging_mode": 0,
    "vpc_id": "27d99e17-42f2-4751-818f-5c8c6c03ff15",
    "vpc_name": "vpc_4944a40e-ac57-4f08-9d38-9786e2759458_192",
    "created_at": "2017-03-31T12:24:46.297Z",
    "error_code": None,
    "product_id": "XXXXXX",
    "security_group_id": "60ea2db8-1a51-4ab6-9e11-65b418c24583",
    "security_group_name": "sg_6379_4944a40e-ac57-4f08-9d38-9786e2759458",
    "subnet_id": "ec2f34b9-20eb-4872-85bd-bea9fc943128",
    "subnet_name": "subnet_az_7f336767-10ec-48a5-9ae8-9cacde119318",
    "available_zones": "XXXXXX",
    "max_memory": 460,
    "used_memory": 56,
    "user_id": "6d0977e4c9b74ae7b5a083a8d0d8fafa",
    "user_name": "liutao02",
    "order_id": "XXXXXXXXX",
    "maintain_begin": "22:00:00",
    "maintain_end": "02:00:00"
}


class TestInstance(base.TestCase):

    def setUp(self):
        super(TestInstance, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = instance.Instance()

        self.assertEqual('/instances', sot.base_path)

        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):

        sot = instance.Instance(**EXAMPLE)
        self.assertEqual(EXAMPLE['instance_id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['engine'], sot.engine)
        self.assertEqual(EXAMPLE['capacity'], sot.capacity)
        self.assertEqual(EXAMPLE['ip'], sot.ip)
        self.assertEqual(EXAMPLE['port'], sot.port)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['resource_spec_code'], sot.resource_spec_code)
        self.assertEqual(EXAMPLE['engine_version'], sot.engine_version)
        self.assertEqual(EXAMPLE['internal_version'], sot.internal_version)
        self.assertEqual(EXAMPLE['charging_mode'], sot.charging_mode)
        self.assertEqual(EXAMPLE['vpc_id'], sot.vpc_id)
        self.assertEqual(EXAMPLE['vpc_name'], sot.vpc_name)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['error_code'], sot.error_code)
        self.assertEqual(EXAMPLE['product_id'], sot.product_id)
        self.assertEqual(EXAMPLE['security_group_id'], sot.security_group_id)
        self.assertEqual(EXAMPLE['security_group_name'],
                         sot.security_group_name)
        self.assertEqual(EXAMPLE['subnet_id'], sot.subnet_id)
        self.assertEqual(EXAMPLE['subnet_name'], sot.subnet_name)
        self.assertEqual(EXAMPLE['available_zones'], sot.available_zones)
        self.assertEqual(EXAMPLE['max_memory'], sot.max_memory)
        self.assertEqual(EXAMPLE['used_memory'], sot.used_memory)
        self.assertEqual(EXAMPLE['user_id'], sot.user_id)
        self.assertEqual(EXAMPLE['user_name'], sot.user_name)
        self.assertEqual(EXAMPLE['maintain_begin'], sot.maintain_begin)
        self.assertEqual(EXAMPLE['maintain_end'], sot.maintain_end)

    def test_stop(self):

        sot = instance.Instance(**EXAMPLE)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {}

        self.sess.put.return_value = mock_response

        sot.stop(self.sess)

        self.sess.put.assert_called_once_with(
            'instances/status',
            json={
                'action': 'stop',
                'instances': [FAKE_ID]}
        )

    def test_start(self):

        sot = instance.Instance(**EXAMPLE)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {}

        self.sess.put.return_value = mock_response

        sot.start(self.sess)

        self.sess.put.assert_called_once_with(
            'instances/status',
            json={
                'action': 'start',
                'instances': [FAKE_ID]}
        )

    def test_restart(self):

        sot = instance.Instance(**EXAMPLE)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {}

        self.sess.put.return_value = mock_response

        sot.restart(self.sess)

        self.sess.put.assert_called_once_with(
            'instances/status',
            json={
                'action': 'restart',
                'instances': [FAKE_ID]}
        )
