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

    UUID = uuid.uuid4().hex[:8]
    ROUTER_NAME = 'sdk-test-router-' + UUID
    NET_NAME = 'sdk-test-net-' + UUID
    SUBNET_NAME = 'sdk-test-subnet-' + UUID
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
            'cce cluster create '
            '{name} {router} {network} '
            '--description descr '
            '--flavor cce.s1.small '
            '--container-network-mode overlay_l2 '
            '--wait --wait-interval 10 '
            '-f json'.format(
                name=self.CLUSTER_NAME,
                router=self.ROUTER_NAME,
                network=self.NET_NAME
            )
        )

        json_output = json.loads(self.openstack(cmd))

        self.assertIsNotNone(json_output['id'])

    def test_03_cluster_delete(self):
        self.addCleanup(self._deinitialize_network)
        self.openstack(
            'cce cluster delete {name}'.format(
                name=self.CLUSTER_NAME
            )
        )

    def _initialize_network(self):
        router = json.loads(self.openstack(
            'router create -f json ' + self.ROUTER_NAME
        ))
        net = json.loads(self.openstack(
            'network create -f json ' + self.NET_NAME
        ))
        self.openstack(
            'subnet create {subnet} -f json '
            '--network {net} '
            '--subnet-range 192.168.0.0/24 '.format(
                subnet=self.SUBNET_NAME,
                net=self.NET_NAME
            )
        )

        self.openstack(
            'router add subnet {router} '
            '{subnet} '.format(
                router=self.ROUTER_NAME,
                subnet=self.SUBNET_NAME
            )
        )

        self.ROUTER_ID = router['id']
        self.NET_ID = net['id']

    def _deinitialize_network(self):
        self.openstack(
            'router remove subnet {router} '
            '{subnet} '.format(
                router=self.ROUTER_NAME,
                subnet=self.SUBNET_NAME
            )
        )
        self.openstack(
            'subnet delete ' + self.SUBNET_NAME
        )
        self.openstack(
            'network delete ' + self.NET_NAME
        )
        self.openstack(
            'router delete ' + self.ROUTER_NAME
        )
