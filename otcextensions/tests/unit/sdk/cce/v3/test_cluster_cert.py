# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import copy

from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.cce.v3 import cluster_cert


EXAMPLE = {
    "kind": "Config",
    "apiVersion": "v1",
    "preferences": {},
    "clusters": [
        {
            "name": "internalCluster",
            "cluster": {
                "server": "https://192.168.1.7:5443",
                "certificate-authority-data": "ca-data"
            }
        }
    ],
    "users": [
        {
            "name": "user",
            "user": {
                "client-certificate-data": "cc-data",
                "client-key-data": "ck-data"
            }
        }
    ],
    "contexts": [
        {
            "name": "internal",
            "context": {
                "cluster": "internalCluster",
                "user": "user"
            }
        }
    ],
    "current-context": "internal"
}


class TestClusterCert(base.TestCase):

    def setUp(self):
        super(TestClusterCert, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)

    def test_basic(self):
        sot = cluster_cert.ClusterCertificate()
        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)
        self.assertEqual('/clusters/%(cluster_id)s/clustercert',
                         sot.base_path)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        obj = copy.deepcopy(EXAMPLE)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = obj
        mock_response.headers = {}

        sot = cluster_cert.ClusterCertificate()
        sot._translate_response(mock_response)
        self.assertEqual(
            obj['clusters'][0]['cluster']['certificate-authority-data'],
            sot.ca)
        self.assertEqual(
            obj['users'][0]['user']['client-certificate-data'],
            sot.client_certificate)
        self.assertEqual(
            obj['users'][0]['user']['client-key-data'],
            sot.client_key)
        self.assertEqual(
            {
                'name': obj['contexts'][0]['name'],
                'cluster': obj['clusters'][0]['cluster']['server'],
                'user': obj['contexts'][0]['context']['user']
            },
            sot.context)
