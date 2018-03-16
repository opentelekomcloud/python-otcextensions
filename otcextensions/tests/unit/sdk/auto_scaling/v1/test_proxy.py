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
# import mock

# from otcextensions.sdk.auto_scaling import auto_scaling_service
from otcextensions.sdk.auto_scaling.v1 import _proxy
# from openstack.auto_scaling.v1 import activity as _activity_log
# from openstack.auto_scaling.v1 import config as _config
from otcextensions.sdk.auto_scaling.v1 import group as _group
from otcextensions.sdk.auto_scaling.v1 import config as _config
# from openstack.auto_scaling.v1 import instance as _instance
# from openstack.auto_scaling.v1 import policy as _policy
# from openstack.auto_scaling.v1 import quota as _quota
# from openstack.tests.unit.test_proxy_base3 import BaseProxyTestCase
from openstack.tests.unit import test_proxy_base


class TestAutoScalingProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestAutoScalingProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        # self.session.get_project_id = mock.Mock(return_value=PROJECT_ID)


class TestAutoScalingGroups(TestAutoScalingProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.groups, _group.Group,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'some_arg': 'arg_value',
            },
            paginated=True,
            expected_kwargs={
                'some_arg': 'arg_value',
            }
        )

    def test_get(self):
        self.verify_get(
            self.proxy.get_group,
            _group.Group,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={
            }
        )

    def test_find(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._find',
            self.proxy.find_group,
            method_args=["flavor"],
            expected_args=[_group.Group, "flavor"],
            expected_kwargs={
                "ignore_missing": True})

    def test_create(self):
        self.verify_create(
            self.proxy.create_group, _group.Group,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_kwargs={
                'instance': 'test',
                'name': 'some_name'
            },
            expected_kwargs={
                'prepend_key': False,
                'instance': 'test',
                'name': 'some_name'
            }
        )

    def test_delete(self):
        self.verify_delete(
            self.proxy.delete_group,
            _group.Group, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={
            }
        )

    def test_update(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._update',
            self.proxy.update_group,
            method_args=['INSTANCE'],
            method_kwargs={'test': 't'},
            expected_args=[_group.Group, 'INSTANCE'],
            expected_kwargs={
                'test': 't',
                'prepend_key': False,
            }
        )


class TestAutoScalingConfigs(TestAutoScalingProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.configs, _config.Config,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'some_arg': 'arg_value',
            },
            paginated=True,
            expected_kwargs={
                'some_arg': 'arg_value',
            }
        )

    def test_get(self):
        self.verify_get(
            self.proxy.get_config,
            _config.Config,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={
            }
        )

    def test_find(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._find',
            self.proxy.find_config,
            method_args=["flavor"],
            expected_args=[_config.Config, "flavor"],
            expected_kwargs={
                "ignore_missing": True})

    def test_create(self):
        self.verify_create(
            self.proxy.create_config, _config.Config,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_kwargs={
                'instance': 'test',
                'name': 'some_name'
            },
            expected_kwargs={
                'prepend_key': False,
                'instance_config': _config.InstanceConfig(),
                'name': 'some_name'
            }
        )

    def test_delete(self):
        self.verify_delete(
            self.proxy.delete_config,
            _config.Config, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={
            }
        )

    # def test_update(self):
    #     self._verify2(
    #         'otcextensions.sdk.sdk_proxy.Proxy._update',
    #         self.proxy.update_config,
    #         method_args=['INSTANCE'],
    #         method_kwargs={'test': 't'},
    #         expected_args=[_config.Config, 'INSTANCE'],
    #         expected_kwargs={
    #             'test': 't',
    #             'prepend_key': False,
    #         }
    #     )
