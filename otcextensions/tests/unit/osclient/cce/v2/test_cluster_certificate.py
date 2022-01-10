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
#
import mock

from otcextensions.osclient.cce.v2 import cluster_certificate
from otcextensions.sdk.cce.v3 import cluster
from otcextensions.tests.unit.osclient.cce.v2 import fakes


class TestClusterCertificate(fakes.TestCCE):

    def setUp(self):
        super(TestClusterCertificate, self).setUp()

    def test_flatten(self):
        _obj = fakes.FakeClusterCertificate.create_one()

        flat_data = cluster_certificate._flatten_cluster_certificate(_obj)

        data = (
            flat_data['name'],
            flat_data['cluster'],
            flat_data['user'],
            flat_data['ca'],
            flat_data['client_certificate'],
            flat_data['client_key'],
        )

        cmp_data = (
            _obj.context['name'],
            _obj.context['cluster'],
            _obj.context['user'],
            _obj.ca,
            _obj.client_certificate,
            _obj.client_key,
        )

        self.assertEqual(data, cmp_data)


class TestClusterCertificateShow(fakes.TestCCE):
    _obj = fakes.FakeClusterCertificate.create_one()

    columns = ('name', 'cluster', 'user', 'ca',
               'client_certificate', 'client_key')
    flat_data = cluster_certificate._flatten_cluster_certificate(_obj)
    data = (
        flat_data['name'],
        flat_data['cluster'],
        flat_data['user'],
        flat_data['ca'],
        flat_data['client_certificate'],
        flat_data['client_key'],
    )

    def setUp(self):
        super(TestClusterCertificateShow, self).setUp()

        self.cmd = cluster_certificate.ShowCCEClusterCertificates(
            self.app, None)

        self.client.find_cluster = mock.Mock(
            return_value=cluster.Cluster(id='cluster_uuid'))
        self.client.get_cluster_certificates = mock.Mock()

    def test_get(self):
        arglist = [
            'cluster_uuid'
        ]

        verifylist = [
            ('cluster', 'cluster_uuid')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.get_cluster_certificates.side_effect = [
            self._obj
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_cluster_certificates.assert_called_once_with(
            cluster='cluster_uuid',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
