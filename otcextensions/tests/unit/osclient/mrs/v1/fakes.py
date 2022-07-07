#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
# import datetime
import random
import uuid

import mock
from openstackclient.tests.unit import utils

from otcextensions.sdk.mrs.v1 import cluster
from otcextensions.sdk.mrs.v1 import datasource
from otcextensions.sdk.mrs.v1 import job
from otcextensions.sdk.mrs.v1 import jobbinary
from otcextensions.tests.unit.osclient import test_base


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, "") for attr in columns)


class TestMrs(utils.TestCommand):

    def setUp(self):
        super(TestMrs, self).setUp()

        self.app.client_manager.mrs = mock.Mock()
        self.client = self.app.client_manager.mrs


class FakeHost(test_base.Fake):
    """Fake one or more Host"""

    @classmethod
    def generate(cls):
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": uuid.uuid4().hex,
            "ip": "192.168.0.169",
            "status": "ACTIVE",
            "flavor": "c2.2xlarge.linux.mrs",
            "type": random.choice(["Core", "Master"]),
            "mem": random.randint(1, 10000),
            "cpu": random.randint(1, 10),
            "root_volume_size": random.randint(1, 300),
            "data_volume_type": random.choice(["SATA", "SAS", "SSD"]),
            "data_volume_size": random.randint(1, 1000),
            "data_volume_count": random.randint(1, 5)
        }
        obj = cluster.Host.existing(**object_info)
        return obj


class FakeCluster(test_base.Fake):
    """Fake one or more Cluster"""

    @classmethod
    def generate(cls):
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": uuid.uuid4().hex,
            "master_num": random.randint(1, 5),
            "core_num": random.randint(1, 5),
            "status": random.choice(["starting", "running", "terminated",
                                     "failed", "abnormal", "terminating",
                                     "frozen", "scaling-out", "scaling-in"]
                                    ),
            "created_at": 1487570757,
            "updated_at": 1487668974,
            "billing_type": "Metered",
            "region": "eu-de",
            "vpc": "vpc-autotest",
            "fee": "0",
            "hadoop_version": "",
            "component_list": [{
                "id": None,
                "componentId": "MRS 3.0.2_001",
                "componentName": "Hadoop",
                "componentVersion": "3.1.1",
                "external_datasources": None,
                "componentDesc": "A distributed data processing framework",
                "componentDescEn": None,
            }],
            "master_node_size": "s1.8xlarge.linux.mrs",
            "core_node_size": "s2.2xlarge.linux.mrs",
            "external_ip": "100.120.0.2",
            "external_alternate_ip": "192.120.0.2",
            "internal_ip": "192.120.0.3",
            "deployment_id": "dep_id-" + uuid.uuid4().hex,
            "remark": "",
            "order_id": "null",
            "az_id": "null",
            "az": random.choice(["eu-de-01", "eu-de-02", "eu-de-03"]),
            "master_node_product_id": "m_id-" + uuid.uuid4().hex,
            "master_node_spec_id": "mspec_id-" + uuid.uuid4().hex,
            "core_node_product_id": "c_id-" + uuid.uuid4().hex,
            "core_node_spec_id": "cspec_id-" + uuid.uuid4().hex,
            "instanceId": "inst_id-" + uuid.uuid4().hex,
            "vnc": None,
            "project_id": "proj_id-" + uuid.uuid4().hex,
            "volume_size": random.randint(1, 1000),
            "volume_type": random.choice(["SATA", "SAS", "SSD"]),
            "subnet_id": "sub_id-" + uuid.uuid4().hex,
            "subnet_name": "subnet-ftest",
            "security_group_id": "sec_gr_id-" + uuid.uuid4().hex,
            "non_master_security_group_id": "sec_gr_id_1-" + uuid.uuid4().hex,
            "stage_desc": "Installing MRS Manager",
            "mrs_install_state": False,
            "safe_mode": 1,
            "cluster_version": "MRS 3.0.2",
            "bootstrapScripts": [
                {
                    "name": "test1-success",
                    "uri": "s3a://bootscript/script/simple/basic_success.sh",
                    "parameters": "",
                    "nodes": ["master", "core"],
                    "active_master": True,
                    "fail_action": "errorout",
                    "before_component_start": True,
                    "state": "SUCCESS",
                    "start_time": 1527681083
                }
            ],
            "node_groups": [
                {
                    "groupName": "master_node_default_group",
                    "nodeNum": 1,
                    "nodeSize": "s1.xlarge.linux.mrs",
                    "nodeSpecId": "cdc6035a249a40249312f5ef72a23cd7",
                    "vmProductId": "",
                    "vmSpecCode": None,
                    "nodeProductId": "dc970349d128460e960a0c2b826c427c",
                    "rootVolumeSize": 40,
                    "rootVolumeProductId": "16c1dcf0897249758b1ec276d06e0572",
                    "rootVolumeType": "SATA",
                    "rootVolumeResourceSpecCode": "",
                    "rootVolumeResourceType": "",
                    "dataVolumeType": "SATA",
                    "dataVolumeCount": 1,
                    "dataVolumeSize": 100,
                    "dataVolumeProductId": "16c1dcf0897249758b1ec276d06e0572",
                    "dataVolumeResourceSpecCode": "",
                    "dataVolumeResourceType": ""
                }
            ],
            "task_node_groups": [
                {
                    "groupName": "task_node_default_group",
                    "nodeNum": 1,
                    "nodeSize": "s1.xlarge.linux.mrs",
                    "nodeSpecId": "cdc6035a249a40249312f5ef72a23cd7",
                    "vmProductId": "",
                    "vmSpecCode": None,
                    "nodeProductId": "dc970349d128460e960a0c2b826c427c",
                    "rootVolumeSize": 40,
                    "rootVolumeProductId": "16c1dcf0897249758b1ec276d06e0572",
                    "rootVolumeType": "SATA",
                    "rootVolumeResourceSpecCode": "",
                    "rootVolumeResourceType": "",
                    "dataVolumeType": "SATA",
                    "dataVolumeCount": 1,
                    "dataVolumeSize": 100,
                    "dataVolumeProductId": "16c1dcf0897249758b1ec276d06e0572",
                    "dataVolumeResourceSpecCode": "",
                    "dataVolumeResourceType": "",
                    "AutoScalingPolicy": None
                }
            ],
            "cluster_type": 0,
            "tags": "k1=v1,k2=v2,k3=v3",
            "key": "myp",
            "master_ip": "192.168.1.1",
            "preffered_private_ip": "192.168.1.2",
            "error_info": None,
            "log_collection": 1,
            "master_data_volume_type": random.choice(["SATA", "SAS", "SSD"]),
            "master_data_volume_size": random.randint(1, 1000),
            "master_data_volume_count": random.randint(1, 10),
            "core_data_volume_type": random.choice(["SATA", "SAS", "SSD"]),
            "core_data_volume_size": random.randint(1, 1000),
            "core_data_volume_count": random.randint(1, 10),
        }

        obj = cluster.ClusterInfo.existing(**object_info)
        return obj


class FakeDatasource(test_base.Fake):
    """Fake one or more Datasource"""

    @classmethod
    def generate(cls):
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": uuid.uuid4().hex,
            "type": random.choice(["hdfs", "obs"]),
            "url": "/simple/mapreduce/input",
            "description": "this is the data source template",
            "is_public": random.choice([False, True]),
            "is_protected": random.choice([False, True]),
        }
        obj = datasource.Datasource.existing(**object_info)
        return obj


class FakeJob(test_base.Fake):
    """Fake one or more Job"""

    @classmethod
    def generate(cls):
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": uuid.uuid4().hex,
            "type": random.choice(["MapReduce", "SparkScript",
                                   "Hive", "DistCp"]),
            "description": "This is the Map Reduce job template",
            "created_at": "2017-06-22T09:39:13",
            "updated_at": "2017-06-22T09:39:13",
            "project_id": "pr-" + uuid.uuid4().hex,
            "is_public": False,
            "is_protected": False,
            "interface": [],
            "mains": [],
            "libs": [],
        }
        obj = job.Job.existing(**object_info)
        return obj


class FakeJobbinary(test_base.Fake):
    """Fake one or more Jobbinary"""

    @classmethod
    def generate(cls):
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": uuid.uuid4().hex,
            "description": "this is the job binary template",
            "is_public": random.choice([False, True]),
            "is_protected": random.choice([False, True]),
            "url": "/simple/mapreduce/program",
            "created_at": "2017-06-22T09:39:13",
            "updated_at": "2017-06-22T09:39:13",
        }
        obj = jobbinary.Jobbinary.existing(**object_info)
        return obj
