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
from otcextensions.sdk.cbr.v3 import restore as _restore


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
            * `enterprise_project_id`: Enterprise project ID
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
            :class:`~otcextensions.sdk.cbr.v3.backup.backup`

        :returns: instance of
            :class:`~otcextensions.sdk.cbr.v3.backup.backup`
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
             or a :class:`~otcextensions.sdk.cbr.v3.backup.backup`
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

        :param backup: The value can be the ID of a backup
             or a :class:`~otcextensions.sdk.cbr.v3.backup.Backup`
             instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.cbr.v3.restore.Restore`,
            comprised of the properties on the Restore class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.cbr.v3.restore.Restore`
        """
        return self._create(
            _checkpoint.Checkpoint,
            **attrs
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
            backup=backup.id,
            **attrs
        )
