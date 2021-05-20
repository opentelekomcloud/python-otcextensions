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
import random
import uuid

import mock

from otcextensions.sdk.cbr.v3 import policy

def _generate_vals():
    my_list = []
    for item in random.randint(1,10):
        my_list.append(uuid.uuid4().hex)
    return my_list

class TestCBR(test_base.TestCommand):

    def setUp(self):
        super(TestCBR, self).setUp()

        self.app.client_manager.cbr = mock.Mock()
        self.app.client_manager.sdk_connection = mock.Mock()
        self.client = self.app.client_manager.cbr
        self.sdk_client = self.app.client_manager.sdk_connection


class FakePolicy(test_base.Fake):
    """Fake one or more CBR policies"""

    for item in random.randint(1, 10):


    @classmethod
    def generate(cls):
        object_info = {
            "name": 'name-' + uuid.uuid4().hex,
            "associated_vaults": [],
            "enabled": true,
            "trigger": {
                "properties": {
                    "pattern": [
                        "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=03;BYMINUTE=00"
                    ],
                    "start_time": "2021-05-18 11:38:55"
                },
                "type": "time",
                "id": "1a7dba0b-92a9-4ee0-ba2e-589281144346",
                "name": "default"
            },
            "operation_definition": {
                "max_backups": -1,
                "retention_duration_days": 30,
                "year_backups": 0,
                "day_backups": 0,
                "month_backups": 0,
                "week_backups": 0,
                "timezone": "UTC+02:00"
            },
            "operation_type": "backup",
            "id": "35133b4e-d47a-4478-a904-a17b52dc346b"
        }

        object_info = {
            'kind': 'NodePool',
            'apiVersion': 'v3',
            'metadata': {
                'name': 'name-' + uuid.uuid4().hex
            },
            'spec': {
                'initialNodeCount': 0,
                'type': 'vm',
                'autoscaling': {
                    'enable': random.choice([True, False]),
                    'minNodeCount': 0,
                    'maxNodeCount': random.randint(0, 100),
                    'scaleDownCooldownTime': random.randint(1, 10),
                    'priority': random.randint(1, 99)
                },
                'nodeManagement': {
                    'serverGroupReference': 'sg-' + uuid.uuid4().hex
                },
                'nodeTemplate': {
                    'flavor': 's2.large.2 ',
                    'az': random.choice([
                        'random',
                        'eu-de-01',
                        'eu-de-02',
                        'eu-de-03']),
                    'os': 'EulerOS 2.5',
                    'login': {
                        'sshKey': 'key-' + uuid.uuid4().hex
                    },
                    'rootVolume': {
                        'volumetype': random.choice(['SAS', 'SATA', 'SSD']),
                        'size': random.randint(40, 32768),
                    },
                    'dataVolumes': [
                        {
                            'volumetype': random.choice([
                                'SAS', 'SATA', 'SSD']),
                            'size': random.randint(100, 32768),
                            'extendParam': {
                                'useType': 'docker'
                            }
                        }
                    ],
                    'billingMode': 0,
                    'extendParam': {
                        'alpha.cce/preInstall': 'bHMgLWw=',
                        'alpha.cce/postInstall': 'bHMgLWwK',
                        'maxPods': 110,
                    },
                    'k8sTags': {
                        't1-' + uuid.uuid4().hex: 'v1-' + uuid.uuid4().hex,
                        't2-' + uuid.uuid4().hex: 'v2-' + uuid.uuid4().hex,
                    },
                    'taints': [
                        {
                            'key': 'key-' + uuid.uuid4().hex,
                            'value': 'value-' + uuid.uuid4().hex,
                            'effect': random.choice([
                                'NoSchedule',
                                'PrefereNoSchedule',
                                'NoExecute'])
                        },
                        {
                            'key': 'key-' + uuid.uuid4().hex,
                            'value': 'value-' + uuid.uuid4().hex,
                            'effect': random.choice([
                                'NoSchedule',
                                'PrefereNoSchedule',
                                'NoExecute'])
                        }
                    ],
                    'userTags': [
                        {
                            'key': 'key-' + uuid.uuid4().hex,
                            'value': 'value-' + uuid.uuid4().hex,
                        },
                        {
                            'key': 'key-' + uuid.uuid4().hex,
                            'value': 'value-' + uuid.uuid4().hex,
                        }
                    ],
                    'nodeNicSpec': {
                        'primaryNic': {
                            'subnetId': 'nw-' + uuid.uuid4().hex,
                        }
                    }
                }
            },
            'status': {
                'currentNode': random.randint(0, 100),
                'phase': ''
            }
        }
        obj = node_pool.NodePool.existing(**object_info)
        return obj
