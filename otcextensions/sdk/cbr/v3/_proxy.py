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
from openstack import proxy

from otcextensions.sdk.cbr.v3 import backup as _backup
from otcextensions.sdk.cbr.v3 import checkpoint as _checkpoint
from otcextensions.sdk.cbr.v3 import member as _member
from otcextensions.sdk.cbr.v3 import policy as _policy
from otcextensions.sdk.cbr.v3 import restore as _restore
from otcextensions.sdk.cbr.v3 import vault as _vault


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Backup ========
    def backups(self, **query):
        """Retrieve a generator of Backups

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `checkpoint_id`: Restore point ID
            * `dec`: Dedicated Cloud
            * `end_time`: Time when the backup ends
            * `image_type`: Backup type: backup or replication
            * `limit`: Number of records displayed per page
            * `marker`: ID of the last record displayed
            * `member_status`: Backup sharing status
            * `name`: Backup name
            * `offset`: Offset value
            * `parent_id`: Parent backup ID
            * `resource_az`: AZ-based filtering
            * `resource_id`: Resource ID
            * `resource_name`: Resource name
            * `resource_type`: Resource Type
            * `sort`: sorting
            * `start_time`: Time when the backup starts
            * `status`: Status
            * `vault_id`: Vault ID

        :returns: A generator of backup
            :class:`~otcextensions.sdk.cbr.v3.backup.Backup` instances
        """
        return self._list(_backup.Backup, **query)

    def get_backup(self, backup):
        """Get the backup by UUID.

        :param backup: key id or an instance of
            :class:`~otcextensions.sdk.cbr.v3.backup.Backup`

        :returns: instance of
            :class:`~otcextensions.sdk.cbr.v3.backup.Backup`
        """
        return self._get(
            _backup.Backup, backup
        )

    def find_backup(self, name_or_id, ignore_missing=True):
        """Find a single CBR backup by name or id

        :param name_or_id: The name or ID of a backup
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent group.

        :returns: ``None``
        """
        return self._find(
            _backup.Backup, name_or_id,
            ignore_missing=ignore_missing,
        )

    def delete_backup(self, backup, ignore_missing=True):
        """Delete a single CBR backup.

        :param backup: The value can be the ID of a backup
             or a :class:`~otcextensions.sdk.cbr.v3.backup.Backup`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent backup.
        """
        return self._delete(
            _backup.Backup, backup, ignore_missing=ignore_missing,
        )

    # ======== Checkpoint / Restore Point ========

    def get_checkpoint(self, checkpoint):
        """Get the checkpoint by UUID.

        :param checkpoint: key id or an instance of
            :class:`~otcextensions.sdk.cbr.v3.checkpoint.Checkpoint`

        :returns: instance of
            :class:`~otcextensions.sdk.cbr.v3.checkpoint.Checkpoint`
        """
        return self._get(
            _checkpoint.Checkpoint, checkpoint
        )

    def create_checkpoint(self, **attrs):
        """Creating a restore point / checkpoint using attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.cbr.v3.checkpoint.Checkpoint`,
            comprised of the properties on the Checkpoint class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.cbr.v3.checkpoint.Checkpoint`
        """
        return self._create(
            _checkpoint.Checkpoint,
            **attrs
        )

    # ======== Policy ========

    def policies(self, **query):
        """Retrieve a generator of CBR policies

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `operation_type`: Policy type: backup or replication
            * `vault_id`: Vault ID

        :returns: A generator of policies
            :class:`~otcextensions.sdk.cbr.v3.policy.Policy` instances
        """
        return self._list(_policy.Policy, **query)

    def get_policy(self, policy):
        """Get the CBR policy by UUID.

        :param policy: key id or an instance of
            :class:`~otcextensions.sdk.cbr.v3.policy.Policy`

        :returns: instance of
            :class:`~otcextensions.sdk.cbr.v3.policy.Policy`
        """
        return self._get(
            _policy.Policy, policy
        )

    def find_policy(self, name_or_id, ignore_missing=True):
        """Find a single CBR policy by name or ID

        :param name_or_id: The name or ID of a policy
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the policy does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent policy.

        :returns: a :class:`~otcextensions.sdk.cbr.v3.policy.Policy` instance
        """
        return self._find(_policy.Policy, name_or_id,
                          ignore_missing=ignore_missing)

    def create_policy(self, **attrs):
        """Creating a CBR policy using attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.cbr.v3.policy.Policy`,
            comprised of the properties on the Policy class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.cbr.v3.policy.Policy`
        """
        return self._create(
            _policy.Policy,
            **attrs
        )

    def update_policy(self, policy, **attrs):
        """Update CBR policy attributes

        :param policy: The id or an instance of
            :class:`~otcextensions.sdk.cbr.v3.policy.Policy`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.cbr.v3.policy.Policy`

        :rtype: :class:`~otcextensions.sdk.cbr.v3.policy.Policy`
        """
        return self._update(_policy.Policy, policy, **attrs)

    def delete_policy(self, policy, ignore_missing=True):
        """Delete a single CBR policy.

        :param policy: The value can be the ID of a policy
             or a :class:`~otcextensions.sdk.cbr.v3.policy.Policy`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent policy.
        """
        return self._delete(
            _policy.Policy, policy, ignore_missing=ignore_missing,
        )

    # ======== Restore ========
    def restore_data(self, backup, **attrs):
        """Restore data using a backup

        :param backup: The value can be the ID of a backup
             or a :class:`~otcextensions.sdk.cbr.v3.backup.Backup`
             instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.cbr.v3.restore.Restore`,
            comprised of the properties on the Restore class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.cbr.v3.restore.Restore`
        """
        backup = self._get_resource(_backup.Backup, backup)
        return self._create(
            _restore.Restore,
            backup_id=backup.id,
            **attrs
        )

    # ======== Vault ========
    def vaults(self, **query):
        """Retrieve a generator of Vaults

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `cloud_type`: Cloud type
            * `id`: Vault ID
            * `limit`: Number of records displayed per page, range: 1-100
            * `name`: Vault name
            * `object_type`: Resource type
            * `offset`: Offset value
            * `policy_id`: Policy ID
            * `protect_type`: Protection type
            * `resource_ids`: Resource IDs
            * `status`: Status

        :returns: A generator of vault
            :class:`~otcextensions.sdk.cbr.v3.vault.Vault` instances
        """
        return self._list(_vault.Vault, **query)

    def get_vault(self, vault):
        """Get the vault by UUID.

        :param vault: key id or an instance of
            :class:`~otcextensions.sdk.cbr.v3.vault.Vault`

        :returns: instance of
            :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
        """
        return self._get(
            _vault.Vault, vault
        )

    def find_vault(self, name_or_id, ignore_missing=True):
        """Find a single CBR vault by name or id

        :param name_or_id: The name or ID of a vault
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent vault.

        :returns: ``None``
        """
        return self._find(
            _vault.Vault, name_or_id,
            ignore_missing=ignore_missing,
        )

    def create_vault(self, **attrs):
        """Creating a CBR vault using attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.cbr.v3.vault.Vault`,
            comprised of the properties on the Vault class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
        """
        return self._create(
            _vault.Vault,
            **attrs
        )

    def update_vault(self, vault, **attrs):
        """Update CBR vault attributes

        :param vault: The id or an instance of
            :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.cbr.v3.vault.Vault`

        :rtype: :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
        """
        return self._update(_vault.Vault, vault, **attrs)

    def delete_vault(self, vault, ignore_missing=True):
        """Delete a single CBR vault.

        :param vault: The value can be the ID of a vault
             or a :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent vault.
        """
        return self._delete(
            _vault.Vault, vault, ignore_missing=ignore_missing,
        )

    def unbind_policy(self, vault, policy):
        """Disassociate policy from CBR vault

        :param vault: The value can be the ID of a vault
             or a :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
             instance.
        :param policy: The value can be the ID of a policy
             or a :class:`~otcextensions.sdk.cbr.v3.policy.Policy`
             instance.
        """
        vault = self._get_resource(_vault.Vault, vault)
        policy = self._get_resource(_policy.Policy, policy)
        return vault.unbind_policy(
            self,
            policy_id=policy.id)

    def bind_policy(self, vault, policy):
        """Associate policy to an existing CBR vault

        :param vault: The value can be the ID of a vault
             or a :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
             instance.
        :param policy: The value can be the ID of a policy
             or a :class:`~otcextensions.sdk.cbr.v3.policy.Policy`
             instance.
        """
        vault = self._get_resource(_vault.Vault, vault)
        policy = self._get_resource(_policy.Policy, policy)
        return vault.bind_policy(
            self,
            policy_id=policy.id)

    def associate_resources(self, vault, resources):
        """Associate resources to an existing CBR vault

        :param vault: The value can be the ID of a vault
             or a :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
             instance.
        :param resources: array of resources in the format: id and type
        """
        vault = self._get_resource(_vault.Vault, vault)
        return vault.associate_resources(
            self,
            resources)

    def dissociate_resources(self, vault, resources):
        """Associate resources to an existing CBR vault

        :param vault: The value can be the ID of a vault
             or a :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
             instance.
        :param resources: list of ressource ids to be released from vault
        """
        vault = self._get_resource(_vault.Vault, vault)
        return vault.dissociate_resources(
            self,
            resources)

    # ======== Share Member ========
    def members(self, backup, **query):
        """List share members for a backup

        :param backup: The value can be the ID of a backup
            or a :class:`~otcextensions.sdk.cbr.v3.backup.Backup`
            instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.cbr.v3.member.Member`,
            comprised of the properties on the Member class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.cbr.v3.member.Member`
        """
        backup = self._get_resource(_backup.Backup, backup)
        return self._list(
            _member.Member,
            backup_id=backup.id,
            **query
        )

    def get_member(self, backup, member):
        """Get one CBR share member by UUID.

        :param member: key id or an instance of
            :class:`~otcextensions.sdk.cbr.v3.member.Member`
        :param backup: The value can be the ID of a backup
            or a :class:`~otcextensions.sdk.cbr.v3.backup.Backup`
            instance.
        :returns: instance of
            :class:`~otcextensions.sdk.cbr.v3.member.Member`
        """
        backup = self._get_resource(_backup.Backup, backup)
        return self._get(
            _member.Member, member, backup_id=backup.id
        )

    def add_members(self, backup, members):
        """Add a list of share members to an existing backup

        :param backup: The value can be the ID of a backup
            or a :class:`~otcextensions.sdk.cbr.v3.backup.Backup`
            instance.
        :param list members: The list contains the project IDs of the backup
            share members to be added
        :returns: The results are the list of share member objects
        """
        backup = self._get_resource(_backup.Backup, backup)
        return backup.add_members(
            self,
            members=members
        )

    def update_member(self, backup, member, status='accepted', vault=None):
        """Update CBR share members

        :param member: The id or an instance of
            :class:`~otcextensions.sdk.cbr.v3.member.Member`
        :param backup: The value can be the ID of a backup
            or a :class:`~otcextensions.sdk.cbr.v3.backup.Backup`
            instance.
        :param str status: status to be updated share member
        :param vault: The value can be the ID of a vault
             or a :class:`~otcextensions.sdk.cbr.v3.vault.Vault`
             instance.
        """
        backup = self._get_resource(_backup.Backup, backup)
        vault = self._get_resource(_vault.Vault, vault)
        return self._update(
            _member.Member, member, backup_id=backup.id,
            status=status, vault_id=vault.id)

    def delete_member(self, backup, member, ignore_missing=True):
        """Delete a single CBR share member.

        :param member: The id or an instance of
            :class:`~otcextensions.sdk.cbr.v3.member.Member`
        :param backup: The value can be the ID of a backup
            or a :class:`~otcextensions.sdk.cbr.v3.backup.Backup`
            instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the share member does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent share member.
        """
        backup = self._get_resource(_backup.Backup, backup)
        return self._delete(
            _member.Member, member, backup_id=backup.id,
            ignore_missing=ignore_missing,
        )
