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

import os
import uuid

from keystoneauth1 import exceptions as _exceptions

import openstack.config
from openstack import connection
from openstack.tests import base

from otcextensions import sdk


#: Defines the OpenStack Client Config (OCC) cloud key in your OCC config
#: file, typically in $HOME/.config/openstack/clouds.yaml. That configuration
#: will determine where the functional tests will be run and what resource
#: defaults will be used to run the functional tests.
TEST_CLOUD_NAME = os.getenv('OS_CLOUD', 'otc')
TEST_CLOUD_REGION = openstack.config.get_cloud_region(cloud=TEST_CLOUD_NAME)


def _get_resource_value(resource_key, default):
    try:
        return TEST_CLOUD_REGION.config['functional'][resource_key]
    except KeyError:
        return default


IMAGE_NAME = _get_resource_value('image_name', 'cirros-0.3.5-x86_64-disk')
FLAVOR_NAME = _get_resource_value('flavor_name', 'm1.small')


class BaseFunctionalTest(base.TestCase):

    def setUp(self):
        super(BaseFunctionalTest, self).setUp()
        self.conn = connection.Connection(config=TEST_CLOUD_REGION)
        sdk.register_otc_extensions(self.conn)

    def addEmptyCleanup(self, func, *args, **kwargs):
        def cleanup():
            result = func(*args, **kwargs)
            self.assertIsNone(result)
        self.addCleanup(cleanup)

    # TODO(shade) Replace this with call to conn.has_service when we've merged
    #             the shade methods into Connection.
    def require_service(self, service_type, **kwargs):
        """Method to check whether a service exists

        Usage:
        class TestMeter(base.BaseFunctionalTest):
            ...
            def setUp(self):
                super(TestMeter, self).setUp()
                self.require_service('metering')

        :returns: True if the service exists, otherwise False.
        """
        try:
            self.conn.session.get_endpoint(service_type=service_type, **kwargs)
        except _exceptions.EndpointNotFound:
            self.skipTest('Service {service_type} not found in cloud'.format(
                service_type=service_type))


class NetworkBaseFunctionalTest(BaseFunctionalTest):
    def create_network(self, prefix='sdk-test'):
        cidr = '192.168.0.0/16'
        ipv4 = 4
        uuid_v4 = uuid.uuid4().hex[:8]
        router_name = prefix + '-router-' + uuid_v4
        net_name = prefix + '-net-' + uuid_v4
        subnet_name = prefix + '-subnet-' + uuid_v4

        network = self.conn.network.create_network(name=net_name)
        self.assertEqual(net_name, network.name)
        net_id = network.id
        subnet = self.conn.network.create_subnet(
            name=subnet_name,
            ip_version=ipv4,
            network_id=net_id,
            cidr=cidr
        )
        self.assertEqual(subnet_name, subnet.name)
        subnet_id = subnet.id

        router = self.conn.network.create_router(name=router_name)
        self.assertEqual(router_name, router.name)
        router_id = router.id
        interface = router.add_interface(
            self.conn.network,
            subnet_id=subnet_id
        )
        self.assertEqual(interface['subnet_id'], subnet_id)
        self.assertIn('port_id', interface)
        return {
            'router_id': router_id,
            'subnet_id': subnet_id,
            'network_id': net_id
        }

    def destroy_network(self, params: dict):
        router_id = params.get('router_id')
        subnet_id = params.get('subnet_id')
        network_id = params.get('network_id')
        router = self.conn.network.get_router(router_id)

        interface = router.remove_interface(
            self.conn.network,
            subnet_id=subnet_id
        )
        self.assertEqual(interface['subnet_id'], subnet_id)
        self.assertIn('port_id', interface)
        sot = self.conn.network.delete_router(
            router_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.conn.network.delete_subnet(
            subnet_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.conn.network.delete_network(
            network_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)

    def create_port(self, network_id, prefix='sdk-test'):
        uuid_v4 = uuid.uuid4().hex[:8]
        port_name = prefix + '-port-' + uuid_v4

        port = self.conn.network.create_port(
            name=port_name,
            network_id=network_id
        )
        self.assertEqual(port_name, port.name)
        return port

    def destroy_port(self, port):
        sot = self.conn.network.delete_port(
            port,
            ignore_missing=False
        )
        self.assertIsNone(sot)
