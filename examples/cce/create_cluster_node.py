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
"""
Create CCE Cluster node
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    "kind": "Cluster",
    "apiVersion": "v3",
    "metadata": {
        "name": "test2"
    },
    "spec": {
        "type": "VirtualMachine",
        "flavor": "cce.s1.small",
        "version": "v1.13.10-r0",
        "az": "eu-de-01",
        "supportIstio": True,
        "hostNetwork": {
            "vpc": "26ca2783-dc40-4e3a-95b1-5a0756441e12",
            "subnet": "25d24fc8-d019-4a34-9fff-0a09fde6a9cb",
            "SecurityGroup": "f9ae0767-25be-44fc-a21c-5b8a0da66dec"
        },
        "containerNetwork": {
            "mode": "overlay_l2",
            "cidr": "172.16.0.0/16"
        },
        "authentication": {
            "mode": "rbac",
            "authenticatingProxy": {}
        },
        "billingMode": 0,
        "kubernetesSvcIpRange": "10.247.0.0/16",
        "kubeProxyMode": "iptables"
    }
}

conn.cce.create_cluster_node(**attrs)
