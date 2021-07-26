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

from otcextensions.sdk.volume_backup.v2 import _proxy
from otcextensions.sdk.volume_backup.v2 import backup_policy as _backup_policy
from otcextensions.sdk.volume_backup.v2 import backup_task as _backup_task
from otcextensions.sdk.volume_backup.v2 import job as _job


class TestVolumeBackupProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestVolumeBackupProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestBackupPolicy(TestVolumeBackupProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.backup_policies, _backup_policy.BackupPolicy,
            mock_method='openstack.proxy.Proxy._list',
            method_kwargs={
            },
            expected_kwargs={
                'paginated': False,
            }
        )

    def test_find(self):
        self.verify_find(
            self.proxy.find_backup_policy,
            _backup_policy.BackupPolicy,
            mock_method='openstack.proxy.Proxy._find',
        )

    def test_create(self):
        self.verify_create(
            self.proxy.create_backup_policy, _backup_policy.BackupPolicy,
            mock_method='openstack.proxy.Proxy._create',
            method_kwargs={
                'name': 'some_name'
            },
            expected_kwargs={
                'name': 'some_name'
            }
        )

    def test_delete(self):
        self.verify_delete(
            self.proxy.delete_backup_policy,
            _backup_policy.BackupPolicy, True,
            mock_method='openstack.proxy.Proxy._delete',
            expected_kwargs={
            }
        )

    def test_update(self):
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.update_backup_policy,
            method_args=['INSTANCE'],
            method_kwargs={'test': 't'},
            expected_args=[_backup_policy.BackupPolicy, 'INSTANCE'],
            expected_kwargs={
                'test': 't',
                'prepend_key': False,
            }
        )

    def test_execute_policy(self):
        self._verify(
            'otcextensions.sdk.volume_backup.v2.backup_policy.'
            'BackupPolicy.execute',
            self.proxy.execute_policy,
            method_args=['INSTANCE'],
            expected_args=[self.proxy],
        )

    def test_enable_policy(self):
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.enable_policy,
            method_args=['INSTANCE'],
            expected_args=[_backup_policy.BackupPolicy, 'INSTANCE'],
            expected_kwargs={
                'prepend_key': False,
                'scheduled_policy': {'status': 'ON'}
            }
        )

    def test_disable_policy(self):
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.disable_policy,
            method_args=['INSTANCE'],
            expected_args=[_backup_policy.BackupPolicy, 'INSTANCE'],
            expected_kwargs={
                'prepend_key': False,
                'scheduled_policy': {'status': 'OFF'}
            }
        )


class TestBackupPolicyResource(TestVolumeBackupProxy):
    def test_link(self):
        self._verify(
            'otcextensions.sdk.volume_backup.v2.backup_policy.'
            'BackupPolicyResource._process',
            self.proxy.link_resources_to_policy,
            method_args=['policy', ['r1', 'r2']],
            expected_args=[
                self.proxy,
                'policy',
                True,
                ['r1', 'r2']],
            expected_kwargs={
            }
        )

    def test_unlink(self):
        self._verify(
            'otcextensions.sdk.volume_backup.v2.backup_policy.'
            'BackupPolicyResource._process',
            self.proxy.unlink_resources_of_policy,
            method_args=['policy', ['r1', 'r2']],
            expected_args=[
                self.proxy,
                'policy',
                False,
                ['r1', 'r2']],
            expected_kwargs={
            }
        )


class TestTask(TestVolumeBackupProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.tasks, _backup_task.BackupTask,
            mock_method='openstack.proxy.Proxy._list',
            method_args=['pol_id'],
            expected_kwargs={
                'paginated': False,
                'policy_id': 'pol_id'
            }
        )


class TestJob(TestVolumeBackupProxy):

    def test_get(self):
        self.verify_get(
            self.proxy.get_job,
            _job.Job,
            mock_method='openstack.proxy.Proxy._get',
            expected_kwargs={
            }
        )
