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

shared_data = {}


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
        print('Creating instance')
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
        self.instance = (
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
            )
        )
        shared_data['id'] = self.instance['id']
        print('Job for creation set')
        print('Waiting for job to finish')
        self.client.wait_job(self.instance['job_id'])
        print('Instance created')
        self.assertIsNotNone(self.instance)

    def test_02_list_instances(self):
        instances = list(self.client.instances())
        self.assertIsNotNone(instances)

    def test_03_get_instance(self):
        instance = self.client.get_instance(shared_data['id'])
        self.assertIsNotNone(instance)

    def test_04_find_instance(self):
        instance = self.client.find_instance(name_or_id=shared_data['id'])
        self.assertIsNotNone(instance)

    def test_05_bind_eip(self):
        instance = self.client.wait_normal_instance(shared_data['id'])
        group_id = [item for item in instance['groups']
                    if item['type'] == 'mongos'][0]['nodes'][0]['id']
        ip = [item for item in list(self.conn.network.ips())
              if item['status'] == 'DOWN'][0]
        eip = self.client.bind_eip(group_id,
                                   ip['floating_ip_address'],
                                   ip['id'])
        shared_data['eip'] = eip
        self.client.wait_job(eip['job_id'])
        self.assertIsNotNone(eip['job_id'])

    def test_06_unbind_eip(self):
        eip = self.client.unbind_eip(shared_data['eip']['node_id'])
        self.client.wait_job(eip['job_id'])
        self.assertIsNotNone(eip['job_id'])

    def test_07_enlarge_instance(self):
        print('Enlarging instance')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        group_id = [item for item in instance['groups']
                    if item['type'] == 'shard'][0]['id']
        result = self.client.enlarge_instance(shared_data['id'],
                                              size=60,
                                              group_id=group_id)
        print('Enlarging instance, job created')
        self.assertIsNotNone(result['job_id'])
        self.client.wait_job(result['job_id'])
        print('Enlarging instance finished')

    def test_06_adding_nodes(self):
        print('Adding nodes')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        attrs = {
            "node_type": "mongos",
            "spec_code": "dds.mongodb.s2.medium.4.mongos",
            "num": 1
        }
        result = self.client.add_instance_nodes(shared_data['id'], **attrs)
        print('Adding nodes, job created')
        self.assertIsNotNone(result['job_id'])
        self.client.wait_job(result['job_id'])
        print('Adding nodes finished')

    def test_07_modify_instance_specs(self):
        print('Modify instance specs')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        group_id = [item for item in instance['groups']
                    if item['type'] == 'mongos'][0]['nodes'][0]['id']
        attrs = {
            "spec_code": "dds.mongodb.s2.xlarge.4.mongos",
            "target_type": "mongos",
            "target_id": group_id
        }
        result = self.client.resize_instance(shared_data['id'], **attrs)
        print('Modify instance specs, job created')
        self.assertIsNotNone(result['job_id'])
        self.client.wait_job(result['job_id'])
        print('Modify instance specs finished')

    # def test_08_switchover(self):
    #     self.wait_job_to_finish()
    #     instance = self.client.switchover_instance(shared_data['id'])
    #     self.assertIsNot(shared_data['instance']['job_id'],
    #                      instance['job_id'])
    #     shared_data['instance']['job_id'] = instance['job_id']

    def test_09_enable_ssl(self):
        print('Enabling SSL')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        result = self.client.enable_instance_ssl(shared_data['id'])
        print('Enabling SSL, job created')
        self.assertIsNotNone(result['job_id'])
        self.client.wait_job(result['job_id'])
        print('Enabling SSL finished')

    def test_10_change_name(self):
        print('Changing name')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        new_name = 'new_name'
        self.client.change_instance_name(shared_data['id'], name=new_name)
        instance = self.client.get_instance(shared_data['id'])
        self.assertEqual(new_name, instance['name'])
        print('Changing name finished')

    def test_11_change_port(self):
        print('Changing port')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        result = self.client.change_instance_port(shared_data['id'], port=8888)
        print('Changing port, job created')
        self.assertIsNotNone(result['job_id'])
        self.client.wait_job(result['job_id'])
        print('Changing port finished')

    def test_12_change_security_group(self):
        print('Changing security group')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        security_group = self.net_client.find_security_group(
            name_or_id='default', ignore_missing=False)
        sec_id = security_group['id']
        instance = (self.client.
                    change_instance_security_group(shared_data['id'],
                                                   security_group_id=sec_id))
        print('Changing security group, job created')
        print(instance['job_id'])
        self.assertIsNotNone(instance['job_id'])
        self.client.wait_job(instance['job_id'])
        print('Changing security group finished')

    def test_13_change_ip(self):
        print('Changing ip')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        group_id = [item for item in instance['groups']
                    if item['type'] == 'mongos'][0]['nodes'][0]['id']
        attrs = {
            "node_id": group_id,
            "new_ip": "192.168.0.133"
        }
        instance = self.client.change_instance_private_ip(shared_data['id'],
                                                          **attrs)
        print('Changing ip, job created')
        self.assertIsNotNone(instance['job_id'])
        self.client.wait_job(instance['job_id'])
        print('Changing ip finished')

    def test_14_create_ip(self):
        print('Creating ip')
        attrs = {
            "dds_type": "shard",
            "password": "New_pass23@"
        }
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        instance = self.client.create_instance_ip(shared_data['id'], **attrs)
        print('Creating ip, job created')
        self.assertIsNotNone(instance)
        self.client.wait_job(instance['job_id'])
        print('Creating ip finished')

    def test_15_replica(self):
        self.client.wait_normal_instance(shared_data['instance']['id'])
        instance = (self.client.
                    configure_client_network(shared_data['id'],
                                             network_ranges=["192.168.0.0/16"])
                    )
        self.assertIsNotNone(instance['job_id'])
        self.client.wait_job(instance['job_id'])

    def test_16_restart_instance(self):
        print('Restarting instance')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        instance = self.client.restart_instance(shared_data['id'])
        print('Restarting instance, job created')
        self.assertIsNotNone(instance['job_id'])
        self.client.wait_job(instance['job_id'])
        print('Restarting instance finished')

    def test_17_delete_instance(self):
        print('Deleting instance')
        print('Check for the state')
        instance = self.client.wait_normal_instance(shared_data['id'])
        print(instance['status'])
        instance = None
        try:
            instance = self.client.delete_instance(instance=shared_data['id'])
        except Exception:
            self.destroy_network(shared_data['network'])
        self.assertIsNotNone(instance)
