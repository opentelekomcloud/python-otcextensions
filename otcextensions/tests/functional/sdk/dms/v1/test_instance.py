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
import openstack
from openstack import exceptions
from openstack import resource

# from openstack import utils
from openstack.tests.functional.network.v2 import test_network
from openstack.network.v2 import security_group
from openstack.network.v2 import network
from openstack.network.v2 import router
from openstack.network.v2 import subnet


from otcextensions.tests.functional import base
import time
import uuid
import random

_logger = openstack._log.setup_logging('openstack')


class TestInstance(base.BaseFunctionalTest):
    UUID = uuid.uuid4().hex[:8]
    INSTANCE_NAME = 'sdk-test-dms-' + UUID
    ROUTER_NAME = 'sdk-test-router-' + UUID
    NET_NAME = 'sdk-test-net-' + UUID
    SUBNET_NAME = 'sdk-test-subnet-' + UUID
    SG_NAME = 'sdk-test-sg-' + UUID
    ROUTER_ID = None
    NET_ID = None
    SUBNET_ID = None
    SG_ID = None
    instances = []

    def setUp(self):
        super(TestInstance, self).setUp()
        self._initialize_network()
        openstack.enable_logging(debug=True, http_debug=True)
        products=list(self.conn.dms.products())
        products_ids=[product.product_id for product in products]
        product_id=random.choice(products_ids)
        availability_zone_names=[
            product.availability_zones for product in products
            if product_id == product.product_id
            ]
        availability_zone_name=random.choice(sum(availability_zone_names, []))
        availability_zones=[
            availability_zone.id
            for availability_zone in self.conn.dms.availability_zones()
            ]
        availability_zone_id=[
            availability_zone.id
            for availability_zone in self.conn.dms.availability_zones()
            if availability_zone_name == availability_zone.code
            ]
        try:
            self.instance = self.conn.dms.create_instance(
                name=self.INSTANCE_NAME,
                engine="kafka", engine_version="2.3.0", storage=4800,
                router_id=self.ROUTER_ID, network_id=self.NET_ID,
                security_group_id=self.SG_ID,
                availability_zones=availability_zone_id,
                product_id=product_id,
                storage_spec_code="dms.physical.storage.ultra"
            )
        except exceptions.DuplicateResource:
            self.instance = self.conn.dms.find_instance(
                alias=self.INSTANCE_NAME
            )
        resource.wait_for_status(
            session=self.conn.dms,
            resource=self.instance,
            status='RUNNING',
            failures=['CREATEFAILED'],
            interval=5,
            wait=900)
        self.assertIn('instance_id', self.instance)
        self.instances.append(self.instance)
    def tearDown(self):
        super(TestInstance, self).tearDown()
        openstack.enable_logging(debug=True, http_debug=True)
        try:
            for instance in self.instances:
                if instance.id:
                    self.conn.dms.delete_instance(instance)
                    resource.wait_for_delete(
                        session=self.conn.dms,
                        resource=instance,
                        interval=2,
                        wait=60)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)
        self._deinitialize_network()

    def test_list(self):
        self.all_instances = list(self.conn.dms.instances())
        self.assertGreaterEqual(len(self.all_instances), 0)
        if len(self.all_instances) > 0:
            instance = self.all_instances[0]
            instance = self.conn.dms.get_instance(instance=instance.id)
            self.assertIsNotNone(instance)

    def _initialize_network(self):
        openstack.enable_logging(debug=True, http_debug=True)
        self.cidr = '192.168.0.0/16'
        self.ipv4 = 4

        sg = self.conn.network.create_security_group(name=self.SG_NAME)
        assert isinstance(sg, security_group.SecurityGroup)
        self.assertEqual(self.SG_NAME, sg.name)
        TestInstance.SG_ID = sg.id

        network = self.conn.network.create_network(name=self.NET_NAME)
        self.assertEqual(self.NET_NAME, network.name)
        TestInstance.NET_ID = network.id

        subnet = self.conn.network.create_subnet(
            name=self.SUBNET_NAME,
            ip_version=self.ipv4,
            network_id=TestInstance.NET_ID,
            cidr=self.cidr
            )
        self.assertEqual(self.SUBNET_NAME, subnet.name)
        TestInstance.SUBNET_ID = subnet.id

        router = self.conn.network.create_router(name=self.ROUTER_NAME)
        self.assertEqual(self.ROUTER_NAME, router.name)
        TestInstance.ROUTER_ID = router.id
        interface = router.add_interface(self.conn.network,
                                         subnet_id=TestInstance.SUBNET_ID)
        self.assertEqual(interface['subnet_id'], TestInstance.SUBNET_ID)
        self.assertIn('port_id', interface)
        #add CIDR to Router for compatibility
        service = self.conn.identity.find_service('vpc')
        endpoints=list(self.conn.identity.endpoints(service_id=service.id))
        endpoint_url = endpoints[0].url
        endpoint = endpoint_url[:endpoint_url.rfind("/")+1];
        cidr = self.conn.compute.put(
            endpoint + self.conn.session.get_project_id() + '/vpcs/' +
            self.ROUTER_ID, data='{"vpc": {"cidr": "192.168.0.0/16"}}',
            headers={'content-type': 'application/json'})
        self.assertIn('cidr', cidr.json()['vpc'])
        self.assertIn('192.168.0.0/16', cidr.json()['vpc']['cidr'])

    def _deinitialize_network(self):
        router = self.conn.network.get_router(TestInstance.ROUTER_ID)
        interface = router.remove_interface(self.conn.network,
                                            subnet_id=TestInstance.SUBNET_ID)
        self.assertEqual(interface['subnet_id'], TestInstance.SUBNET_ID)
        self.assertIn('port_id', interface)
        sot = self.conn.network.delete_router(
            TestInstance.ROUTER_ID, ignore_missing=False)
        self.assertIsNone(sot)
        sot = self.conn.network.delete_subnet(
            TestInstance.SUBNET_ID, ignore_missing=False)
        self.assertIsNone(sot)
        sot = self.conn.network.delete_network(
            TestInstance.NET_ID, ignore_missing=False)
        self.assertIsNone(sot)
        sot = self.conn.network.delete_security_group(
            TestInstance.SG_ID, ignore_missing=False)
        self.assertIsNone(sot)
