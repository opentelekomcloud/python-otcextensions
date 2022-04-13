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
Create CCE Cluster
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    "kind": "Cluster",
    "apiVersion": "v3",
    "metadata": {
        "name": "turbo-cluster",
    },
    "spec": {
        "type": "VirtualMachine",
        "flavor": "cce.s1.small",
        "version": "v1.19.10-r0",
        "az": "eu-de-01",
        "hostNetwork": {
            "vpc": "05c33818-78df-4329-b546-5df2f1aa823e",
            "subnet": "9f0c8ef2-c608-4238-88be-87bce5fe90da",
        },
        "containerNetwork": {
            "mode": "eni",
        },
        "eniNetwork": {
            "eniSubnetId": "417dcc1f-95d7-43e7-8533-ab078d266303",
            "eniSubnetCIDR": "10.0.0.0/14",
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

conn.cce.create_cluster(**attrs)
