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
import mock

from otcextensions.osclient.sdrs.v1 import active_domains
from otcextensions.tests.unit.osclient.sdrs.v1 import fakes


class TestActiveDomains(fakes.TestSDRS):
    object = fakes.FakeActiveDomain.create_multiple(2)

    columns = ('ID', 'name', 'description', 'sold_out',
               'local_replication_cluster', 'remote_replication_cluster')

    flat_data = [(active_domains._flatten_domain(obj)) for obj in object]

    data = [
        (flat_d['id'],
         flat_d['name'],
         flat_d['description'],
         flat_d['sold_out'],
         flat_d['local_replication_cluster'],
         flat_d['remote_replication_cluster']
         ) for flat_d in flat_data]

    def setUp(self):
        super(TestActiveDomains, self).setUp()
        self.cmd = active_domains.ListDomain(self.app, None)
        self.client.get_domains = mock.Mock(self.object)
        self.client.api_mock = self.client.get_domains

    def test_flatten(self):
        obj = fakes.FakeActiveDomain.create_one()
        flat_data = active_domains._flatten_domain(obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['description'],
            flat_data['sold_out'],
            flat_data['local_replication_cluster'],
            flat_data['remote_replication_cluster']
        )

        cmp_data = (
            obj['domains'][0].id,
            obj['domains'][0].name,
            obj['domains'][0].description,
            obj['domains'][0].sold_out,
            obj['domains'][0].local_replication_cluster.availability_zone,
            obj['domains'][0].remote_replication_cluster.availability_zone
        )

        self.assertEqual(data, cmp_data)

    def test_default(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_domains.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        new_list = list(data)
        self.assertEqual(self.data, new_list)
