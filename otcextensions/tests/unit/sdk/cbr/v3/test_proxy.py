#!/usr/bin/env python3
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

from otcextensions.sdk.cbr.v3 import _proxy
from otcextensions.sdk.cbr.v3 import backup as _backup
from otcextensions.sdk.cbr.v3 import member as _member
from otcextensions.sdk.cbr.v3 import policy as _policy
from otcextensions.sdk.cbr.v3 import checkpoint as _checkpoint
from otcextensions.sdk.cbr.v3 import restore as _restore
from otcextensions.sdk.cbr.v3 import vault as _vault


class TestCBRProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestCBRProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestCBRBackup(TestCBRProxy):

    def test_backups(self):
        self.verify_list(self.proxy.backups, _backup.Backup)

    def test_backup_delete(self):
        self.verify_delete(self.proxy.delete_backup,
                           _backup.Backup, True)

    def test_backup_find(self):
        self.verify_find(self.proxy.find_backup, _backup.Backup)

    def test_backup_get(self):
        self.verify_get(self.proxy.get_backup, _backup.Backup)

    def test_member_add(self):
        members = ['member1', 'member2']
        backup = _backup.Backup(id='backup')
        self._verify2(
            'otcextensions.sdk.cbr.v3.backup.Backup.add_members',
            self.proxy.add_members,
            method_args=[backup, members],
            expected_args=[self.proxy],
            expected_kwargs={'members': members}
        )


class TestCBRPolicy(TestCBRProxy):

    def test_policies(self):
        self.verify_list(self.proxy.policies, _policy.Policy)

    def test_policy_find(self):
        self.verify_find(self.proxy.find_policy, _policy.Policy)

    def test_policy_get(self):
        self.verify_get(self.proxy.get_policy, _policy.Policy)

    def test_policy_create(self):
        self.verify_create(self.proxy.create_policy,
                           _policy.Policy,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_policy_delete(self):
        self.verify_delete(self.proxy.delete_policy,
                           _policy.Policy, True)


class TestCBRCheckpoint(TestCBRProxy):

    def test_checkpoint_get(self):
        self.verify_get(self.proxy.get_checkpoint, _checkpoint.Checkpoint)

    def test_checkpoint_create(self):
        self.verify_create(self.proxy.create_checkpoint,
                           _checkpoint.Checkpoint,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})


class TestCBRRestore(TestCBRProxy):

    def test_restore_server(self):
        attrs = {'a': 'b'}
        backup = _backup.Backup(id='my_backup')
        self._verify2(
            'openstack.proxy.Proxy._create',
            self.proxy.restore_data,
            method_args=[backup],
            method_kwargs=attrs,
            expected_args=[_restore.Restore],
            expected_kwargs=dict(
                backup_id=backup.id,
                **attrs
            )
        )


class TestCBRVault(TestCBRProxy):

    def test_vaults(self):
        self.verify_list(self.proxy.vaults, _vault.Vault)

    def test_vault_find(self):
        self.verify_find(self.proxy.find_vault, _vault.Vault)

    def test_vault_get(self):
        self.verify_get(self.proxy.get_vault, _vault.Vault)

    def test_vault_create(self):
        self.verify_create(self.proxy.create_vault,
                           _vault.Vault,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_vault_delete(self):
        self.verify_delete(self.proxy.delete_vault,
                           _vault.Vault, True)

    def test_bind_policy(self):
        vault = _vault.Vault(id='vault')
        policy = _policy.Policy(id='policy')
        self._verify2(
            'otcextensions.sdk.cbr.v3.vault.Vault.bind_policy',
            self.proxy.bind_policy,
            method_args=[vault, policy],
            expected_args=[self.proxy],
            expected_kwargs={'policy_id': 'policy'}
        )

    def test_unbind_policy(self):
        vault = _vault.Vault(id='vault')
        policy = _policy.Policy(id='policy')
        self._verify2(
            'otcextensions.sdk.cbr.v3.vault.Vault.unbind_policy',
            self.proxy.unbind_policy,
            method_args=[vault, policy],
            expected_args=[self.proxy],
            expected_kwargs={'policy_id': 'policy'}
        )

    def test_associate_resources(self):
        vault = _vault.Vault(id='vault')
        resources = 'resources'
        self._verify2(
            'otcextensions.sdk.cbr.v3.vault.Vault.associate_resources',
            self.proxy.associate_resources,
            method_args=[vault, resources],
            expected_args=[self.proxy, resources],
        )

    def test_dissociate_resources(self):
        vault = _vault.Vault(id='vault')
        resources = 'resources'
        self._verify2(
            'otcextensions.sdk.cbr.v3.vault.Vault.dissociate_resources',
            self.proxy.dissociate_resources,
            method_args=[vault, resources],
            expected_args=[self.proxy, resources],
        )


class TestCBRMember(TestCBRProxy):

    def test_list(self):
        backup = _backup.Backup(id='backup')
        self.verify_list(
            self.proxy.members,
            _member.Member,
            method_args=[backup],
            expected_kwargs={'backup_id': backup.id}
        )

    def test_get(self):
        backup = _backup.Backup(id='backup')
        member = _member.Member(id='member')
        self._verify2(
            'openstack.proxy.Proxy._get',
            self.proxy.get_member,
            method_args=[backup, member],
            method_kwargs={},
            expected_args=[_member.Member, member],
            expected_kwargs={'backup_id': backup.id}
        )

    def test_delete(self):
        backup = _backup.Backup(id='backup')
        member = _member.Member(id='member')
        self._verify2(
            'openstack.proxy.Proxy._delete',
            self.proxy.delete_member,
            method_args=[backup, member, True],
            method_kwargs={},
            expected_args=[_member.Member, member],
            expected_kwargs={
                'backup_id': backup.id,
                'ignore_missing': True}
        )

    def test_update(self):
        backup = _backup.Backup(id='backup')
        member = _member.Member(id='member')
        status = 'accepted'
        vault = _vault.Vault(id='vault')
        self._verify2(
            'openstack.proxy.Proxy._update',
            self.proxy.update_member,
            method_args=[backup, member, status, vault],
            method_kwargs={},
            expected_args=[_member.Member, member],
            expected_kwargs={
                'backup_id': backup.id,
                'status': status,
                'vault_id': vault.id}
        )
