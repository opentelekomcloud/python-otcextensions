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
import mock
from keystoneauth1 import adapter

from openstack import resource
from openstack.tests.unit import base
from openstack.tests.unit import test_resource

from otcextensions.sdk.deh.v1 import host


FAKE_ID = '68d5745e-6af2-40e4-945d-fe449be00148'
EXAMPLE = {
    'dedicated_host_id': FAKE_ID,
    'name': 'win_2008 servers',
    'auto_placement': 'off',
    'availability_zone': 'az1',
    'host_properties': {
        'vcpus': 36,
        'cores': 12,
        'sockets': 2,
        'memory': 1073741824,
        'host_type': 'h1',
        'host_type_name': 'High performance',
        'available_instance_capacities': [
            {
                'flavor': 'h1.large'
            },
            {
                'flavor': 'h1.2large'
            },
            {
                'flavor': 'h1.4large'
            },
            {
                'flavor': 'h1.8large'
            }
        ]
    },
    'state': 'available',
    'project_id': '9c53a566cb3443ab910cf0daebca90c4',
    'available_vcpus': 20,
    'available_memory': 1073201821,
    'instance_total': 2,
    'allocated_at': '2016-10-10T14:35:47Z',
    'released_at': None,
    'instance_uuids': [
        'erf5th66cb3443ab912ff0daebca3456',
        '23457h66cb3443ab912ff0daebcaer45'
    ]
}


class TestHost(base.TestCase):

    def setUp(self):
        super(TestHost, self).setUp()
        self.sot = host.Host(id='id')

        self.request = mock.Mock(spec=resource._Request)
        self.request.url = "uri"
        self.request.body = "body"
        self.request.headers = "headers"

        self.response = test_resource.FakeResponse({})

        self.sot._prepare_request = mock.Mock(return_value=self.request)
        self.sot._translate_response = mock.Mock()

        self.session = mock.Mock(spec=adapter.Adapter)
        self.session.get = mock.Mock(return_value=self.response)
        self.session.post = mock.Mock(return_value=self.response)

    def test_basic(self):
        sot = host.Host()

        self.assertEqual('/dedicated-hosts', sot.base_path)

        self.assertDictEqual({'availability_zone': 'availability_zone',
                              'changes_since': 'changes-since',
                              'flavor': 'flavor',
                              'host_type': 'host_type',
                              'host_type_name': 'host_type_name',
                              'id': 'id',
                              'instance_uuid': 'instance_uuid',
                              'limit': 'limit',
                              'marker': 'marker',
                              'name': 'name',
                              'released_at': 'released_at',
                              'status': 'status',
                              'tags': 'tags',
                              'tenant': 'tenant'},
                             sot._query_mapping._mapping)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):

        sot = host.Host(**EXAMPLE)
        self.assertEqual(EXAMPLE['dedicated_host_id'], FAKE_ID)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['auto_placement'], sot.auto_placement)
        self.assertEqual(EXAMPLE['availability_zone'], sot.availability_zone)
        self.assertEqual(EXAMPLE['state'], sot.status)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['available_vcpus'], sot.available_vcpus)
        self.assertEqual(EXAMPLE['available_memory'], sot.available_memory)
        self.assertEqual(EXAMPLE['instance_total'], sot.instance_total)
        self.assertEqual(EXAMPLE['released_at'], sot.released_at)
        ref = EXAMPLE['host_properties']
        actual = sot.host_properties
        self.assertEqual(ref['vcpus'], actual.vcpus)
        self.assertEqual(ref['cores'], actual.cores)
        self.assertEqual(ref['sockets'], actual.sockets)
        self.assertEqual(ref['memory'], actual.memory)
        self.assertEqual(ref['host_type'], actual.host_type)
        self.assertEqual(ref['host_type_name'], actual.host_type_name)

    def test_fetch_tags(self):
        res = self.sot
        sess = self.session

        tags = [
            {'key': 'color', 'value': 'blue'},
            {'key': 'color', 'value': 'green'}
        ]

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.links = {}
        mock_response.json.return_value = {
            'tags': tags}

        sess.get.side_effect = [mock_response]

        result = res.fetch_tags(sess)
        # Check tags attribute is updated
        self.assertEqual(tags, res.tags)
        # Check the passed resource is returned
        self.assertEqual(res, result)
        url = 'dedicated-host-tags/' + res.id + '/tags'
        sess.get.assert_called_once_with(url)

    def test_add_tags(self):
        res = self.sot
        sess = self.session

        tags = [
            {'key': 'color', 'value': 'blue'},
            {'key': 'color', 'value': 'green'}
        ]

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.links = {}
        mock_response.json.return_value = {
            'tags': tags}

        sess.get.side_effect = [mock_response]

        result = res.add_tags(sess, tags)
        # Check tags attribute is updated
        self.assertEqual(tags, res.tags)
        # Check the passed resource is returned
        self.assertEqual(res, result)
        url = 'dedicated-host-tags/' + res.id + '/tags/action'
        sess.post.assert_called_once_with(
            url,
            json={'action': 'create', 'tags': tags}
        )

    def test_remove_tags(self):
        res = self.sot
        sess = self.session

        tags = [
            {'key': 'color', 'value': 'blue'},
            {'key': 'color', 'value': 'green'}
        ]

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.links = {}
        mock_response.json.return_value = {
            'tags': []}

        sess.get.side_effect = [mock_response]

        result = res.remove_tags(sess, tags)
        # Check tags attribute is updated
        self.assertEqual([], res.tags)
        # Check the passed resource is returned
        self.assertEqual(res, result)
        url = 'dedicated-host-tags/' + res.id + '/tags/action'
        sess.post.assert_called_once_with(
            url,
            json={'action': 'delete', 'tags': tags}
        )
