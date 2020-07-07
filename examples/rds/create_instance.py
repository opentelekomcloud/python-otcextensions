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
Create a RDS instance
"""
import openstack


openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


attrs = {
    "name": "rds_name",
    "port": 3306,
    "ha": {
        "mode": "Ha",
        "replication_mode": "async"
    },
    "region": "eu-de",
    "datastore": {
        "type": "MySQL",
        "version": "8.0"
    },
    "volume": {
        "type": "ULTRAHIGH",
        "size": 40
    },
    "password": "admin_password",
    "private_ips": [],
    "public_ips": [],
    "db_user_name": "root",
    "availability_zone": "eu-de-01,eu-de-02",
    "vpc_id": "vpc_id",
    "subnet_id": "network_id_of_the_subnet",
    "security_group_id": "secgrp_id",
    "flavor_ref": "rds.mysql.c2.medium.ha",
    "switch_strategy": "reliability",
    "backup_strategy": {
        "start_time": "23:00-00:00",
        "keep_days": 10
    },
    "charge_info": {
        "charge_mode": "postPaid"
    }
}

instance = conn.rds.create_instance(**attrs)
print(instance)
