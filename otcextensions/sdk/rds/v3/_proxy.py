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
from openstack import resource

from otcextensions.sdk import job
from otcextensions.sdk.rds.v3 import backup as _backup
from otcextensions.sdk.rds.v3 import configuration as _configuration
from otcextensions.sdk.rds.v3 import datastore as _datastore
from otcextensions.sdk.rds.v3 import flavor as _flavor
from otcextensions.sdk.rds.v3 import instance as _instance


class Proxy(proxy.Proxy, job.JobProxyMixin):

    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            'Content-Type': 'application/json',
            'X-Language': 'en-us'
        }

    # ======= Datastores =======
    def datastore_types(self):
        """List supported datastore types

        :returns: A generator of supported datastore type objects
            with name attribute.
        """
        for ds in ['MySQL', 'PostgreSQL', 'SQLServer']:
            obj = type('obj', (object, ), {'name': ds})
            yield obj

    def datastores(self, database_name):
        """List datastores

        :param database_name: database store name
            (MySQL, PostgreSQL, or SQLServer and is case-sensitive.)

        :returns: A generator of supported datastore versions.

        :rtype: :class:`~otcextensions.sdk.rds.v3.datastore.Datastore`
        """
        return self._list(
            _datastore.Datastore,
            database_name=database_name,
        )

    # ======= Flavors =======

    def flavors(self, datastore_name, version_name):
        """List flavors of given datastore_name and datastore_version

        :param datastore_name: datastore_name
        :param version_name: version_name

        :returns: A generator of flavor objects.
        """
        return self._list(_flavor.Flavor,
                          datastore_name=datastore_name,
                          version_name=version_name)

    # ======= Instance =======

    def create_instance(self, **attrs):
        """Create a new instance from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.rds.v3.instance.Instance`,
            comprised of the properties on the Instance class.

        :returns: The result of an instance creation.

        :rtype: :class:`~otcextensions.sdk.rds.v3.instance.Instance`
        """
        return self._create(_instance.Instance, **attrs)

    def delete_instance(self, instance, ignore_missing=True):
        """Delete an instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.rds.v3.instance.Instance` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the instance does not exist.
            When set to ``True``, no exception will be set when
            attempting to delete a nonexistent instance.

        :returns: ``None``
        """
        return self._delete(
            _instance.Instance,
            instance,
            ignore_missing=ignore_missing,
        )

    def get_instance(self, instance):
        """Get a single instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.rds.v3.instance.Instance` instance.

        :returns: One :class:`~otcextensions.sdk.rds.v3.instance.Instance`
        """
        return self._get(_instance.Instance, instance)

    def find_instance(self, name_or_id, ignore_missing=True):
        """Find a single instance

        :param name_or_id: The name or ID of a instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the resource does not exist.
            When set to ``True``, None will be returned when
            attempting to find a nonexistent resource.

        :returns:
            One :class:`~otcextensions.sdk.rds.v3.instance.Instance` or None.
        """
        return self._find(_instance.Instance,
                          name_or_id,
                          ignore_missing=ignore_missing)

    def instances(self, **params):
        """Return a generator of instances

        :param dict params: Optional query parameters to be sent to limit
            the instances being returned.

        :returns: A generator of instance objects.
        """
        return self._list(_instance.Instance, **params)

    def restore_instance(self,
                         instance,
                         backup=None,
                         restore_time=None):
        """Restore instance from backup or Restore using Point in
            Time Recovery

        :param instance: Either the id of a source target instance or a
            :class:`~otcextensions.sdk.rds.v3.instance.Instance` instance.
        :param backup: Either the id of a backup or a
            :class:`~otcextensions.sdk.rds.v3.backup.Backup` instance.

        :returns: Job ID
        """
        instance = self._get_resource(_instance.Instance, instance)
        if backup:
            backup = self._get_resource(_backup.Backup, backup)
        return instance.restore(self, backup, restore_time)

    def get_instance_restore_time(self, instance):
        """Obtaining a restore time of an instance.

        :param instance: This parameter can be either the ID of an instance
            or a :class:`~openstack.sdk.rds.v3.instance.Instance`

        :returns: Instance restore time

        :rtype: list

        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.fetch_restore_times(self)

    def get_instance_backup_policy(self, instance):
        """Obtaining a backup policy of the instance

        :param instance: This parameter can be either the ID of an instance
            or a :class:`~openstack.sdk.rds.v3.instance.Instance`

        :returns: Instance Backup policy.

        :rtype: :class:`~otcextensions.sdk.rds.v3.instance.BackupPolicy`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.get_backup_policy(self)

    def set_instance_backup_policy(self, instance, keep_days,
                                   start_time=None, period=None):
        """Sets the backup policy of the instance

        :param instance: This parameter can be either the ID of an instance
            or a :class:`~openstack.sdk.rds.v3.instance.Instance`
        :param keep_days:
        :param start_time:
        :param period:

        :returns: ``None``
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.set_backup_policy(self, keep_days=keep_days,
                                          start_time=start_time, period=period)

#     def get_instance_configuration(self, instance):
#         """Obtaining a Configuration associated to instance.
#
#         :param instance: This parameter can be either the ID of an instance
#             or a :class:`~openstack.sdk.rds.v3.instance.Instance`
#         :returns: Configuration Group details associated to instance
#         :rtype: :class:
#             `~otcextensions.sdk.rds.v3.instance.InstanceConfiguration`
#
#         """
#         instance = self._get_resource(instance)
#         return self._get(_instance.InstanceConfiguration,
#                          requires_id=False,
#                          instance_id=instance.id)
#
#     def update_instance_configuration(self, instance, **attrs):
#         """Updates the configuration params of the instance.
#
#         :param instance: This parameter can be either the ID of an instance
#             or a :class:`~openstack.sdk.rds.v3.instance.Instance`
#
#         :returns: Parameter restart required as bool value
#         """
#         instance = self._get_resource(_instance.Instance, instance)
#         return self._update(_instance.InstanceConfiguration,
#                             instance_id=instance.id,
#                             **attrs)
#
    # ======= Configurations =======
    def configurations(self, **params):
        """Obtaining a list of DB Configuration.

        :param dict params: Optional query parameters to be sent to limit
            the configurations being returned.

        :returns: A generator of Configuration objects.
        """
        return self._list(
            _configuration.Configuration,
            paginated=False
        )

    def get_configuration(self, cg):
        """Obtaining a Configuration.

        :param parameter_group: The value can be the ID of a Configuration or
            a :class:`~otcextensions.sdk.rds.v3.configuration.Configuration`
            instance.

        :returns:
            One :class:`~otcextensions.rds.v3.configuration.Configuration`
        """
        return self._get(_configuration.Configuration, cg)

    def find_configuration(self, name_or_id, ignore_missing=True):
        """Find Configuration by name or id.

        :param name_or_id: The name or ID of configuration.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the resource does not exist.
            When set to ``True``, None will be returned when
            attempting to find a nonexistent resource.

        :returns: A configuration object.

        :rtype: :class:`~otcextensions.sdk.rds.v3.configuration.Configuration`
        """
        return self._find(_configuration.Configuration,
                          name_or_id,
                          ignore_missing=ignore_missing)

    def create_configuration(self, **attrs):
        """Create DB Configuration.

        :param dict attrs: Dict to overwrite Configuration object

        :returns: A Configuration object.

        :rtype:
            :class:`~otcextensions.sdk.rds.v3.configuration.Configuration`
        """
        return self._create(_configuration.Configuration,
                            prepend_key=False,
                            **attrs)

    def delete_configuration(self, cg, ignore_missing=True):
        """Delete DB Configuration.

        :param cg: The value can be the ID of a Configuration or a
            object of
            :class:`~otcextensions.sdk.rds.v3.configuration.Configuration`.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the Configration does not exist.
            When set to ``True``, no exception will be set when
            attempting to delete a nonexistent Configuration.

        :returns: ``None``
        """
        self._delete(
            _configuration.Configuration,
            cg,
            ignore_missing=ignore_missing,
        )

    def update_configuration(self, config, **attrs):
        """Sets the configuration properties

        :param config: This parameter can be either the ID of a configuration
            or a :class:`~openstack.sdk.rds.v3.config.Configuration`
        :param dict attrs: The attributes to update on the configuration.

        :returns: ``None``
        """
        return self._update(_configuration.Configuration, config,
                            **attrs)

    def apply_configuration(self, configuration, instances):
        """Apply configuration to instances.

        :param configuration: The value can be the ID of a Configuration
            or a object of
            :class:`~otcextensions.sdk.rds.v3.configuration.Configuration`.
        :param instances: List of instance ids the configuration should be
            applied to

        :returns: Updated Configuration object.

        :rtype:
            :class:`~otcextensions.rds.v3.configuration.Configuration`.
        """
        cg = self._get_resource(_configuration.Configuration,
                                configuration)
        return cg.apply(self, instances)

    # ======= Backups =======
    def backups(self, instance, **params):
        """List Backups.

        :param instance: This parameter can be either the ID of an instance
            or a :class:`~openstack.sdk.rds.v3.instance.Instance`
        :param dict params: Optional query parameters to be sent to limit
            the instance backups being returned.

        :returns: A generator of backup objects.
        """
        instance = self._get_resource(_instance.Instance, instance)
        return self._list(_backup.Backup, instance_id=instance.id, **params)

    def create_backup(self, instance, **attrs):
        """Create a backups of instance

        :param instance: This parameter can be either the ID of an instance
            or a :class:`~openstack.sdk.rds.v3.instance.Instance`

        :returns: A new backup object.

        :rtype: :class:`~otcextensions.sdk.rds.v3.backup.Backup`
        """
        instance = self._get_resource(_instance.Instance, instance)
        attrs.update({'instance_id': instance.id})
        return self._create(_backup.Backup, **attrs)

    def delete_backup(self, backup, ignore_missing=True):
        """Deletes given backup

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextension.sdk.rds.v3.instance.Instance` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the instance does not exist.
            When set to ``True``, no exception will be set when
            attempting to delete a nonexistent instance.

        :returns: ``None``
        """
        return self._delete(_backup.Backup,
                            backup,
                            ignore_missing=ignore_missing)

    def find_backup(self, name_or_id, instance, ignore_missing=True):
        """Find a single backup

        :param name_or_id: The name or ID of a instance.
        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextension.sdk.rds.v3.instance.Instance` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the resource does not exist.
            When set to ``True``, None will be returned when
            attempting to find a nonexistent resource.

        :returns: One :class:`~otcextensions.sdk.rds.v3.backup.Backup`
            or None
        """
        instance = self._get_resource(_instance.Instance, instance)
        return self._find(_backup.Backup,
                          name_or_id,
                          ignore_missing=ignore_missing,
                          instance_id=instance.id)

    def backup_download_links(self, backup_id):
        """Obtaining a backup file download links.

        :param backup_id:

        :returns: backup files download link

        :rtype: :class:`~otcextensions.sdk.rds.v3.backup.BackupFile`
        """
        return self._list(_backup.BackupFile, backup_id=backup_id)

    def wait_for_backup(self, backup, status='COMPLETED', failures=None,
                        interval=2, wait=300, attribute='status'):
        failures = ['FAILED'] if failures is None else failures
        return resource.wait_for_status(
            self, backup, status, failures, interval, wait)
