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

from openstack.tests.unit import base

from otcextensions.sdk.obs.v1 import container


EXAMPLE = {
    "Name": "container_name",
    "CreationDate": "2013-01-15T05:52:15.920Z<",
}

EXAMPLE_LIST = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ListAllMyBucketsResult xmlns="http://obs.otc.t-systems.com/doc/2016-01-01/">
<Owner><ID>some_id</ID>
<DisplayName></DisplayName>
</Owner><Buckets>
<Bucket><Name>test-v1</Name>
<CreationDate>2018-10-02T08:54:55.885Z</CreationDate></Bucket>
<Bucket><Name>test-v2</Name>
<CreationDate>2018-09-19T12:47:22.205Z</CreationDate></Bucket>
</Buckets></ListAllMyBucketsResult>
"""


class TestContainer(base.TestCase):

    def setUp(self):
        super(TestContainer, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = container.Container()

        self.assertEqual('/', sot.base_path)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_head)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):

        sot = container.Container(**EXAMPLE)
        self.assertEqual(EXAMPLE['Name'], sot.id)
        self.assertEqual(EXAMPLE['Name'], sot.name)
        self.assertEqual(EXAMPLE['CreationDate'], sot.creation_date)

    def test_list(self):

        sot = container.Container()

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = EXAMPLE_LIST

        self.sess.get.return_value = mock_response

        result = list(sot.list(
            self.sess,
        ))

        self.assertEqual(2, len(result))
        self.assertEqual('test-v1', result[0].name)
        self.assertEqual('test-v2', result[1].name)

    def test_create(self):

        sot = container.Container(name='test-v1')

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = ''

        self.sess.put.return_value = mock_response

        sot.create(
            self.sess,
            endpoint_override='epo',
            requests_auth=2)

        self.sess.put.assert_called_once_with(
            '/',
            data=None,
            endpoint_override='epo',
            requests_auth=2
        )
