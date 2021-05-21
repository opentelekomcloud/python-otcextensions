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

from otcextensions.sdk.cbr.v3 import policy
from otcextensions.tests.unit.osclient.cbr.v3 import fakes


class TestShowPolicy(fakes.TestCBR):

    _obj = fakes.FakePolicy.create_one()

    def setUp(self):
        super(TestShowPolicy, self).setUp()

        self.cmd = policy.ShowPolicy(self.app, None)

        self.client.find_policy = mock.Mock()

        self.client.find_policy = mock.Mock(
            return_value=policy.Policy(id='policy_uuid'))

    def test_show(self):
        arglist = [
            'policy_uuid',
        ]

        verifylist = [
            ('policy', 'policy_uuid'),
        ]

        dict_pol = self._obj.to_dict()
        print(dict_pol)
