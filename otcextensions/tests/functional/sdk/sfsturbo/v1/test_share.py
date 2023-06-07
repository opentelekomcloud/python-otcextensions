#!/usr/bin/env python3
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
import openstack
import uuid
import time
import fixtures

from openstack import resource
from otcextensions.tests.functional import base

_logger = openstack._log.setup_logging('openstack')


class TestShare(base.BaseFunctionalTest):

    TIMEOUT = int(os.environ.get('OS_TEST_TIMEOUT'))
    share = None
    uuid_v4 = uuid.uuid4().hex[:8]
    network_info = None

    def setUp(self):
        test_timeout = 15 * TestShare.TIMEOUT
        try:
            self.useFixture(
                fixtures.EnvironmentVariable(
                    'OS_TEST_TIMEOUT', str(test_timeout)))
        except ValueError:
            pass
        super(TestShare, self).setUp()

    def _create_network(self):
        cidr = '192.168.0.0/16'
        gateway = '192.168.0.1'
        uuid_v4 = uuid.uuid4().hex[:8]
        vpc_name = 'sfsturbo-test-vpc-' + uuid_v4
        subnet_name = 'sfsturbo-test-subnet-' + uuid_v4
        secgroup_name = 'sfsturbo-test-secgroup' + uuid_v4
        secgroup_name_2 = 'sfsturbo-test-secgroup2' + uuid_v4

        if not TestShare.network_info:
            attrs = {
                'name': vpc_name,
                'cidr': cidr
            }
            vpc = self.conn.vpc.create_vpc(**attrs)
            self.assertEqual(vpc_name, vpc.name)
            attrs = {
                'vpc_id': vpc.id,
                'name': subnet_name,
                'cidr': cidr,
                'gateway_ip': gateway,
                'dns_list': [
                    "100.125.4.25",
                    "100.125.129.199",
                ],
            }
            subnet = self.conn.vpc.create_subnet(**attrs)
            resource.wait_for_status(self.conn.vpc, subnet, "ACTIVE", None, 2,
                                     20)

            self.assertEqual(subnet_name, subnet.name)

            sec_group = self.conn.network.create_security_group(
                name=secgroup_name)
            sec_group_2 = self.conn.network.create_security_group(
                name=secgroup_name_2)

            TestShare.network_info = {
                'vpc': vpc,
                'subnet': subnet,
                'secgroup': sec_group,
                'secgroup_2': sec_group_2,
            }

    def _destroy_network(self):
        if TestShare.network_info:
            secgroup = TestShare.network_info['secgroup']
            secgroup_2 = TestShare.network_info['secgroup_2']
            subnet = TestShare.network_info['subnet']
            vpc = TestShare.network_info['vpc']

            time.sleep(100)
            self.conn.vpc.delete_subnet(
                subnet,
                ignore_missing=False
            )
            resource.wait_for_delete(self.conn.vpc, subnet, 2, 120)
            self.conn.vpc.delete_vpc(
                vpc,
                ignore_missing=False
            )

            TestShare.network_info = None

            sot = self.conn.network.delete_security_group(
                secgroup.id,
                ignore_missing=False
            )
            self.assertIsNone(sot)

            sot = self.conn.network.delete_security_group(
                secgroup_2.id,
                ignore_missing=False
            )
            self.assertIsNone(sot)

    def _create_share(self):
        share_name = 'sfsturbo-test-share-' + self.uuid_v4
        TestShare.share = self.conn.sfsturbo.create_share(
            name=share_name,
            vpc_id=TestShare.network_info['vpc'].id,
            subnet_id=TestShare.network_info['subnet'].id,
            security_group_id=TestShare.network_info['secgroup'].id,
            share_proto="NFS",
            share_type="STANDARD",
            size=100,
            availability_zone="eu-de-01"
        )
        self.conn.sfsturbo.wait_for_share(TestShare.share, wait=600)
        self.assertIsNotNone(TestShare.share)

    def test_01_shares(self):
        self._create_network()
        self._create_share()
        shares = list(self.conn.sfsturbo.shares())
        self.assertGreaterEqual(len(shares), 0)

    def test_02_get_share(self):
        share = self.conn.sfsturbo.get_share(TestShare.share.id)
        self.assertEqual(share.id, TestShare.share.id)

    def test_03_extend_capacity(self):
        share = self.conn.sfsturbo.extend_capacity(TestShare.share.id,
                                                   new_size=200)
        self.conn.sfsturbo.wait_for_extend_capacity(share, wait=400)
        share = self.conn.sfsturbo.get_share(share=share.id)
        self.assertEqual(share.avail_capacity, '200.00')

    def test_04_change_security_group(self):
        share = self.conn.sfsturbo.change_security_group(
            TestShare.share.id,
            security_group_id=TestShare.network_info['secgroup_2'].id)
        self.conn.sfsturbo.wait_for_change_security_group(share)
        share = self.conn.sfsturbo.get_share(share=share.id)
        self.assertEqual(share.security_group_id,
                         TestShare.network_info['secgroup_2'].id)

    def test_05_delete_share(self):
        try:
            self.conn.sfsturbo.delete_share(share=TestShare.share)
            self.conn.sfsturbo.wait_for_delete_share(share=TestShare.share)
        except openstack.exceptions.ResourceNotFound:
            self._destroy_network()
            raise
        self._destroy_network()
        try:
            share = self.conn.sfsturbo.get_share(TestShare.share.id)
        except openstack.exceptions.ResourceNotFound:
            share = None
        self.assertIsNone(share)
