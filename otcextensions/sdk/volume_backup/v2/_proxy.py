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
from openstack import resource

from otcextensions.sdk import sdk_proxy
from otcextensions.sdk.volume_backup.v2 import backup as _backup
from otcextensions.sdk.volume_backup.v2 import backup_policy as _backup_policy
from otcextensions.sdk.volume_backup.v2 import backup_task as _backup_task
from otcextensions.sdk.volume_backup.v2 import job as _job


class Proxy(sdk_proxy.Proxy):

    # ======== Backup ========
    def backups(self, details=False, **query):
        """Retrieve a generator of backups

        :param bool details: When ``True``, returns
            :class:`~otcextensions.sdk.volume_backup.v2.backup.BackupDetail`
            objects, otherwise
            :class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`.
            *Default: ``False``*
        :param dict query: Optional query parameters to be sent to limit the
            resources being returned:
            * ``name``: backup name
            * ``status``: backup status :
            ``available``, ``error``, ``restoring``, ``creating``,
            ``deleting``, ``error_restoring``
            * ``volume_id``: backup of volume
            * ``offset``:  pagination marker
            * ``limit``: pagination limit

        :returns: A generator of backup
            (:class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`)
            instances
        """
        return self._list(
            _backup.Backup,
            paginated=True,
            details=details,
            **query)

    def get_backup(self, backup):
        """Get a backup

        :param backup: The value can be the ID of a backup
            or a :class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`
            instance.
        :returns: Backup instance
        :rtype: :class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`
        """
        return self._get(_backup.Backup, backup)

    def create_backup(self, **attrs):
        """Create a new Backup from attributes with native API

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`
            comprised of the properties on the Backup class.
        :returns: The results of Backup creation
        :rtype: :class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`
        """
        return self._create(_backup.Backup, **attrs)

    def delete_backup(self, backup, ignore_missing=True):
        """Delete a CloudBackup

        :param backup: The value can be the ID of a backup or a :class:`
            ~otcextensions.sdk.volume_backup.v2.backup.Backup` instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the zone does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent zone.

        :returns: rsync job
        :rtype: :class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`
        """
        return self._delete(_backup.Backup,
                            backup,
                            ignore_missing=ignore_missing)

    def restore_backup(self, backup, volume_id):
        """Restore a Backup to volume

        :param backup: The value can be the ID of a zone or a :class:`
            ~otcextensions.sdk.volume_backup.v2.backup.Backup` instance
        :param volume_id: the volume to restore to
        :returns: A sync Job of restore backup
        :rtype: :class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`
        """
        backup = self._get_resource(_backup.Backup, backup)
        return backup.restore(self, volume_id)

    def wait_for_backup(self, backup, status='available', failures=['error'],
                        interval=2, wait=120):
        """Wait for the backup appear with the asked status

        :param backup: The value can be the ID of a backup or a :class:`
            ~otcextensions.sdk.volume_backup.v2.backup.Backup` instance
        :param status: requested Status to be waited for.
        :param failures: status of failure
        :param interval: interval for a check
        :param wait: maximal time in secods to wait for the backup

        :returns: Backup object
        :rtype: :class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`
        """
        return resource.wait_for_status(
            self, backup, status, failures, interval, wait)

    def wait_for_backup_delete(self, backup, interval=2, wait=120):
        """Wait for the backup be deleted

        :param backup: The value can be the ID of a backup or a :class:`
            ~otcextensions.sdk.volume_backup.v2.backup.Backup` instance
        :param interval: interval for a check
        :param wait: maximal time in secods to wait for the backup

        :returns: Backup object
        :rtype: :class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`
        """
        return resource.wait_for_delete(
            self, backup, interval, wait)

    # ======== Backup Policy ========
    def backup_policies(self):
        """Retrieve a generator of backup_policys

        :returns: A generator of backup_policy (:class:`~openstack.
            volume_backup.v2.backup_policy.BackupPolicy`) instances
        """
        return self._list(_backup_policy.BackupPolicy, paginated=False)

    def create_backup_policy(self, **attrs):
        """Create a new backup policy from name and scheduled policy attributes

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`

        :returns: The results of backup policy creation
        :rtype:
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
        """
        return self._create(_backup_policy.BackupPolicy, **attrs)
        # scheduled_policy = _backup_policy.SchedulePolicy.new(**attrs)
        # backup_policy = _backup_policy.BackupPolicy(
        #     name=name, scheduled_policy=scheduled_policy)
        # return backup_policy.create(self, prepend_key=False)

    def update_backup_policy(self, backup_policy, **attrs):
        """update a backup_policy from backup policy attributes

        :param backup_policy: The value can be the ID of a backup_policy or a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
            instance
        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.ScheduledPolicy`,
            comprised of the properties on the SchedulePolicy class.

        :returns: The results of backup_policy creation
        :rtype:
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
        """
        return self._update(_backup_policy.BackupPolicy,
                            backup_policy,
                            prepend_key=False,
                            **attrs)

    def delete_backup_policy(self, backup_policy, ignore_missing=True):
        """Delete a backup policy

        :param backup_policy: The value can be the ID of a backup_policy or a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
            instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the backup_policy does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent backup_policy.

        :returns: backup_policy been deleted
        :rtype:
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
        """
        return self._delete(_backup_policy.BackupPolicy,
                            backup_policy,
                            ignore_missing=ignore_missing)

    def find_backup_policy(self, name_or_id, ignore_missing=True):
        """Find a single backup_policy

        :param name_or_id: The name or ID of a backup_policy
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the backup_policy does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent backup_policy.

        :returns: ``None``
        """
        if isinstance(name_or_id, _backup_policy.BackupPolicy):
            name_or_id = name_or_id.id
        return self._find(_backup_policy.BackupPolicy, name_or_id,
                          ignore_missing=ignore_missing)

    def execute_policy(self, backup_policy):
        """Execute policy immediately

        ::param backup_policy: The value can be the ID of a backup_policy or a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
            instance
        """
        backup_policy = self._get_resource(_backup_policy.BackupPolicy,
                                           backup_policy)
        return backup_policy.execute(self)

    def enable_policy(self, backup_policy):
        """Enable policy

        ::param backup_policy: The value can be the ID of a backup_policy or a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
            instance
        """
        updated = {
            "scheduled_policy": {
                "status": "ON"
            }
        }
        return self.update_backup_policy(backup_policy, **updated)

    def disable_policy(self, backup_policy):
        """disable policy

        ::param backup_policy: The value can be the ID of a backup_policy or a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
            instance
        """
        updated = {
            "scheduled_policy": {
                "status": "OFF"
            }
        }
        return self.update_backup_policy(backup_policy, **updated)

    def link_resources_to_policy(self, backup_policy, resources):
        """link resource to backup policy

        :param backup_policy: The value can be the ID of a backup_policy or a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
            instance
        :param resources: resources to bound, should be a list of volume id
        :rtype: :class:`~otcextensions.sdk.volume_backup.v2.backup_policy
                    .BackupPolicyResource`
        """
        backup_policy = self._get_resource(_backup_policy.BackupPolicy,
                                           backup_policy)
        policy_resource = _backup_policy.BackupPolicyResource()
        return policy_resource.link(self,
                                    backup_policy.id,
                                    resources)

    def unlink_resources_of_policy(self, backup_policy, resources):
        """Unlink resources of backup policy

        :param backup_policy: The value can be the ID of a backup_policy or a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
            instance
        :param resources: resources to bound, should be a list of volume id
        :rtype: :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.
                        BackupPolicyResource`
        """
        backup_policy = self._get_resource(_backup_policy.BackupPolicy,
                                           backup_policy)
        policy_resource = _backup_policy.BackupPolicyResource()
        return policy_resource.unlink(self,
                                      backup_policy.id,
                                      resources)

    # ======== Misc ========
    def tasks(self, backup_policy, **query):
        """Retrieve a generator of tasks

        :param backup_policy: The value can be the ID of a backup_policy or a
            :class:`~otcextensions.sdk.volume_backup.v2.backup_policy.BackupPolicy`
            instance
        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
                * ``id``: task id
                * ``job_id``: alternate to id
                * ``status``: includes:``RUNNING``, ``EXECUTE_TIMEOUT``,
                        ``WAITING``, EXECUTE_FAIL``, ``EXECUTE_SUCCESS``
                * ``sort_dir``: ``desc``, ``asc``
                * ``sort_key``: only ``created_at`` support for now
                * ``marker``:  pagination marker
                * ``limit``: pagination limit
                * ``offset``: pagination offset

        :returns: A generator of backup
            (:class:`~otcextensions.sdk.volume_backup.v2.backup.Backup`)
            instances
        """
        backup_policy = self._get_resource(_backup_policy.BackupPolicy,
                                           backup_policy)
        query["policy_id"] = backup_policy.id
        return self._list(_backup_task.BackupTask, paginated=False, **query)

    def get_job(self, job):
        """Get a job detail

        :param job: The value can be the ID of a job
             or a :class:`~otcextensions.sdk.volume_backup.v1.job.Job`
             instance.
        :returns: Backup instance
        :rtype: :class:`~otcextensions.sdk.volume_backup.v1.job.Job`
        """
        return self._get(_job.Job, job)
