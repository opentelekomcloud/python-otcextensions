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

from otcextensions.tests.unit.osclient.css.v1 import fakes
from otcextensions.osclient.css.v1 import certificate


class TestDownloadCertificate(fakes.TestCss):

    def setUp(self):
        super(TestDownloadCertificate, self).setUp()

        self.cmd = certificate.DownloadCertificate(self.app, None)
        self.client.download_certificate = mock.Mock(return_value=None)

    def test_download_certificate(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.assertIsNone(result)
