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
import copy

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.cce.v3 import cluster as _cluster

OS_HEADERS = {
    'Content-Type': 'application/json',
}

EXAMPLE_LIST = {
    'kind': 'Cluster',
    'apiVersion': 'v3',
    'items': [
        {
            'kind': 'Cluster',
            'apiVersion': 'v3',
            'metadata': {
                'name': 'mycluster-demo',
                'uid': '40c54866-38c5-11e9-b246-0255ac101413',
                'creationTimestamp': '2019-02-25 06:19:05.789462 +0000 UTC',
                'updateTimestamp': '2019-02-25 06:26:14.457426 +0000 UTC'
            },
            'spec': {
                'type': 'VirtualMachine',
                'flavor': 'cce.s1.small',
                'version': 'v1.13.10-r0',
                'az': 'eu-de-01',
                'supportIstio': True,
                'description': 'thisisademocluster',
                'hostNetwork': {
                    'vpc': 'a8cc62dc-acc2-47d0-9bfb-3b1d776c520b',
                    'subnet': '6d9e5355-85af-4a89-af28-243edb700db6'
                },
                'containerNetwork': {
                    'mode': 'overlay_l2',
                    'cidr': '172.16.0.0/16'
                },
                'authentication': {
                    'mode': 'rbac',
                    'authenticatingProxy': {}
                },
                'billingMode': 0
            },
            'status': {
                'phase': 'Available',
                'endpoints': {
                    'internal': 'https://192.168.0.129:5443',
                    'external_otc': 'https://40c54866-38c5-'
                }
            }
        }
    ]
}


class TestCluster(base.TestCase):

    def setUp(self):
        super(TestCluster, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)

        self.sot = _cluster.Cluster()

        self.sot_expected = _cluster.Cluster(**EXAMPLE_LIST['items'][0])

    def test_basic(self):
        sot = _cluster.Cluster()
        self.assertEqual('', sot.resource_key)
        self.assertEqual('', sot.resources_key)
        self.assertEqual('/clusters',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        obj = EXAMPLE_LIST['items'][0]
        sot = _cluster.Cluster.existing(**obj)
        self.assertEqual(obj['metadata']['uid'], sot.id)
        self.assertEqual(obj['kind'], sot.kind)
        # self.assertEqual(obj['spec'], sot.spec)
        # self.assertEqual(obj['status'], sot.status)

    def test_list(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = copy.deepcopy(EXAMPLE_LIST)

        self.sess.get.return_value = mock_response

        result = list(
            self.sot.list(
                self.sess,
            )
        )

        self.sess.get.assert_called_once_with(
            '/clusters',
            params={},
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )

        expected_list = [
            self.sot_expected,
        ]

        self.assertEqual(
            set(i.id for i in expected_list),
            set(i.id for i in result))

    def test_get_status(self):
        data = EXAMPLE_LIST['items'][0]
        cluster = _cluster.Cluster(**data)

        self.assertEqual(data['status']['phase'], getattr(cluster,
                                                          'status.status'))
