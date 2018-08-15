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

from otcextensions.sdk.dcs.v1 import _proxy
from otcextensions.sdk.dcs.v1 import instance as _instance
from otcextensions.sdk.dcs.v1 import statistic as _stat

from openstack.tests.unit import test_proxy_base


class TestDCSProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestDCSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_create_instance(self):
        self.verify_create(
            self.proxy.create_instance, _instance.Instance,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
        )

    def test_instances(self):
        self.verify_list(
            self.proxy.instances, _instance.Instance,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
        )

    def test_instances_query(self):
        self.verify_list(
            self.proxy.instances, _instance.Instance,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'start': '1',
                'limit': '2',
                'name': '3',
                'status': '4',
                'includeFailure': True,
                'exactMatchName': True
            },
            expected_kwargs={
                'start': '1',
                'limit': '2',
                'name': '3',
                'status': '4',
                'includeFailure': True,
                'exactMatchName': True
            }
        )

    def test_get_instance(self):
        self.verify_get(
            self.proxy.get_instance, _instance.Instance,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
        )

    def test_find_instance(self):
        self.verify_find(
            self.proxy.find_instance, _instance.Instance,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._find',
        )

    def test_update_instance(self):
        self.sot = _instance.Instance()
        self.sot.update = mock.Mock(return_value=self.sot)
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.update_instance('VALUE', a='b')
        self.proxy._get_resource.assert_called_with(
            _instance.Instance,
            'VALUE',
            a='b'
        )
        self.sot.update.assert_called_with(
            self.proxy,
            has_body=False
        )
        self.proxy._get.assert_called_with(
            _instance.Instance,
            self.sot
        )

    def test_extend_instance(self):
        self.sot = _instance.Instance()
        self.sot.extend = mock.Mock(return_value={})
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.extend_instance(self.sot, 4)
        self.proxy._get_resource.assert_called_with(
            _instance.Instance,
            self.sot
        )
        self.sot.extend.assert_called_with(
            self.proxy,
            4
        )
        self.proxy._get.assert_called_with(
            _instance.Instance,
            self.sot
        )

    def test_delete_instance(self):
        self.verify_delete(
            self.proxy.delete_instance, _instance.Instance, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
        )

    def test_stop_instance(self):
        self.sot = _instance.Instance()
        self.sot.stop = mock.Mock(return_value={})
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._find = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.stop_instance(self.sot)
        self.sot.stop.assert_called_with(
            self.proxy,
        )
        self.proxy._get.assert_called_with(
            _instance.Instance,
            self.sot
        )

    def test_start_instance(self):
        self.sot = _instance.Instance()
        self.sot.start = mock.Mock(return_value={})
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._find = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.start_instance(self.sot)
        self.sot.start.assert_called_with(
            self.proxy,
        )
        self.proxy._get.assert_called_with(
            _instance.Instance,
            self.sot
        )

    def test_restart_instance(self):
        self.sot = _instance.Instance()
        self.sot.restart = mock.Mock(return_value={})
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._find = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.restart_instance(self.sot)
        self.sot.restart.assert_called_with(
            self.proxy,
        )
        self.proxy._get.assert_called_with(
            _instance.Instance,
            self.sot
        )

    def test_statistics(self):
        self.verify_list(
            self.proxy.statistics, _stat.Statistic,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
        )
