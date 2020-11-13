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

from openstack.tests.unit import base

from otcextensions import sdk


class TestCase(base.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        sdk.load(self.cloud)
        self.cloud.config.config['rdsv3_api_version'] = '3'

    def get_keystone_v3_token(
            self,
            project_name='admin',
    ):
        ets = self.os_fixture._get_endpoint_templates('rdsv3')
        svc = self.os_fixture.v3_token.add_service('rdsv3', name='rdsv3')
        svc.add_standard_endpoints(region='RegionOne', **ets)

        return super(TestCase, self).get_keystone_v3_token()

    def get_rds_url(self, resource=None,
                    append=None, base_url_append=None,
                    qs_elements=None):
        url = self.get_mock_url(
            'rdsv3', resource=resource,
            append=append, base_url_append=base_url_append,
            qs_elements=qs_elements)

        url = url % {'project_id': self.cloud.current_project_id}

        return url
