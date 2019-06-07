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

from otcextensions.sdk.auto_scaling.v1 import _proxy
from otcextensions.sdk.auto_scaling.v1 import activity as _activity
from otcextensions.sdk.auto_scaling.v1 import config as _config
from otcextensions.sdk.auto_scaling.v1 import group as _group
from otcextensions.sdk.auto_scaling.v1 import instance as _instance
from otcextensions.sdk.auto_scaling.v1 import policy as _policy
from otcextensions.sdk.auto_scaling.v1 import quota as _quota


class TestAutoScalingProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestAutoScalingProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestAutoScalingGroups(TestAutoScalingProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.groups, _group.Group,
            method_kwargs={
                'some_arg': 'arg_value',
            },
            expected_kwargs={
                'some_arg': 'arg_value',
            }
        )

    def test_get(self):
        self.verify_get(
            self.proxy.get_group,
            _group.Group,
            expected_kwargs={
            }
        )

    def test_find(self):
        self._verify2(
            'openstack.proxy.Proxy._find',
            self.proxy.find_group,
            method_args=["flavor"],
            expected_args=[_group.Group, "flavor"],
            expected_kwargs={
                "ignore_missing": True})

    def test_create(self):
        self.verify_create(
            self.proxy.create_group, _group.Group,
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
            expected_kwargs={
            }
        )

    def test_update(self):
        self._verify2(
            'openstack.proxy.Proxy._update',
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
            method_kwargs={
                'some_arg': 'arg_value',
            },
            expected_kwargs={
                'some_arg': 'arg_value',
            }
        )

    def test_get(self):
        self.verify_get(
            self.proxy.get_config,
            _config.Config,
            expected_kwargs={
            }
        )

    def test_find(self):
        self._verify2(
            'openstack.proxy.Proxy._find',
            self.proxy.find_config,
            method_args=["flavor"],
            expected_args=[_config.Config, "flavor"],
            expected_kwargs={
                "ignore_missing": True})

    def test_create(self):
        self.verify_create(
            self.proxy.create_config, _config.Config,
            method_kwargs={
                'instance_config': {},
                'name': 'some_name'
            },
            expected_kwargs={
                'prepend_key': False,
                'instance_config': {},
                'name': 'some_name'
            }
        )

    def test_delete(self):
        self.verify_delete(
            self.proxy.delete_config,
            _config.Config, True,
            expected_kwargs={
            }
        )


class TestAutoScalingPolicy(TestAutoScalingProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.policies, _policy.Policy,
            method_kwargs={
                'some_arg': 'arg_value',
                'group': 'group_id'
            },
            expected_kwargs={
                'some_arg': 'arg_value',
                'scaling_group_id': 'group_id',
            }
        )

    def test_delete(self):
        self.verify_delete(
            self.proxy.delete_policy,
            _policy.Policy, True,
            expected_kwargs={
            }
        )

    def test_create(self):
        self.verify_create(
            self.proxy.create_policy, _policy.Policy,
            method_kwargs={
                'name': 'some_name'
            },
            expected_kwargs={
                'prepend_key': False,
                'name': 'some_name'
            }
        )

    def test_find(self):
        self._verify2(
            'openstack.proxy.Proxy._find',
            self.proxy.find_policy,
            method_args=['pol'],
            expected_args=[_policy.Policy, 'pol'],
            expected_kwargs={
                'ignore_missing': True})

    def test_update(self):
        self._verify2(
            'openstack.proxy.Proxy._update',
            self.proxy.update_policy,
            method_args=['INSTANCE'],
            method_kwargs={'test': 't'},
            expected_args=[_policy.Policy, 'INSTANCE'],
            expected_kwargs={
                'test': 't',
                'prepend_key': False,
            }
        )

    def test_execute(self):
        self._verify2(
            'otcextensions.sdk.auto_scaling.v1.policy.Policy._action',
            self.proxy.execute_policy,
            method_args=['INSTANCE'],
            expected_args=[self.proxy, {'action': 'execute'}]
        )

    def test_resume(self):
        self._verify2(
            'otcextensions.sdk.auto_scaling.v1.policy.Policy._action',
            self.proxy.resume_policy,
            method_args=['INSTANCE'],
            expected_args=[self.proxy, {'action': 'resume'}]
        )

    def test_pause(self):
        self._verify2(
            'otcextensions.sdk.auto_scaling.v1.policy.Policy._action',
            self.proxy.pause_policy,
            method_args=['INSTANCE'],
            expected_args=[self.proxy, {'action': 'pause'}]
        )


class TestAutoScalingActivityLog(TestAutoScalingProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.activities, _activity.Activity,
            method_kwargs={
                'some_arg': 'arg_value',
                'group': 'group_id'
            },
            expected_kwargs={
                'some_arg': 'arg_value',
                'scaling_group_id': 'group_id',
            }
        )


class TestAutoScalingQuota(TestAutoScalingProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.quotas, _quota.Quota,
            expected_kwargs={
                'paginated': False
            }
        )

    def test_list_scaling(self):
        self.verify_list(
            self.proxy.quotas, _quota.ScalingQuota,
            method_args=['INSTANCE'],
            expected_kwargs={
                'paginated': False,
                'scaling_group_id': 'INSTANCE'
            }
        )


class TestAutoScalingInstance(TestAutoScalingProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.instances, _instance.Instance,
            method_args=['group'],
            expected_kwargs={
                'scaling_group_id': 'group'
            },
        )

    def test_batch_action_remove(self):
        self._verify2(
            'otcextensions.sdk.auto_scaling.v1.instance.Instance.batch_action',
            self.proxy.batch_instance_action,
            method_args=['INSTANCE', ['a1', 'a2'], 'REMOVE'],
            expected_args=[self.proxy, ['a1', 'a2'], 'REMOVE', False]
        )

    def test_batch_action_add(self):
        self._verify2(
            'otcextensions.sdk.auto_scaling.v1.instance.Instance.batch_action',
            self.proxy.batch_instance_action,
            method_args=['INSTANCE', ['a1', 'a2'], 'ADD'],
            expected_args=[self.proxy, ['a1', 'a2'], 'ADD', False]
        )

    def test_batch_action_protect(self):
        self._verify2(
            'otcextensions.sdk.auto_scaling.v1.instance.Instance.batch_action',
            self.proxy.batch_instance_action,
            method_args=['INSTANCE', ['a1', 'a2'], 'PROTECT'],
            expected_args=[self.proxy, ['a1', 'a2'], 'PROTECT', False]
        )

    def test_batch_action_unprotect(self):
        self._verify2(
            'otcextensions.sdk.auto_scaling.v1.instance.Instance.batch_action',
            self.proxy.batch_instance_action,
            method_args=['INSTANCE', ['a1', 'a2'], 'UNPROTECT'],
            expected_args=[self.proxy, ['a1', 'a2'], 'UNPROTECT', False]
        )

    def test_delete(self):
        self.verify_delete(
            self.proxy.remove_instance,
            _instance.Instance, True,
            mock_method='otcextensions.sdk.auto_scaling.v1.'
                        'instance.Instance.remove',
            expected_args=[self.proxy],
            expected_kwargs={
                'delete_instance': False
            }
        )
