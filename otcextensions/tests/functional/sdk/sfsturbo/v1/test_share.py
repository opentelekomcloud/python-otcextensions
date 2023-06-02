import openstack
import uuid

from openstack import resource
from otcextensions.tests.functional import base

_logger = openstack._log.setup_logging('openstack')


class TestShare(base.BaseFunctionalTest):

    share = None
    uuid_v4 = uuid.uuid4().hex[:8]
    network_info = None

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
                'vpc_id': vpc.id,
                'subnet_id': subnet.id,
                'secgroup_id': sec_group.id,
                'secgroup_id_2': sec_group_2.id,
            }

    def _destroy_network(self):
        if TestShare.network_info:
            secgroup_id = TestShare.network_info['secgroup_id']
            secgroup_id_2 = TestShare.network_info['secgroup_id_2']
            subnet_id = TestShare.network_info['subnet_id']
            vpc_id = TestShare.network_info['vpc_id']

            sot = self.conn.network.delete_security_group(
                secgroup_id,
                ignore_missing=False
            )
            self.assertIsNone(sot)

            sot = self.conn.network.delete_security_group(
                secgroup_id_2,
                ignore_missing=False
            )
            self.assertIsNone(sot)

            sot = self.conn.vpc.delete_subnet(
                subnet_id,
                ignore_missing=False
            )
            self.assertIsNone(sot)
            sot = self.conn.network.delete_network(
                vpc_id,
                ignore_missing=False
            )

            TestShare.network_info = None
            self.assertIsNone(sot)

    def _create_share(self):
        share_name = 'sfsturbo-test-share-' + self.uuid_v4
        TestShare.share = self.conn.sfsturbo.create_share(
            name=share_name,
            vpc_id=TestShare.network_info['vpc_id'],
            subnet_id=TestShare.network_info['subnet_id'],
            security_group_id=TestShare.network_info['secgroup_id'],
            share_proto="NFS",
            share_type="STANDARD",
            size=100,
            availability_zone="eu-de-01"
            )
        self.conn.sfsturbo.wait_for_share(TestShare.share)
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
        self.conn.sfsturbo.wait_for_extend_capacity(share, new_capacity='200')
        share = self.conn.sfsturbo.get_share(share=share.id)
        self.assertEqual(share.avail_capacity, 200)

    def test_04_change_security_group(self):
        share = self.conn.sfsturbo.change_security_group(
            TestShare.share.id,
            security_group_id=TestShare.network_info['secgroup_id_2'])
        share = self.conn.sfsturbo.get_share(share=share.id)
        self.assertEqual(share.security_group_id,
                         TestShare.network_info['secgroup_id_2'])

    def test_05_delete_share(self):
        try:
            self.conn.sfsturbo.delete_share(share=TestShare.share)
        except openstack.exceptions.InvalidRequest:
            self._destroy_network()
            raise
        self._destroy_network()
        try:
            share = self.conn.sfsturbo.get_share(TestShare.share.id)
        except openstack.exceptions.ResourceNotFound:
            share = None
        self.assertIsNone(share)
