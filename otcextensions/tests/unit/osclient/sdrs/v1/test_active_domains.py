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

from otcextensions.osclient.sdrs.v1 import active_domains
from otcextensions.tests.unit.osclient.sdrs.v1 import fakes


class TestActiveDomains(fakes.TestSDRS):

    def setUp(self):
        super(TestActiveDomains, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeActiveDomain.create_one()
        i = len(obj['domains']) - 1
        flat_data = active_domains._flatten_domain(i, obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['description'],
            flat_data['sold_out'],
            flat_data['local_replication_cluster'],
            flat_data['remote_replication_cluster']
        )

        cmp_data = (
            obj['domains'][i].id,
            obj['domains'][i].name,
            obj['domains'][i].description,
            obj['domains'][i].sold_out,
            obj['domains'][i].local_replication_cluster.availability_zone,
            obj['domains'][i].remote_replication_cluster.availability_zone
        )

        self.assertEqual(data, cmp_data)
