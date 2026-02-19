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
#
import mock

from otcextensions.osclient.nat.v3 import private_gateway
from otcextensions.tests.unit.osclient.nat.v3 import fakes


class TestListPrivateNatGateways(fakes.TestNat):

    objects = fakes.FakePrivateNatGateway.create_multiple(3)

    column_list_headers = (
        'Id',
        'Name',
        'Spec',
        'Status',
        'Project Id',
        'Enterprise Project Id',
    )

    columns = (
        'id',
        'name',
        'spec',
        'status',
        'project_id',
        'enterprise_project_id',
    )

    data = []

    for s in objects:
        data.append((
            s.id,
            s.name,
            s.spec,
            s.status,
            s.project_id,
            s.enterprise_project_id,
        ))

    def setUp(self):
        super(TestListPrivateNatGateways, self).setUp()

        self.cmd = private_gateway.ListPrivateNatGateways(self.app, None)

        self.client.private_nat_gateways = mock.Mock()
        self.client.api_mock = self.client.private_nat_gateways

    def test_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.api_mock.side_effect = [self.objects]

        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            '--limit', '1',
            '--marker', 'm1',
            '--page-reverse',
            '--id', 'id1', 'id2',
            '--name', 'n1',
            '--description', 'd1',
            '--spec', 'Small',
            '--project-id', 'p1',
            '--status', 'ACTIVE',
            '--vpc-id', 'v1',
            '--virsubnet-id', 's1',
            '--enterprise-project-id', 'ep1',
        ]

        verifylist = [
            ('limit', 1),
            ('marker', 'm1'),
            ('page_reverse', True),
            ('id', ['id1', 'id2']),
            ('name', ['n1']),
            ('description', ['d1']),
            ('spec', ['Small']),
            ('project_id', ['p1']),
            ('status', ['ACTIVE']),
            ('vpc_id', ['v1']),
            ('virsubnet_id', ['s1']),
            ('enterprise_project_id', ['ep1']),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.client.api_mock.side_effect = [self.objects]

        self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            limit=1,
            marker='m1',
            page_reverse=True,
            id=['id1', 'id2'],
            name=['n1'],
            description=['d1'],
            spec=['Small'],
            project_id=['p1'],
            status=['ACTIVE'],
            vpc_id=['v1'],
            virsubnet_id=['s1'],
            enterprise_project_id=['ep1'],
        )
