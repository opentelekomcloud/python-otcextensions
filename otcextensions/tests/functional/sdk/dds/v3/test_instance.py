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
import uuid

from otcextensions.tests.functional.sdk.dds import TestDds


class TestInstance(TestDds):
    uuid_v4 = uuid.uuid4().hex[:8]
    network = None
    instance = None

    def setUp(self):
        super(TestInstance, self).setUp()

    def create_network(self):
        cidr = '192.168.0.0/16'
        ipv4 = 4
        router_name = 'sdk-dds-test-router-' + self.uuid_v4
        net_name = 'sdk-dds-test-net-' + self.uuid_v4
        subnet_name = 'sdk-dds-test-subnet-' + self.uuid_v4

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

    def test_01_create_instance(self):
        security_group = self.net_client.find_security_group(
            name_or_id='default', ignore_missing=False)
        self.network = self.create_network()
        name = 'test-dds-' + self.uuid_v4
        datastore = {
            'type': 'DDS-Community',
            'version': '3.4',
            'storage_engine': 'wiredTiger'
        }
        region = 'eu-de'
        availability_zone = 'eu-de-01'
        vpc_id = self.network['router_id']
        subnet_id = self.network['network_id']
        security_group_id = security_group.id
        password = 'Test@123!'
        mode = 'Sharding'
        flavor = [
            {
                "type": "mongos",
                "num": 2,
                "spec_code": "dds.mongodb.s2.medium.4.mongos"
            },
            {
                "type": "shard",
                "num": 2,
                "storage": "ULTRAHIGH",
                "size": 20,
                "spec_code": "dds.mongodb.s2.medium.4.shard"
            },
            {
                "type": "config",
                "num": 1,
                "storage": "ULTRAHIGH",
                "size": 20,
                "spec_code": "dds.mongodb.s2.large.2.config"
            }
        ]
        backup_strategy = {
            'start_time': '23:00-00:00',
            'keep_days': '8'
        }
        self.instance = self.client.create_instance(
            name=name,
            datastore=datastore,
            region=region,
            availability_zone=availability_zone,
            vpc_id=vpc_id,
            subnet_id=subnet_id,
            security_group_id=security_group_id,
            password=password,
            mode=mode,
            flavor=flavor,
            backup_strategy=backup_strategy
        )
        self.assertIsNotNone(self.instance)

    def test_02_list_instances(self):
        instances = list(self.client.instances())
        self.assertIsNotNone(instances)

    def test_03_get_instance(self):
        instance = self.client.get_instance(id=self.instance.id)
        self.assertIsNotNone(instance)

    def test_04_find_instance(self):
        instance = self.client.find_instance(name_or_id=self.instance.name)
        self.assertIsNotNone(instance)

    def test_05_delete_instance(self):
        instance = None
        try:
            instance = self.client.delete_instance(instance=self.instance)
        except Exception:
            self.destroy_network(self.network)
        self.assertIsNotNone(instance)
