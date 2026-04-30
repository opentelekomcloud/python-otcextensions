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

from openstack import exceptions as sdk_exceptions
from openstack import resource


class PrivateNatEnvironmentMixin(object):
    def _delete_private_transit_ip(self, transit_ip_id):
        self.conn.natv3.delete_private_transit_ip(transit_ip_id, ignore_missing=True)

    def _create_private_nat_vpc(self, prefix, suffix):
        vpc_name = "{prefix}-vpc-{suffix}".format(prefix=prefix, suffix=suffix)
        return self.conn.vpc.create_vpc(name=vpc_name, cidr="192.168.0.0/16")

    def _delete_private_nat_vpc(self, vpc):
        try:
            vpc = self.conn.vpc.get_vpc(vpc.id)
        except sdk_exceptions.ResourceNotFound:
            return

        self.conn.vpc.delete_vpc(vpc, ignore_missing=True)
        resource.wait_for_delete(self.conn.vpc, vpc, 2, 120)

    def _create_private_nat_subnet(self, vpc, prefix, suffix):
        subnet_name = "{prefix}-subnet-{suffix}".format(prefix=prefix, suffix=suffix)
        gw, _ = vpc.cidr.split("/")
        subnet = self.conn.vpc.create_subnet(
            name=subnet_name,
            vpc_id=vpc.id,
            cidr=vpc.cidr,
            gateway_ip=gw[:-2] + ".1",
            dns_list=["100.125.4.25", "100.125.129.199"],
        )
        resource.wait_for_status(self.conn.vpc, subnet, "ACTIVE", None, 2, 60)
        return subnet

    def _delete_private_nat_subnet(self, subnet):
        try:
            subnet = self.conn.vpc.get_subnet(subnet.id)
        except sdk_exceptions.ResourceNotFound:
            return

        resource.wait_for_status(self.conn.vpc, subnet, "ACTIVE", None, 2, 60)
        self.conn.vpc.delete_subnet(subnet, ignore_missing=True)
        resource.wait_for_delete(self.conn.vpc, subnet, 2, 120)

    def _create_private_nat_network_stack(self, prefix):
        suffix = uuid.uuid4().hex[:8]
        vpc = self._create_private_nat_vpc(prefix, suffix)
        subnet = self._create_private_nat_subnet(vpc, prefix, suffix)

        return {
            "vpc": vpc,
            "subnet": subnet,
            "network_id": subnet.neutron_network_id,
        }

    def _cleanup_private_nat_network_stack(self, stack):
        subnet = stack.get("subnet")
        vpc = stack.get("vpc")

        if subnet:
            self._delete_private_nat_subnet(subnet)

        if vpc:
            self._delete_private_nat_vpc(vpc)

    def _prepare_private_nat_subnet_environment(self, prefix):
        suffix = uuid.uuid4().hex[:8]
        vpc = self._create_private_nat_vpc(prefix, suffix)
        self.addCleanup(self._delete_private_nat_vpc, vpc)

        subnet = self._create_private_nat_subnet(vpc, prefix, suffix)
        self.addCleanup(self._delete_private_nat_subnet, subnet)
        return {"vpc": vpc, "subnet": subnet}

    def _create_private_nat_gateway(self, subnet_id, prefix):
        gateway = self.conn.natv3.create_private_nat_gateway(
            name="{prefix}-gateway-{suffix}".format(
                prefix=prefix, suffix=uuid.uuid4().hex[:8]
            ),
            spec="Small",
            downlink_vpcs=[{"virsubnet_id": subnet_id}],
        )
        resource.wait_for_status(self.conn.natv3, gateway, "ACTIVE", None, 2, 120)
        return gateway

    def _delete_private_nat_gateway(self, gateway):
        try:
            gateway = self.conn.natv3.get_private_nat_gateway(gateway.id)
        except sdk_exceptions.ResourceNotFound:
            return

        self.conn.natv3.delete_private_nat_gateway(gateway, ignore_missing=True)
        resource.wait_for_delete(self.conn.natv3, gateway, 2, 120)

    def _prepare_private_nat_gateway_environment(self, prefix):
        stack = self._create_private_nat_network_stack(prefix)
        self.addCleanup(self._cleanup_private_nat_network_stack, stack)

        gateway = self._create_private_nat_gateway(stack["subnet"].id, prefix)
        self.addCleanup(self._delete_private_nat_gateway, gateway)
        return {"stack": stack, "gateway": gateway}
