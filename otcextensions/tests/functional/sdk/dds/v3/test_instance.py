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
import time


from otcextensions.tests.functional.sdk.dds import TestDds

shared_data = {}

class TestInstance(TestDds):
    uuid_v4 = uuid.uuid4().hex[:8]
    network = None
    instance = None

    def setUp(self):
        super(TestInstance, self).setUp()

    # def create_network(self):
    #     cidr = '192.168.0.0/16'
    #     ipv4 = 4
    #     router_name = 'sdk-dds-test-router-' + self.uuid_v4
    #     net_name = 'sdk-dds-test-net-' + self.uuid_v4
    #     subnet_name = 'sdk-dds-test-subnet-' + self.uuid_v4
    #
    #     network = self.conn.network.create_network(name=net_name)
    #     self.assertEqual(net_name, network.name)
    #     net_id = network.id
    #     subnet = self.conn.network.create_subnet(
    #         name=subnet_name,
    #         ip_version=ipv4,
    #         network_id=net_id,
    #         cidr=cidr
    #     )
    #     self.assertEqual(subnet_name, subnet.name)
    #     subnet_id = subnet.id
    #
    #     router = self.conn.network.create_router(name=router_name)
    #     self.assertEqual(router_name, router.name)
    #     router_id = router.id
    #     interface = router.add_interface(
    #         self.conn.network,
    #         subnet_id=subnet_id
    #     )
    #     self.assertEqual(interface['subnet_id'], subnet_id)
    #     self.assertIn('port_id', interface)
    #     return {
    #         'router_id': router_id,
    #         'subnet_id': subnet_id,
    #         'network_id': net_id
    #     }
    def create_network(self):
        return {
                'router_id': '8cfcc486-5b67-4e65-ab5c-c0f3de3bf12e',
                'subnet_id': 'fca51a32-edec-4c45-bfd5-1c2606f456a0',
                'network_id': 'eb15b01f-3f32-411f-9ab7-c8617b5c0942'
            }

    def wait_job_to_finish(self):
        while True:
            job = self.client.get_job(shared_data['instance']['job_id'])
            if job['status'] != 'Running':
                self.assertIsNotNone(job)
                break
            time.sleep(1)

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
        shared_data['network'] = self.network
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
        self.instance  = (
        self.client.create_instance(
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
        ))
        shared_data['instance'] = self.instance
        self.assertIsNotNone(self.instance)

    def test_02_list_instances(self):
        instances = list(self.client.instances())
        self.assertIsNotNone(instances)

    def test_03_get_instance(self):
        instance = self.client.get_instance(shared_data['instance']['id'])
        self.assertIsNotNone(instance)

    def test_04_find_instance(self):
        instance = self.client.find_instance(name_or_id=shared_data['instance']['name'])
        self.assertIsNotNone(instance)

    def test_05_enlarge_instance(self):
        self.wait_job_to_finish()
        instance = self.client.get_instance(shared_data['instance']['id'])
        group_id = [item for item in instance['groups'] if item['type'] == 'shard'][0]['id']
        result = self.client.enlarge_instance(shared_data['instance']['id'], size=60, group_id=group_id)
        self.assertIsNot(shared_data['instance']['job_id'], result['job_id'])
        shared_data['instance']['job_id'] = result['job_id']
        # job

    def test_06_adding_nodes(self):
        self.wait_job_to_finish()
        attrs = {
            "node_type": "mongos",
            "spec_code":"dds.mongodb.s2.medium.4.mongos",
            "num": 1
        }
        result = self.client.add_instance_nodes(shared_data['instance']['id'], **attrs)
        self.assertIsNot(shared_data['instance']['job_id'], result['job_id'])
        shared_data['instance']['job_id'] = result['job_id']

    def test_08_modify_instance_specs(self):
        self.wait_job_to_finish()
        attrs = {
            "target_id": 1,
            "target_spec_code": "dds.mongodb.s2.large.4.mongos"
        }
        result = self.client.resize_instance(shared_data['instance']['id'], **attrs)
        self.assertIsNotNone(result)
        # job

    def test_09_switchover(self):
        instance = self.client.switchover_instance(shared_data['instance']['id'])
        self.assertIsNotNone(instance)
        # job

    def test_10_enable_ssl(self):
        instance = self.client.enable_instance_ssl(shared_data['instance']['id'])
        self.assertIsNotNone(instance)
        # job

    def test_11_change_name(self):
        instance = self.client.change_insance_name(shared_data['instance']['id'], name = 'new_name')
        self.assertIsNotNone(instance)
        # ?

    def test_12_change_port(self):
        instance = self.client.change_instance_port(shared_data['instance']['id'], port=8888)
        self.assertIsNotNone(instance)
        # job + port

    def test_13_change_security_group(self):
        instance = self.client.change_instance_security_group(shared_data['instance']['id'],
                                                              security_group_id='default')
        self.assertIsNotNone(instance)
        # job + SECURITY GROUP
    def test_14_change_ip(self):
        attrs = {
            "node_id": "52a4c096bb1f455d8d866956a959519eno02",
            "new_ip": "192.168.0.133"
        }
        instance = self.client.change_instance_private_ip(shared_data['instance']['id'], **attrs)
        self.assertIsNotNone(instance)
        # job

    def test_15_create_ip(self):
        attrs = {
            "type": "shard",
            "password": "new_pass"
        }
        instance = self.client.create_instance_ip(shared_data['instance']['id'], **attrs)
        self.assertIsNotNone(instance)
        # ?

    def test_16_replica(self):
        instance = self.client.configure_client_network(shared_data['instance']['id'],
                                                        network_ranges=["192.168.0.0/16"])
        self.assertIsNotNone(instance)
        # ?

    def test_17_restart_instance(self):
        instance = self.client.restart_instance(shared_data['instance']['id'])
        self.assertIsNotNone(instance)

    def test_18_delete_instance(self):
        instance = None
        try:
            instance = self.client.delete_instance(instance=shared_data['instance'])
        except Exception:
            self.destroy_network(shared_data['network'])
        self.assertIsNotNone(instance)
