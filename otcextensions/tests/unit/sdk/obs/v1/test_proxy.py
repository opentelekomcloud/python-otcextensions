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

from otcextensions.sdk.ak_auth import AKRequestsAuth
from otcextensions.sdk.obs.v1 import _proxy
from otcextensions.sdk.obs.v1 import container as _container
from otcextensions.sdk.obs.v1 import obj as _obj


class TestObsProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestObsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

        self._ak_auth = AKRequestsAuth(
            access_key='ak',
            secret_access_key='sk',
            host='host',
            region='regio',
            service='OBS')
        self.proxy._ak_auth = self._ak_auth
        self.proxy.region_name = 'regio'

    def test_containers(self):
        self.verify_list(
            self.proxy.containers, _container.Container,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            expected_kwargs={
                'requests_auth': self._ak_auth
            }
        )

    def test_create_container(self):
        self.verify_create(
            self.proxy.create_container, _container.Container,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_kwargs={
                'name': 'nm'
            },
            expected_kwargs={
                'name': 'nm',
                'endpoint_override': 'https://nm.obs.regio.otc.t-systems.com',
                'requests_auth': self._ak_auth
            }
        )

    def test_delete_container(self):
        self.verify_delete(
            self.proxy.delete_container, _container.Container, ignore=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={
                'endpoint_override': 'https://resource_or_id.obs.regio.'
                                     'otc.t-systems.com',
                'ignore_missing': True,
                'requests_auth': self._ak_auth
            }
        )

    def test_get_container_metadata(self):
        self.assertRaises(
            NotImplementedError,
            self.proxy.get_container_metadata,
            'container'
        )

    def test_set_container_metadata(self):
        self.assertRaises(
            NotImplementedError,
            self.proxy.set_container_metadata,
            'container',
            metadata={}
        )

    def test_delete_container_metadata(self):
        self.assertRaises(
            NotImplementedError,
            self.proxy.delete_container_metadata,
            'container',
            keys={}
        )

    def test_objects(self):
        self.verify_list(
            self.proxy.objects, _obj.Object,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_args={
                'container': 'container'
            },
            expected_kwargs={
                'endpoint_override': 'https://container.obs.regio.'
                                     'otc.t-systems.com',
                'requests_auth': self._ak_auth
            }
        )

    def test_create_object(self):
        self.verify_create(
            self.proxy.create_object, _obj.Object,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_kwargs={
                'name': 'nm',
                'container': 'container'
            },
            expected_kwargs={
                'name': 'nm',
                'endpoint_override': 'https://container.obs.regio.otc.'
                                     't-systems.com',
                'requests_auth': self._ak_auth
            }
        )

    def test_delete_object(self):
        self.verify_delete(
            self.proxy.delete_object, _obj.Object, ignore=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={
                'endpoint_override': 'https://None.obs.regio.'
                                     'otc.t-systems.com',
                'ignore_missing': True,
                'requests_auth': self._ak_auth
            }
        )

    def test_download_object(self):
        self._verify2(
            'otcextensions.sdk.obs.v1.obj.Object.download',
            self.proxy.download_object,
            method_args=[{}],
            method_kwargs={'container': 'cont'},
            expected_args=[self.proxy],
            expected_kwargs={
                'filename': '-',
                'endpoint_override': 'https://cont.obs.regio.'
                                     'otc.t-systems.com',
                'requests_auth': self._ak_auth
            }
        )

    def test_stream_object(self):
        self.assertRaises(
            NotImplementedError,
            self.proxy.stream_object,
            'container',
        )

    def test_copy_object(self):
        self.assertRaises(
            NotImplementedError,
            self.proxy.copy_object,
        )

    def test_get_object_metadata(self):
        self.assertRaises(
            NotImplementedError,
            self.proxy.get_object_metadata,
            'container',
        )

    def test_set_object_metadata(self):
        self.assertRaises(
            NotImplementedError,
            self.proxy.set_object_metadata,
            'container',
        )

    def test_delete_object_metadata(self):
        self.assertRaises(
            NotImplementedError,
            self.proxy.delete_object_metadata,
            'container',
        )


class TestExtractName(TestObsProxy):

    def test_extract_name(self):

        self.assertEqual(
            ['bucket'],
            self.proxy._extract_name('/', project_id='123')
        )
        self.assertEqual(
            ['object'],
            self.proxy._extract_name('/dummy', project_id='123')
        )
        self.assertEqual(
            ['object'],
            self.proxy._extract_name('/dummy/dummy2', project_id='123')
        )
