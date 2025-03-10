#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import uuid
import json

from openstackclient.tests.functional import base


class TestCce(base.TestCase):
    """Functional tests for CCE Instance. """

    UUID = uuid.uuid4().hex[:4]
    ROUTER_NAME = 'sdk--cce-test-router-' + UUID
    NET_NAME = 'sdk-cce-test-net-' + UUID
    SUBNET_NAME = 'sdk-cce-test-subnet-' + UUID
    ROUTER_ID = None
    NET_ID = None

    CLUSTER_NAME = 'sdk-test-cce-' + UUID

    def test_01_cluster_list(self):
        self.openstack(
            'cce cluster list -f json '
        )

    def test_02_cluster_create(self):
        self._initialize_network()
        cmd = (
            f'cce cluster create '
            f'{self.CLUSTER_NAME} {self.ROUTER_NAME} {self.NET_NAME} '
            f'--description descr '
            f'--flavor cce.s1.small '
            f'--container-network-mode overlay_l2 '
            f'--wait --wait-interval 10 '
            f'-f json'
        )

        json_output = json.loads(self.openstack(cmd))

        self.assertIsNotNone(json_output['ID'])

    def test_03_cluster_delete(self):
        self.addCleanup(self._deinitialize_network)
        self.openstack(
            f'cce cluster delete {self.CLUSTER_NAME} --wait --wait-interval 10'
        )

    def _initialize_network(self):
        router = json.loads(self.openstack(
            'router create -f json ' + self.ROUTER_NAME
        ))
        self.assertIsNotNone(router)

        net = json.loads(self.openstack(
            'network create -f json ' + self.NET_NAME
        ))
        self.assertIsNotNone(net)

        subnet = json.loads(self.openstack(
            f'subnet create {self.SUBNET_NAME} '
            f'-f json --network {self.NET_NAME} '
            f'--subnet-range 192.168.0.0/24'
        ))
        self.assertIsNotNone(subnet)

        self.openstack(
            f'router add subnet {self.ROUTER_NAME} {self.SUBNET_NAME}'
        )

        self.ROUTER_ID = router['id']
        self.NET_ID = net['id']

    def _deinitialize_network(self):
        self.openstack(
            f'router remove subnet {self.ROUTER_NAME} {self.SUBNET_NAME}'
            )
        self.openstack('subnet delete ' + self.SUBNET_NAME)
        self.openstack('network delete ' + self.NET_NAME)
        self.openstack('router delete ' + self.ROUTER_NAME)
