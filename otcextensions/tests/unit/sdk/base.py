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
        self.cloud.config.config['ddsv3_api_version'] = '3'

    def get_keystone_v3_token(
        self,
        project_name='admin',
    ):
        ets_rds = self.os_fixture._get_endpoint_templates('rdsv3')
        svc_rds = self.os_fixture.v3_token.add_service('rdsv3', name='rdsv3')
        svc_rds.add_standard_endpoints(region='RegionOne', **ets_rds)

        ets_cce = self.os_fixture._get_endpoint_templates('ccev2.0')
        svc_cce = self.os_fixture.v3_token.add_service(
            'ccev2.0', name='ccev2.0'
        )
        svc_cce.add_standard_endpoints(region='RegionOne', **ets_cce)

        ets_dds = self.os_fixture._get_endpoint_templates('ddsv3')
        svc_dds = self.os_fixture.v3_token.add_service('ddsv3', name='ddsv3')
        svc_dds.add_standard_endpoints(region='RegionOne', **ets_dds)

        return super(TestCase, self).get_keystone_v3_token()

    def get_rds_url(
        self,
        resource=None,
        append=None,
        base_url_append=None,
        qs_elements=None,
    ):
        url = self.get_mock_url(
            'rdsv3',
            resource=resource,
            append=append,
            base_url_append=base_url_append,
            qs_elements=qs_elements,
        )

        url = url % {'project_id': self.cloud.current_project_id}

        return url

    def get_cce_url(
        self,
        resource=None,
        append=None,
        base_url_append=None,
        qs_elements=None,
    ):
        endpoint_url = (
            'https://ccev2.0.example.com/' 'api/v3/projects/%(project_id)s'
        ) % {'project_id': self.cloud.current_project_id}
        # Strip trailing slashes, so as not to produce double-slashes below
        if endpoint_url.endswith('/'):
            endpoint_url = endpoint_url[:-1]
        to_join = [endpoint_url]
        qs = ''
        if base_url_append:
            to_join.append(base_url_append)
        if resource:
            to_join.append(resource)
        to_join.extend(append or [])
        if qs_elements is not None:
            qs = '?%s' % '&'.join(qs_elements)
        return '%(uri)s%(qs)s' % {'uri': '/'.join(to_join), 'qs': qs}

    def get_dds_url(
        self,
        resource=None,
        append=None,
        base_url_append=None,
        qs_elements=None,
    ):
        url = self.get_mock_url(
            'ddsv3',
            resource=resource,
            append=append,
            base_url_append=base_url_append,
            qs_elements=qs_elements,
        )

        url = url % {'project_id': self.cloud.current_project_id}

        return url
