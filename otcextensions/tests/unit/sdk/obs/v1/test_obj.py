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
import base64
import mock
import hashlib

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.obs.v1 import obj


EXAMPLE = {
    "Key": "name",
    "LastModified": "2013-01-15T05:52:15.920Z<",
    "ETag": "etag",
}

EXAMPLE_LIST = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ListBucketResult xmlns="http://obs.otc.t-systems.com/doc/2016-01-01/">
<Name>ag-test-v1</Name><Prefix></Prefix><Marker></Marker>
<MaxKeys>1000</MaxKeys><IsTruncated>false</IsTruncated>
<Contents><Key>setup.py</Key>
<LastModified>2018-10-02T10:17:04.666Z</LastModified>
<ETag>"9c24605289b49ad77a51ba7986425158"</ETag>
<Size>1030</Size><Owner><ID>859d69896ff44ba6a20845edb43f311e</ID>
<DisplayName>OTC00000000001000000448</DisplayName></Owner>
<StorageClass>STANDARD</StorageClass></Contents></ListBucketResult>
"""


class TestObject(base.TestCase):

    def setUp(self):
        super(TestObject, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = obj.Object()

        self.assertEqual('/', sot.base_path)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_head)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):

        sot = obj.Object(**EXAMPLE)
        self.assertEqual(EXAMPLE['Key'], sot.id)
        self.assertEqual(EXAMPLE['Key'], sot.name)
        self.assertEqual(EXAMPLE['LastModified'], sot.last_modified)
        self.assertEqual(EXAMPLE['ETag'], sot.etag)

    def test_list(self):

        sot = obj.Object()

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = EXAMPLE_LIST

        self.sess.get.return_value = mock_response

        result = list(sot.list(
            self.sess,
        ))

        self.assertEqual(1, len(result))
        self.assertEqual('setup.py', result[0].name)
        self.assertEqual('9c24605289b49ad77a51ba7986425158', result[0].etag)
        self.assertEqual(1030, result[0].content_length)

    def test_create(self):

        data = 'some test data'
        md5 = hashlib.md5()
        md5.update(str.encode(data))
        data_md5 = base64.b64encode(md5.digest()).decode()
        sot = obj.Object(name='test-v1', data=data)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = ''

        self.sess.put.return_value = mock_response

        sot.create(
            self.sess,
            endpoint_override='epo',
            requests_auth=2)

        self.sess.put.assert_called_once_with(
            '/test-v1',
            data=data,
            endpoint_override='epo',
            requests_auth=2,
            headers={
                'Content-MD5': data_md5
            }
        )
    #
