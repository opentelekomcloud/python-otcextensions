#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import json
import uuid

from openstackclient.tests.functional import base


class DcaasTestCase(base.TestCase):
    """Common functional test bits for DCAAS commands"""

    UUID = uuid.uuid4().hex[:9]
    NETWORK_NAME = "test-dc-network-" + UUID
    SUBNET_NAME = "test-dc-subnet-" + UUID
    ROUTER_NAME = "test-dc-router-" + UUID
    IP_VERSION = 4
    CIDR = "192.168.0.0/16"
    EP_GROUP_NAME = "test-dc-eg-" + UUID
    EP_GROUP_TYPE = "cidr"

    def setUp(self):
        super(DcaasTestCase, self).setUp()
        self.create_test_infra()
        self.EP_GROUP_ID = self.create_endpoint_group()

    def tearDown(self):
        try:
            if self.EP_GROUP_ID:
                self.delete_endpoint_group()
        finally:
            self.delete_test_infra()
            super(DcaasTestCase, self).tearDown()

    def _get_project_id(self):
        json_output = json.loads(self.openstack(
            'token issue -f json'
        ))
        return json_output['project_id']

    def _create_network(self):
        json.loads(self.openstack(
            'network create -f json ' + self.NETWORK_NAME
        ))

    def _delete_network(self):
        json.loads(self.openstack('network delete ' + self.NETWORK_NAME))

    def _create_subnet(self):
        json.loads(self.openstack(
            'subnet create {subnet} -f json '
            '--network {network} '
            '--subnet-range {subnet_range} '.format(
                subnet=self.SUBNET_NAME,
                network=self.NETWORK_NAME,
                subnet_range=self.CIDR)
        ))

    def _delete_subnet(self):
        json.loads(self.openstack('subnet delete ' + self.SUBNET_NAME))

    def _create_router(self):
        json.loads(self.openstack(
            'router create -f json ' + self.ROUTER_NAME
        ))
        self.openstack(
            'router add subnet {router} {subnet} '.format(
                router=self.ROUTER_NAME,
                subnet=self.SUBNET_NAME
            )
        )

    def _router_remove_subnet(self):
        self.openstack(
            'router remove subnet {router} {subnet} '.format(
                router=self.ROUTER_NAME,
                subnet=self.SUBNET_NAME
            )
        )

    def _delete_router(self):
        json.loads(self.openstack('router delete ' + self.ROUTER_NAME))

    def create_test_infra(self):
        self._create_network()
        self._create_subnet()
        self._create_router()

    def delete_test_infra(self):
        self._router_remove_subnet()
        self._delete_subnet()
        self._delete_network()
        self._delete_router()

    def create_endpoint_group(self):
        project_id = self._get_project_id()
        endpoints = [self.CIDR]
        json_output = json.loads(self.openstack(
            'dcaas endpoint group create '
            '{project_id} '
            '{endpoints} '
            '{type} '
            '--name {name} -f json'.format(
                name=self.EP_GROUP_NAME,
                project_id=project_id,
                endpoints=endpoints,
                type=self.EP_GROUP_TYPE
            )
        ))
        return json_output['id']

    def delete_endpoint_group(self):
        json.loads(self.openstack(
            'dcaas endpoint group delete ' + self.EP_GROUP_NAME
        ))
