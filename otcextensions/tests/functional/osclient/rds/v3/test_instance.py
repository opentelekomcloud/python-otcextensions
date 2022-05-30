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
import time

import concurrent.futures

from openstackclient.tests.functional import base
from tempest.lib.exceptions import CommandFailed


class TestRdsInstance(base.TestCase):
    """Functional tests for RDS Instance. """

    UUID = uuid.uuid4().hex[:8]
    ROUTER_NAME = 'sdk-test-router-' + UUID
    NET_NAME = 'sdk-test-net-' + UUID
    SUBNET_NAME = 'sdk-test-subnet-' + UUID
    SG_NAME = 'sdk-test-sg-' + UUID
    ROUTER_ID = None
    NET_ID = None
    SG_ID = None

    RDS_NAME = 'sdk-test-rds-' + UUID
    RDS_HA_NAME = 'sdk-test-rds-ha-' + UUID
    RDS_RR_NAME = 'sdk-test-rds-rr-' + UUID
    INSTANCE_LIST = [RDS_NAME, RDS_HA_NAME]

    VOL_TYPE = 'ULTRAHIGH'
    VOL_SIZE = 100
    DATASTORE = 'MySQL'
    VERSION = None

    AZ = 'eu-de-01'
    HA_AZ = 'eu-de-01,eu-de-02'

    FLAVOR = None
    HA_FLAVOR = None
    RR_FLAVOR = None
    REGION = None

    BACKUP_NAME = 'sdk-test-rds-backup-' + UUID
    BACKUP_ID = None

    def test_01_instance_list(self):
        self.openstack(
            'rds instance list -f json '
        )

    def test_02_instance_list_filters(self):
        self.openstack(
            'rds instance list '
            '--limit 1 --id 2 '
            '--name 3 --type Single '
            '--datastore-type PostgreSQL '
            '--router-id 123asd '
            '--network-id 123qwe '
            '--offset 5'
        )

        self.assertTrue(True)

    def test_03_create_instance(self):
        self._initialize_network()
        TestRdsInstance.REGION = self._get_region()
        TestRdsInstance.VERSION = self._get_latest_version()
        TestRdsInstance.FLAVOR = self._get_default_flavor()
        TestRdsInstance.HA_FLAVOR = self._get_default_flavor('ha')
        TestRdsInstance.RR_FLAVOR = self._get_default_flavor('replica')
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self._create_instance, self.RDS_NAME)
            # Create HA Instance
            executor.submit(
                self._create_instance,
                self.RDS_HA_NAME,
                'semisync')
        for instance in self.INSTANCE_LIST:
            json_output = json.loads(self.openstack(
                'rds instance show -f json ' + instance
            ))
            self.assertEqual(json_output['name'], instance)

    def test_04_create_read_replica(self):
        instance_name = self.INSTANCE_LIST[0]
        json_output = json.loads(self.openstack(
            'rds instance create -f json '
            ' {name} {flavor} '
            ' --replica-of {instance} '
            ' --volume-type {vol_type}'
            ' --size {vol_size} '
            ' --region {region} '
            ' --availability-zone {az} '
            ' --wait --wait-interval 10'.format(
                name=self.RDS_RR_NAME,
                flavor=self.RR_FLAVOR,
                instance=instance_name,
                region=self.REGION,
                vol_type=self.VOL_TYPE,
                vol_size=self.VOL_SIZE,
                az=self.AZ)
        ))
        self.assertTrue(self._wait_for_instance(json_output['id']))
        self.assertIsNotNone(json_output)

    def test_05_backup_list(self):
        instance_name = self.INSTANCE_LIST[0]
        json_output = json.loads(self.openstack(
            'rds backup list -f json ' + instance_name
        ))
        self.assertIsNotNone(json_output)

    def test_06_create_manual_backup(self):
        instance_name = self.INSTANCE_LIST[1]
        json_output = json.loads(self.openstack(
            'rds backup create -f json '
            ' --description sdk-test-backup '
            '{name} {instance} --wait --wait-interval 10'.format(
                name=self.BACKUP_NAME,
                instance=instance_name
            )
        ))
        self.assertIsNotNone(json_output)
        TestRdsInstance.BACKUP_ID = json_output['id']

    def test_07_backup_download_links(self):
        instance_name = self.INSTANCE_LIST[1]
        json_output = json.loads(self.openstack(
            'rds backup list -f json ' + instance_name
        ))
        for backup in json_output:
            json_output = json.loads(self.openstack(
                'rds backup download links -f json ' + backup['ID']
            ))
            self.assertIsNotNone(json_output)

    # def test_08_create_instance_from_backup(self):
    #    json_output = json.loads(self.openstack(
    #        'rds instance show -f json ' + self.INSTANCE_LIST[1]))
    #    from_instance = json_output['id']

    #    restore_instance = self.RDS_NAME + '-restore'
    #    json_output = self._create_instance(
    #        instance_name=restore_instance,
    #        backup=self.BACKUP_ID,
    #        from_instance=from_instance)
    #    self.addCleanup(
    #        self.openstack,
    #        'rds instance delete ' + restore_instance)
    #    self.assertEqual(json_output['status'], 'ACTIVE')

    def test_09_backup_delete(self):
        self.openstack('rds backup delete ' + self.BACKUP_ID)
        self.assertRaises(
            CommandFailed,
            self.openstack,
            'rds backup delete ' + self.BACKUP_ID
        )

    def test_10_backup_policy_set(self):
        instance_name = self.INSTANCE_LIST[0]
        self.openstack(
            'rds instance backup policy set '
            '{instance} --keep-days {keep_days} '
            '--start-time {start_time} '
            '--period {period}'.format(
                instance=instance_name,
                keep_days=5,
                start_time="19:00-20:00",
                period="3,4"
            )
        )

        self.assertTrue(self._wait_for_instance(instance_name))
        json_output = json.loads(self.openstack(
            'rds instance backup policy show -f json ' + instance_name
        ))
        self.assertEqual(json_output['keep_days'], 5)

    def test_11_backup_policy_set_0(self):
        instance_name = self.INSTANCE_LIST[0]
        self.openstack(
            'rds instance backup policy set '
            '{instance} --keep-days {keep_days} '.format(
                instance=instance_name,
                keep_days=0,
            )
        )

        self.assertTrue(self._wait_for_instance(instance_name))
        json_output = json.loads(self.openstack(
            'rds instance backup policy show -f json ' + instance_name
        ))
        self.assertEqual(json_output['keep_days'], 0)

    def test_12_delete_instance(self):
        self.addCleanup(self._deinitialize_network)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self._delete_instance, self.RDS_NAME)
            executor.submit(self._delete_instance, self.RDS_HA_NAME)

        for instance in self.INSTANCE_LIST:
            self.assertRaises(
                CommandFailed,
                self.openstack,
                'rds instance show ' + instance
            )
        time.sleep(60)

    def _create_instance(
            self,
            instance_name,
            ha_mode=None,
            backup=None,
            from_instance=None):
        cli_str = ('rds instance create {name}'
                   ' --datastore-type {datastore}'
                   ' --datastore-version {version}'
                   ' --router-id {router_id}'
                   ' --network-id {net_id}'
                   ' --security-group-id {sg_id}'
                   ' --volume-type {vol_type}'
                   ' --size {vol_size}'
                   ' --password Test@123'
                   ' --region {region}'
                   ' --wait --wait-interval 10'
                   ' -f json '.format(
                       name=instance_name,
                       datastore=self.DATASTORE,
                       version=self.VERSION,
                       router_id=self.ROUTER_ID,
                       net_id=self.NET_ID,
                       sg_id=self.SG_ID,
                       vol_type=self.VOL_TYPE,
                       vol_size=self.VOL_SIZE,
                       region=self.REGION))
        if ha_mode:
            cli_str += (' {flavor}'
                        ' --availability-zone {az}'
                        ' --ha-mode {ha_mode}'.format(
                            flavor=self.HA_FLAVOR,
                            az=self.HA_AZ,
                            ha_mode=ha_mode))
        else:
            cli_str += self.FLAVOR + ' --availability-zone ' + self.AZ

        if backup or from_instance:
            cli_str += (' --from-instance {instance}'
                        ' --backup {backup}'.format(
                            instance=from_instance,
                            backup=backup))

        json_output = json.loads(self.openstack(cli_str))

        self._wait_for_instance(json_output['id'])

        return json_output

    def _get_region(self):
        json_output = json.loads(self.openstack(
            'region list -f json'))
        return json_output[0]['Region']

    def _get_latest_version(self):
        json_output = json.loads(self.openstack(
            'rds datastore version list -f json ' + self.DATASTORE))
        versions = [data['Name'] for data in json_output]
        return sorted(versions)[-1]

    def _get_default_flavor(self, flavor_type=None):
        if not self.VERSION:
            TestRdsInstance.VERSION = self._get_latest_datastore_version(
                self.DATASTORE)
        json_output = json.loads(self.openstack(
            'rds flavor list -f json {} {}'.format(
                self.DATASTORE, self.VERSION)
        ))
        if flavor_type:
            flavor_list = [[data['vcpus'], data['name']]
                           for data in json_output if
                           data['instance_mode'] == flavor_type.lower()]
        else:
            flavor_list = [[data['vcpus'], data['name']]
                           for data in json_output if
                           data['instance_mode'] == 'single']
        flavor_list = sorted(flavor_list, key=lambda x: int(x[0]))
        return flavor_list[0][1]

    def _delete_instance(self, instance_name):
        self.openstack(
            'rds instance delete --wait ' + instance_name
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
        sg = json.loads(self.openstack(
            'security group create -f json ' + self.SG_NAME
        ))

        self.openstack(
            'router add subnet {router} '
            '{subnet} '.format(
                router=self.ROUTER_NAME,
                subnet=self.SUBNET_NAME
            )
        )

        TestRdsInstance.ROUTER_ID = router['id']
        TestRdsInstance.NET_ID = net['id']
        TestRdsInstance.SG_ID = sg['id']

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
        self.openstack(
            'security group delete ' + self.SG_NAME
        )

    def _wait_for_instance(self, instance, timeout=1000, polling=10):
        """
        Wait For Instance Status to return to ACTIVE State
        """
        max_time = time.time() + float(timeout)
        time.sleep(polling)
        while max_time > time.time():
            json_output = json.loads(self.openstack(
                'rds instance show -f json ' + instance
            ))
            status = json_output['status'].lower()
            if status == 'active':
                return True
            else:
                time.sleep(polling)
        return False
