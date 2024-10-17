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
 Create instance
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

datastore = {
    'type': 'DDS-Community',
    'version': '3.4',
    'storage_engine': 'wiredTiger'
}
region = 'eu-de'
availability_zone = 'eu-de-01'
vpc_id = 'vpc-1'
subnet_id = 'subnet-1'
security_group_id = 'sg-1'
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
instance = conn.dds.create_instance(
                name='test-dds',
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
print(instance)