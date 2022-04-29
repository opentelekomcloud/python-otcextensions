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
import datetime

import mock

from otcextensions.sdk.sdrs.v1 import active_domains
from otcextensions.sdk.sdrs.v1 import job
from otcextensions.tests.unit.osclient import test_base

FAIL_REASON = "SdrsExtendReplicationPairNewTask-fail:SDRS.0011:Client " \
              "error : {\"badRequest\": {\"message\": \"Extending Replica" \
              "tion error: Check replication volume size or volume " \
              "status or volume quota fail, detail is f() takes exactly " \
              "1 argument (2 given)\", \"code\": 400}}"


def generate_entities():
    """Generate random list of sub_jobs"""
    jobs_list = []
    random_int = random.randint(1, 10)
    while random_int > 0:
        sub_job = {
            'id': uuid.uuid4().hex,
            'status': random.choice(['SUCCESS', 'FAIL', 'INIT']),
            'job_type': uuid.uuid4().hex,
            'begin_time': datetime.datetime.now(),
            'end_time': datetime.datetime.now(),
            'error_code': None,
            'fail_reason': None,
            'entities': {
                'server_group_id': uuid.uuid4().hex
            }
        }
        jobs_list.append(sub_job)
        random_int -= 1
    return jobs_list


class TestSDRS(test_base.TestCommand):

    def setUp(self):
        super(TestSDRS, self).setUp()

        self.app.client_manager.sdrs = mock.Mock()
        self.client = self.app.client_manager.sdrs


class FakeActiveDomain(test_base.Fake):
    """Fake one or more SDRS Active-active domains"""

    @classmethod
    def generate(cls):
        object_info = {
            'domains': [{
                'id': 'id-' + uuid.uuid4().hex,
                'name': 'name-' + uuid.uuid4().hex,
                'description': 'description-' + uuid.uuid4().hex,
                'sold_out': random.choice([True, False]),
                'local_replication_cluster': {
                    'availability_zone': random.choice(['eu-de-01',
                                                        'eu-de-02',
                                                        'eu-de-03'])
                },
                'remote_replication_cluster': {
                    'availability_zone': random.choice(['eu-de-01',
                                                        'eu-de-02',
                                                        'eu-de-03'])
                }
            }]
        }

        obj = active_domains.ActiveDomains.existing(**object_info)
        return obj


class FakeJob(test_base.Fake):
    """Fake one or more SDRS jobs"""

    @classmethod
    def generate(cls):
        object_info = {
            'job_id': uuid.uuid4().hex,
            'status': random.choice(['SUCCESS', 'FAIL', 'INIT']),
            'job_type': uuid.uuid4().hex,
            'begin_time': datetime.datetime.now(),
            'end_time': datetime.datetime.now()
        }

        entities = random.choice([True, False])

        if entities:
            object_info['entities'] = dict(sub_jobs=generate_entities())
        else:
            object_info['error_code'] = 'SDRS.001'
            object_info['fail_reason'] = FAIL_REASON

        obj = job.Job.existing(**object_info)
        return obj
