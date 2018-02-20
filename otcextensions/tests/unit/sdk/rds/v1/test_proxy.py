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

from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.rds.v1 import _proxy
from otcextensions.sdk.rds.v1 import datastore
from otcextensions.sdk.rds.v1 import flavor


class TestRdsProxy(test_proxy_base.TestProxyBase):

    PROJECT_ID = '123'

    def setUp(self):
        super(TestRdsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        self.session.get_project_id.side_effect = [TestRdsProxy.PROJECT_ID]

    def test_datastores(self):
        self.verify_list(
            self.proxy.datastores, datastore.Datastore,
            method_kwargs={
                'db_name': 'test',
            },
            paginated=False,
            expected_kwargs={
                'datastore_name': 'test',
                'endpoint_override': None,
                'headers': {
                    'Content-Type': 'application/json',
                    'X-Language': 'en-us',
                },
                'project_id': TestRdsProxy.PROJECT_ID
            }
        )

    def test_flavor_get(self):
        self.verify_get(self.proxy.get_flavor, flavor.Flavor,
                        expected_kwargs={'project_id': TestRdsProxy.PROJECT_ID}
                        )
        self.assertEqual(
            'application/json',
            self.proxy.additional_headers['Content-Type'])

    def test_flavors(self):
        self.verify_list(
            self.proxy.flavors, flavor.Flavor,
            paginated=False,
            expected_kwargs={
                'project_id': TestRdsProxy.PROJECT_ID
            }
        )
