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
import datetime
import random
import uuid

import mock

from openstackclient.tests.unit import utils

from otcextensions.tests.unit.osclient import fake_base

from otcextensions.sdk.cce.v1 import cluster
# from otcextensions.sdk.kms.v1 import data_key


class TestCCE(utils.TestCommand):

    def setUp(self):
        super(TestCCE, self).setUp()

        self.app.client_manager.cce = mock.Mock()
        self.client = self.app.client_manager.cce


class FakeCluster(fake_base.Fake):
    """Fake one or more Cluster"""

    @classmethod
    def generate(cls):
        object_info = {
            'kind': 'cluster',
            'metadata': {
                'uuid': 'id-' + uuid.uuid4().hex,
                'name': 'name-' + uuid.uuid4().hex,
            },
            'spec': {
                'cpu': random.randint(1, 15),
                'memory': random.randint(1, 150000),
                'endpoint': 'endpoint-' + uuid.uuid4().hex,
                'availability_zone': 'az-' + uuid.uuid4().hex,
                'vpc': 'vpc-' + uuid.uuid4().hex,
                'hostList': {
                    'spec': {
                        'hostList': [{
                            'kind': 'host'
                        }]
                    }
                }
            },
            'status': {
                'status': 'sts'
            }
        }
        obj = cluster.Cluster.existing(**object_info)
        return obj
