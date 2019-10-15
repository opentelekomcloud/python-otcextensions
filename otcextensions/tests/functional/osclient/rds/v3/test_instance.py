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

from openstackclient.tests.functional import base
from tempest.lib.exceptions import CommandFailed

class TestRdsInstance(base.TestCase):
    """Functional tests for RDS Instance. """

    NAME = uuid.uuid4().hex
    OTHER_NAME = uuid.uuid4().hex
    ROUTER_NAME = 'sdk-test-router-' + NAME
    NET_NAME = 'sdk-test-net-' + NAME
    SUBNET_NAME = 'sdk-test-subnet-' + NAME
    SG_NAME = 'sdk-test-sg-' + NAME
    ROUTER_ID = None
    NET_ID = None
    SG_ID = None

    RDS_NAME = 'sdk-test-rds-' + NAME
    DATASTORE = 'MySQL'
    VERSION = '5.7'
    REGION = 'eu-de'
    AZ = 'eu-de-01'
    FLAVOR = 'rds.mysql.c2.medium'
    VOL_TYPE = 'ULTRAHIGH'
    VOL_SIZE = 100


    def test_instance_list(self):
        self.openstack(
            'rds instance list -f json '
        )

    def test_instance_list_filters(self):
        self.openstack(
            'rds instance list '
            '--limit 1 --id 2 '
            '--name 3 --type Single '
            '--datastore-type PostgreSQL '
            '--router-id 123asd --subnet-id 123qwe '
            '--offset 5'
        )

        self.assertTrue(True)

    def test_create_instance(self):
        self._initialize_network()
        self.addCleanup(self._denitialize_network)
        json_output = json.loads(self.openstack(
            'rds instance create {name} {flavor}'
            ' --datastore-type {datastore}'
            ' --datastore-version {version}'
            ' --router-id {router_id}'
            ' --subnet-id {subnet_id}'
            ' --security-group-id {sg_id}'
            ' --volume-type {vol_type}'
            ' --size {vol_size}'
            ' --password Test@123'
            ' --availability-zone {az}'
            ' --region {region}'
            ' --wait --wait-interval 10'
            ' -f json '.format(
                name=self.RDS_NAME,
                flavor=self.FLAVOR,
                datastore=self.DATASTORE,
                version=self.VERSION,
                router_id=self.ROUTER_ID,
                subnet_id=self.NET_ID,
                sg_id=self.SG_ID,
                vol_type=self.VOL_TYPE,
                vol_size=self.VOL_SIZE,
                az=self.AZ,
                region=self.REGION)
        ))
        self.addCleanup(
            self.openstack,
            'rds instance delete ' + self.RDS_NAME
        )  
        
        self.assertIsNotNone(json_output)

        json_output = json.loads(self.openstack(
            'rds instance show -f json ' + self.RDS_NAME
        ))
        self.assertIsNotNone(json_output)

        json_output = json.loads(self.openstack(
            'rds backup list -f json ' + self.RDS_NAME
        ))
        self.assertIsNotNone(json_output)

        json_output = json.loads(self.openstack(
            'rds instance backup policy show -f json ' + self.RDS_NAME
        ))
        self.assertIsNotNone(json_output)

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

        self.ROUTER_ID = router['id']
        self.NET_ID = net['id']
        self.SG_ID = sg['id']

    def _denitialize_network(self):
        try:
            self.openstack(
                'rds instance delete ' + self.RDS_NAME
            )
        except CommandFailed:
            pass
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
