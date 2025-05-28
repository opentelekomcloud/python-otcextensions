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
from openstack.tests.unit import base
from otcextensions.sdk.apig.v2 import vpc_channel

EXAMPLE_MEMBER_GROUP = {
    'member_group_name': 'group1',
    'member_group_remark': 'test',
    'member_group_weight': 10,
    'dict_code': 'code',
    'microservice_version': '1.0',
    'microservice_port': 8080,
    'microservice_labels': [{'label_name': 'env', 'label_value': 'prod'}],
    'member_group_id': 'mg-123',
    'create_time': '2025-01-01T12:00:00Z',
    'update_time': '2025-01-02T12:00:00Z'
}

EXAMPLE_MEMBER = {
    'host': '192.168.0.1',
    'weight': 20,
    'is_backup': True,
    'member_group_name': 'group1',
    'status': 1,
    'port': 80,
    'ecs_id': 'ecs-123',
    'ecs_name': 'ecs-node'
}

EXAMPLE_HEALTH_CONFIG = {
    'protocol': 'HTTP',
    'path': '/health',
    'method': 'GET',
    'port': 8080,
    'threshold_normal': 3,
    'threshold_abnormal': 2,
    'time_interval': 5,
    'http_code': '200',
    'enable_client_ssl': False,
    'status': 1,
    'timeout': 2,
    'vpc_channel_id': 'vpc-123',
    'id': 'hc-123',
    'create_time': '2025-01-01T12:00:00Z'
}

EXAMPLE_MICROSERVICE = {
    'service_type': 'CSE',
    'cse_info': {
        'engine_id': 'e1',
        'service_id': 's1',
        'engine_name': 'engine',
        'service_name': 'service',
        'register_address': '127.0.0.1',
        'cse_app_id': 'app',
        'version': '1.0'
    },
    'cce_info': {
        'cluster_id': 'c1',
        'namespace': 'ns',
        'workload_type': 'deployment',
        'app_name': 'app',
        'label_key': 'env',
        'label_value': 'prod',
        'cluster_name': 'cname'
    },
    'id': 'ms-1',
    'instance_id': 'i-1',
    'create_time': '2025-01-01T12:00:00Z',
    'update_time': '2025-01-02T12:00:00Z'
}

EXAMPLE_VPC_CHANNEL = {
    'gateway_id': 'gw-1',
    'id': 'vpc-123',
    'name': 'test-channel',
    'port': 443,
    'balance_strategy': 1,
    'member_type': 'IP',
    'type': 1,
    'dict_code': 'code',
    'member_groups': [EXAMPLE_MEMBER_GROUP],
    'members': [EXAMPLE_MEMBER],
    'vpc_health_config': EXAMPLE_HEALTH_CONFIG,
    'microservice_info': EXAMPLE_MICROSERVICE,
    'create_time': '2025-01-01T12:00:00Z',
    'status': 1
}


class TestVpcChannel(base.TestCase):

    def test_basic(self):
        sot = vpc_channel.VpcChannel()
        self.assertEqual('apigw/instances/%(gateway_id)s/vpc-channels',
                         sot.base_path)
        self.assertEqual('vpc_channels', sot.resources_key)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = vpc_channel.VpcChannel(**EXAMPLE_VPC_CHANNEL)
        self.assertEqual(EXAMPLE_VPC_CHANNEL['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_VPC_CHANNEL['id'], sot.id)
        self.assertEqual(EXAMPLE_VPC_CHANNEL['name'], sot.name)
        self.assertEqual(EXAMPLE_VPC_CHANNEL['port'], sot.port)
        self.assertEqual(EXAMPLE_VPC_CHANNEL['status'], sot.status)
        self.assertEqual(EXAMPLE_VPC_CHANNEL['balance_strategy'],
                         sot.balance_strategy)
        self.assertEqual(EXAMPLE_VPC_CHANNEL['member_type'], sot.member_type)
        self.assertEqual(EXAMPLE_VPC_CHANNEL['type'], sot.type)
        self.assertEqual(EXAMPLE_VPC_CHANNEL['dict_code'], sot.dict_code)

        self.assertEqual(1, len(sot.member_groups))
        self.assertEqual('group1', sot.member_groups[0].member_group_name)
        self.assertEqual(1, len(sot.members))
        self.assertEqual('192.168.0.1', sot.members[0].host)
        self.assertEqual('HTTP', sot.vpc_health_config.protocol)
        self.assertEqual('CSE', sot.microservice_info.service_type)
        self.assertEqual('e1', sot.microservice_info.cse_info.engine_id)
        self.assertEqual('c1', sot.microservice_info.cce_info.cluster_id)
