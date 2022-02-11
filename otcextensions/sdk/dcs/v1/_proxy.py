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
from otcextensions.sdk.dcs.v1 import backup as _backup
from otcextensions.sdk.dcs.v1 import config as _config
from otcextensions.sdk.dcs.v1 import instance as _instance
from otcextensions.sdk.dcs.v1 import restore_record as _restore_record
from otcextensions.sdk.dcs.v1 import statistic as _stat
from otcextensions.sdk.dcs.v1 import quota as _quota
from otcextensions.sdk.dcs.v1 import maintenance_time_window as _maintenance_tw
from otcextensions.sdk.dcs.v1 import service_specification as _service_spec


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Instances ========
    def create_instance(self, **kwargs):
        """Create an instance

        :param dict kwargs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        return self._create(_instance.Instance, **kwargs)

    def instances(self, **query):
        """List all cache instances

        :returns: A generator of Instance object of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        return self._list(_instance.Instance, **query)

    def get_instance(self, instance):
        """Get detail about a given instance

        :param instance: The instance id or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: one object of class
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        return self._get(_instance.Instance, instance)

    def find_instance(self, name_or_id, ignore_missing=False):
        """Find instance by name or id

        :param name_or_id: The instance id or name of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: one object of class
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        return self._find(_instance.Instance, name_or_id,
                          ignore_missing=ignore_missing)

    def update_instance(self, instance, **attrs):
        """Update instance with attributes

        :param instance: The value can be the ID of an instance
            or a :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
            instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dcs.v1.instance.Instance`,
            comprised of the properties on the Instance class.
        :returns: The updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        # Update method does not return the instance object which needs to be
        # fetched additionally in return statement.
        self._update(_instance.Instance, instance, **attrs)
        return self._get(_instance.Instance, instance)

    def delete_instance(self, instance, ignore_missing=True):
        """Delete an instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.exceptions.ResourceNotFound` will be
            raised when the queue does not exist.
        :returns: `None`
        """
        self._delete(_instance.Instance, instance,
                     ignore_missing=ignore_missing)

    def extend_instance(self, instance, capacity):
        """Extend capacity of existing instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :param int capacity: New instance capacity
        :returns: Updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self._get_resource(_instance.Instance, instance)
        res.extend(self, capacity)
        return self._get(_instance.Instance, res)

    def stop_instance(self, instance):
        """Stop existing instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: Updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self.find_instance(instance)
        res.stop(self)
        return self._get(_instance.Instance, res)

    def start_instance(self, instance):
        """Start existing instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: Updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self.find_instance(instance)
        res.start(self)
        return self._get(_instance.Instance, res)

    def restart_instance(self, instance):
        """Retart existing instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: Updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self.find_instance(instance)
        res.restart(self)
        return self._get(_instance.Instance, res)

    def change_instance_password(self, instance,
                                 current_password, new_password):
        """Change instance password

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :param current_password: Current instance password
        :param new_password: New instance password
        :returns: Updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self.find_instance(instance)
        return res.change_pwd(
            self,
            current_password=current_password,
            new_password=new_password)

    # ======== Backups ========
    def backup_instance(self, instance, **kwargs):
        """Create an instance backup

        :param instance: The instance id or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :param dict kwargs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.dcs.v1.backup.Backup`
        """
        inst = self._get_resource(_instance.Instance, instance)
        return self._create(_backup.Backup, instance_id=inst.id, **kwargs)

    def backups(self, instance, **query):
        """List all instance backups

        :returns: A generator of Instance object of
            :class:`~otcextensions.sdk.dcs.v1.backup.Backup`
        """
        inst = self._get_resource(_instance.Instance, instance)
        return self._list(
            _backup.Backup, paginated=False,
            instance_id=inst.id, **query)

    def delete_instance_backup(self, instance, backup, ignore_missing=True,
                               **attrs):
        """Delete an instance backup

        :param backup: The instance id, an instance of
            :class:`~otcextensions.sdk.dcs.v1.backup.Backup`
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.exceptions.ResourceNotFound` will be
            raised when the queue does not exist.
        :returns: `None`
        """
        inst = self._get_resource(_instance.Instance, instance)
        self._delete(_backup.Backup, backup, instance_id=inst.id,
                     ignore_missing=ignore_missing,
                     **attrs)

    # ======== Restores ========
    def restore_instance(self, instance, backup=None, **kwargs):
        """Restore instance from backup

        :param instance: The instance id or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :param dict kwargs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.dcs.v1.restore_record.RestoreRecord`
            `backup_id` and `description` are expected
        """
        inst = self._get_resource(_instance.Instance, instance)
        return self._create(
            _restore_record.RestoreRecord,
            instance_id=inst.id,
            **kwargs)

    def restore_records(self, instance, **query):
        """List all instance restore records

        :param instance: The instance id or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: A generator of Instance object of
            :class:`~otcextensions.sdk.dcs.v1.restore_record.RestoreRecord`
        """
        inst = self._get_resource(_instance.Instance, instance)
        return self._list(
            _restore_record.RestoreRecord, paginated=False,
            instance_id=inst.id, **query)

    # ======== Misc ========
    def statistics(self):
        """Query statisctics for all instances

        :returns: A generator of Instance object of
            :class:`~otcextensions.sdk.dcs.v1.stat.Statistics`
        """
        return self._list(_stat.Statistic, paginated=False)

    def instance_params(self, instance):
        """List all instance configuration records

        :param instance: The instance id or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: A generator of Instance object of
            :class:`~otcextensions.sdk.dcs.v1.config.Config`
        """
        inst = self._get_resource(_instance.Instance, instance)
        return self._list(
            _config.Config, paginated=False,
            instance_id=inst.id)

    def update_instance_params(self, instance, params):
        """Update instance configuration parameter with attributes

        :param instance: The value can be the ID of an instance
            or a :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
            instance.
        :param params: List of parameters of
            a :class:`~otcextensions.sdk.dcs.v1.config.Config`.
        :returns: None
        """
        res = self._get_resource(_instance.Instance, instance)
        obj = self._get_resource(_config.Config, None, instance_id=res.id)
        return obj._update(
            self,
            params
        )

    # ======== Quotas ========
    def quotas(self):
        """Return a generator of quotas

        :returns: A generator of quota objects
        :rtype: :class:`~otcextensions.sdk.dcs.v1.quota.Quota`.
        """
        return self._list(_quota.Quota)

    # ======== Maintenance Time Window ========
    def maintenance_time_windows(self):
        """Return a generator of maintenance time windows

        :returns: A generator of maintenance time window objects
        :rtype: :class: `~otcextensions.sdk.dcs.v1.maintenance_time_window.MaintenanceTimeWindow`.
        """
        endpoint = _maintenance_tw.MaintenanceTimeWindow._get_session(
            self).get_endpoint().split('/%').pop(0)
        base_path = endpoint + '/instances/maintain-windows'

        return self._list(
            resource_type=_maintenance_tw.MaintenanceTimeWindow,
            base_path=base_path)

    # ======== Service Specification ========
    def service_specifications(self):
        """Return a generator of service specifications

        :returns: A generator of service specifications
        :rtype: :class:`~otcextensions.sdk.dcs.v1.service_specification.ServiceSpecification`.
        """
        endpoint = _service_spec.ServiceSpecification._get_session(
            self).get_endpoint().split('/%').pop(0)
        base_path = endpoint + '/products'

        return self._list(
            resource_type=_service_spec.ServiceSpecification,
            base_path=base_path
        )
