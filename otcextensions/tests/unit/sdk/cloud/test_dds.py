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

from openstack import exceptions

from otcextensions.tests.unit.sdk import base


class TestDdsMixin(base.TestCase):

    def setUp(self):
        super(TestDdsMixin, self).setUp()

    def test_create_dds_instance(self):
        attrs = {
            'name': 'dds_name',
            'datastore_type': 'DDS',
            'datastore_version': '3.1',
            'datastore_storage_engine': 'wt',
            'region': 'eu-de',
            'availability_zone': 'az1',
            'router': 'my_router',
            'network': 'my_network',
            'security_group': 'my_security_group',
            'password': 'password12344@@!',
            'mode': 'ReplicaSet',
            'flavors': [{
                "type": "replica",
                "num": 1,
                "storage": "ULTRAHIGH",
                "size": 30,
                "spec_code": "dds.mongodb.s2.medium.4.repset"
            }],
            'backup_timeframe': '23:00-00:00',
            'backup_keepdays': '1',
            'ssl_option': '0',
        }

        self.register_uris([
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['my_router']
                ),
                json={'id': 'router_id'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['my_network']
                ),
                json={'id': 'net_id'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='security-groups',
                    base_url_append='v2.0',
                    append=['my_security_group']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_dds_url(
                    resource='flavors',
                    qs_elements=[f'region={attrs["region"]}',
                                 f'engine_name={attrs["datastore_type"]}']
                ),
                status_code=200,
                json={'flavors': [
                    {"type": "replica",
                     "num": 1,
                     "storage": "ULTRAHIGH",
                     "size": 30,
                     "spec_code": "dds.mongodb.s2.medium.4.repset"
                     }]
                }
            ),
            dict(
                method='POST',
                uri=self.get_dds_url(
                    base_url_append='instances'
                ),
                status_code=200,
                json={
                    'instance': {'id': 123987},
                    'job_id': '15'
                }
            ),
            dict(
                method='GET',
                uri=self.get_dds_url(
                    base_url_append='instances',
                    qs_elements=['id=123987']
                ),
                status_code=200,
                json={'instances': [{'id': 123987, 'name': 'inst_name'}]}
            )
        ])

        obj = self.cloud.create_dds_instance(**attrs)
        self.assert_calls()

        self.assertEqual(123987, obj.id)

    def test_create_dds_instance_bad_flavor_spec_code(self):
        attrs = {
            'name': 'dds_name',
            'datastore_type': 'DDS',
            'datastore_version': '3.1',
            'datastore_storage_engine': 'wt',
            'region': 'eu-de',
            'availability_zone': 'az1',
            'router': 'my_router',
            'network': 'my_network',
            'security_group': 'my_security_group',
            'password': 'password12344@@!',
            'mode': 'ReplicaSet',
            'flavors': [{
                "type": "replica",
                "num": 1,
                "storage": "ULTRAHIGH",
                "size": 30,
                "spec_code": "dds"
            }],
            'backup_timeframe': '23:00-00:00',
            'backup_keepdays': '1',
            'ssl_option': '0',
        }

        self.register_uris([
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['my_router']
                ),
                json={'id': 'router_id'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['my_network']
                ),
                json={'id': 'net_id'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='security-groups',
                    base_url_append='v2.0',
                    append=['my_security_group']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_dds_url(
                    resource='flavors',
                    qs_elements=[f'region={attrs["region"]}',
                                 f'engine_name={attrs["datastore_type"]}']
                ),
                status_code=200,
                json={'flavors': [
                    {"type": "replica",
                     "num": 1,
                     "storage": "ULTRAHIGH",
                     "size": 30,
                     "spec_code": "dds.mongodb.s2.medium.4.repset"
                     }]
                }
            )
        ])

        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_dds_instance,
            **attrs
        )
        self.assert_calls()
