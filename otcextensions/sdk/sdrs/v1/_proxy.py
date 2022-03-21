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
from openstack import exceptions

from otcextensions.sdk.sdrs.v1 import job as _job
from otcextensions.sdk.sdrs.v1 import active_domains as _active_domains
from otcextensions.sdk.sdrs.v1 import protection_group as _protection_group
from otcextensions.sdk.sdrs.v1 import protected_instance as _protected_instance
from otcextensions.sdk.sdrs.v1 import replication_pair as _replication_pair
from otcextensions.sdk.sdrs.v1 import dr_drill as _dr_drill
from otcextensions.sdk.sdrs.v1 import task_center as _task_center
from otcextensions.sdk.sdrs.v1 import quota as _quota


class Proxy(proxy.Proxy):
    skip_discovery = True

    # ======== Job ========
    def get_job(self, job):
        """ Get single SDRS job by UUID.

        :param job: The id or and instance of
            :class:'~otcextensions.sdk.sdrs.v1.job.Job'

        :returns: instance of
            :class: '~class:'otcextensions.sdk.sdrs.v1.job.Job'
        """
        return self._get(_job.Job, job)

    # ======== Active-active domain ========
    def get_domains(self):
        """Retrieve a generator of Active-active domains

        :returns: A generator of active-active domains
            :class: '~otcextensions.sdk.sdrs.v1.active_domains.ActiveDomain'
        """
        return self._list(_active_domains.ActiveDomains)

    # ======== Protection group ========
    def create_protection_group(self, **attrs):
        """Creating a SDRS protection group using attributes

        :param dict attrs:  Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`,
            comprised of the properties on the ProtectionGroup class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`

        """
        return self._create(_protection_group.ProtectionGroup, **attrs)

    def protection_groups(self, **query):
        """Retrieve a generator of Protection groups

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * 'availability_zone': Production site AZ
            * `limit`: Number of records displayed per page
            * `marker`: ID of the last record displayed
            * `name`: Protection group name
            * `offset`: Offset value
            * 'query_type': Query type of protection group
            * `status`: Status

        :returns: A generator of protection groups
            :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup` instances
        """
        return self._list(_protection_group.ProtectionGroup, **query)

    def get_protection_group(self, protection_group):
        """Get the protection group by UUID.

        :param protection_group: key id or an instance of
            :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`

        :returns: instance of
            :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
        """
        return self._get(
            _protection_group.ProtectionGroup,
            protection_group
        )

    def delete_protection_group(self, protection_group, ignore_missing=True):
        """Delete a single SDRS protection group.

        :param protection_group: The value can be the ID of a protection_group
             or a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup` will
            be raised when the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent protection group.
        """
        return self._delete(
            _protection_group.ProtectionGroup,
            protection_group,
            ignore_missing=ignore_missing,
        )

    def find_protection_group(self, name_or_id, ignore_missing=True):
        """Find a single SDRS protection group by name or id

        :param name_or_id: The name or ID of a protection group
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the group does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent protection group.

        :returns: a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
        """
        return self._find(
            _protection_group.ProtectionGroup, name_or_id,
            ignore_missing=ignore_missing
        )

    def update_protection_group(self, protection_group, name):
        """Update SDRS protection group name

        :param protection_group: The value can be the ID of a protection group
            or a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
            instance.
        :param str name: name to be updated for protection group

        :rtype: :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
        """
        protection_group = self._get_resource(
            _protection_group.ProtectionGroup, protection_group
        )
        return self._update(
            _protection_group.ProtectionGroup, protection_group, name=name
        )

    def enable_protection(self, protection_group):
        """Enable protection for existing protection group

        :param protection_group: The value can be the ID of a protection group
            or a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
            instance.
        :returns: The result is the job id of an action
        """
        protection_group = self._get_resource(
            _protection_group.ProtectionGroup,
            protection_group
        )
        return protection_group.enable_protection_group(
            self,
            protection_group=protection_group.id
        )

    def disable_protection(self, protection_group):
        """Disable protection for existing protection group

        :param protection_group: The value can be the ID of a protection group
            or a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
            instance.
        :returns: The result is the job id of an action
        """
        protection_group = self._get_resource(
            _protection_group.ProtectionGroup,
            protection_group
        )
        return protection_group.disable_protection_group(
            self,
            protection_group=protection_group.id
        )

    def perform_failover(self, protection_group):
        """Perform failover for protection group

        :param protection_group: The value can be the ID of a protection group
            or a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
            instance.
        :returns: The result is the job id of an action
        """
        protection_group = self._get_resource(
            _protection_group.ProtectionGroup,
            protection_group
        )
        return protection_group.perform_failover(
            self,
            protection_group=protection_group.id
        )

    def perform_planned_failover(self, protection_group, priority_station='target'):
        """Perform failover for protection group

        :param protection_group: The value can be the ID of a protection group
            or a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
            instance.
        :param priority_station: direction of planned failover
            Values: 'target' or 'source'
        :returns: The result is the job id of an action
        """
        protection_group = self._get_resource(
            _protection_group.ProtectionGroup,
            protection_group
        )
        return protection_group.perform_planned_failover(
            self,
            protection_group=protection_group.id,
            priority_station=priority_station
        )

    # ======== Protected instance ========
    def create_protected_instance(self, **attrs):
        """Creating a protected instance using attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`,
            comprised of the properties on the Protected instance class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        """
        return self._create(
            _protected_instance.ProtectedInstance,
            **attrs
        )

    def delete_protected_instance(self, protected_instance, delete_target_server=False,
                                  delete_target_eip=False, ignore_missing=True):
        """Delete a single SDRS protected instance.

        :param protected_instance: The value can be the ID of a protected instance
             or a :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
             instance.
        :param bool delete_target_server: Specifies whether target
            ECS should be deleted after protection group deletion
        :param bool delete_target_eip: Specifies whether target
            EIP should be deleted after protection group deletion
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent protected instance
        :returns: instance of
            :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        """
        res = self._get_resource(_protected_instance.ProtectedInstance,
                                 protected_instance)
        try:
            del_in = res.delete(self, delete_target_server=delete_target_server,
                                delete_target_eip=delete_target_eip)
        except exceptions.ResourceNotFound:
            if ignore_missing:
                return None
            raise
        return del_in

    def protected_instances(self, **query):
        """Retrieve a generator of Protected instances

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * 'availability_zone': Production site AZ
            * `limit`: Number of records displayed per page
            * `marker`: ID of the last record displayed
            * `name`: Protection group name
            * `offset`: Offset value
            * 'protected_instance_ids': Protected instance ID list
            * 'query_type': Query type of protected instance
            * 'server_group_id': Protection group ID
            * 'server_group_ids': Protection groups ID list
            * `status`: Status

        :returns: A generator of protected instances
            :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
            instances
        """
        return self._list(_protected_instance.ProtectedInstance,
                          **query)

    def get_protected_instance(self, instance_id):
        """Get the SDRS protected instance by UUID.

        :param instance_id: key id or an instance of
            :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`

        :returns: instance of
            :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        """
        return self._get(
            _protected_instance.ProtectedInstance,
            instance_id
        )

    def update_protected_instance(self, instance_id, name):
        """Update SDRS protected instance name

        :param instance_id: The value can be the ID of a protected instance
            or a :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
            instance.
        :param str name: name to be updated for protected instance

        :rtype: :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        """
        protected_instance = self._get_resource(
            _protected_instance.ProtectedInstance, instance_id
        )
        return self._update(
            _protected_instance.ProtectedInstance,
            protected_instance,
            name=name
        )

    def find_protected_instance(self, name_or_id, ignore_missing=True):
        """Find a single SDRS protected instance by name or id

        :param name_or_id: The name or ID of a protected instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the instance does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent protected instance.

        :returns: a :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        """
        return self._find(
            _protected_instance.ProtectedInstance,
            name_or_id,
            ignore_missing=ignore_missing
        )

    def attach_replication_pair(self, protected_instance,
                                replication,
                                device='/dev/vdb'):
        """Attach replication pair to protected instance

        :param protected_instance: The value can be the ID of a protected instance
            or a :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        :param replication:The value can be the ID of a replication pair
            or a :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
        :param device: Disk device name of replication pair
        """
        protected_instance = self._get_resource(
            _protected_instance.ProtectedInstance,
            protected_instance)
        replication = self._get_resource(
            _replication_pair.ReplicationPair, replication)

        return protected_instance.attach_pair(
            self,
            protected_instance=protected_instance.id,
            replication_id=replication.id,
            device=device
        )

    def detach_replication_pair(self,
                                protected_instance,
                                replication):
        """Detach replication pair from protected instance

        :param protected_instance: The value can be the ID of a protected instance
            or a :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        :param replication:The value can be the ID of a replication pair
            or a :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
        """
        protected_instance = self._get_resource(
            _protected_instance.ProtectedInstance,
            protected_instance)
        replication = self._get_resource(
            _replication_pair.ReplicationPair, replication)
        return protected_instance.detach_pair(
            self,
            protected_instance=protected_instance.id,
            replication_id=replication.id
        )

    def add_nic(self, protected_instance, subnet_id,
                security_groups=None, ip_address=None):
        """Add NIC to a protected instance

        :param protected_instance: The value can be the ID of a protected instance
            or a :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        :param str subnet_id: Subnet ID of the NIC to be added
        :param list security_groups: list of security groups to be added for NIC
            in format 'id': 'value'
        :param str ip_address: IP address of NIC
        """
        protected_instance = self._get_resource(
            _protected_instance.ProtectedInstance,
            protected_instance)
        return protected_instance.add_nic(
            self,
            protected_instance=protected_instance.id,
            subnet_id=subnet_id,
            security_groups=security_groups,
            ip_address=ip_address
        )

    def delete_nic(self, protected_instance, nic_id):
        """Delete NIC from a protected instance

        :param protected_instance: The value can be the ID of a protected instance
            or a :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        :param str nic_id: ID of a Network interface card to be deleted
        """
        protected_instance = self._get_resource(
            _protected_instance.ProtectedInstance,
            protected_instance)
        return protected_instance.delete_nic(
            self,
            protected_instance=protected_instance.id,
            nic_id=nic_id
        )

    def modify_protected_instance(self,
                                  protected_instance,
                                  flavor=None,
                                  production_flavor=None,
                                  dr_flavor=None):
        """Modify server(s) flavor of protected instance

        :param protected_instance: The value can be the ID of a protected instance
            or a :class:`~otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance`
        :param str flavor: flavor ID for both production and DR sites
        :param str production_flavor: flavor ID for production site
            If 'flavor' is specified this parameter doesn't take effect
        :param str dr_flavor: flavor ID for DR site
            If 'flavor' is specified this parameter doesn't take effect
        """
        protected_instance = self._get_resource(
            _protected_instance.ProtectedInstance,
            protected_instance)
        return protected_instance.modify_instance(
            self,
            protected_instance=protected_instance.id,
            flavor=flavor,
            production_flavor=production_flavor,
            dr_flavor=dr_flavor
        )

    # ======== Replication pair ========

    def create_replication_pair(self, **attrs):
        """Creating a replication pair using attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`,
            comprised of the properties on the Replication Pair class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
        """
        return self._create(
            _replication_pair.ReplicationPair,
            **attrs
        )

    def delete_replication_pair(self, replication, server_group_id=None,
                                delete_target_volume=False, ignore_missing=True):
        """Delete a single SDRS replication pair

        :param replication: The value can be the ID of a replication pair
             or a :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
             instance.
        :param bool server_group_id: Protection group ID of replication pair
        :param bool delete_target_volume: Specifies whether DR site
            volume should be deleted after replication pair deletion
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent protected instance
        :returns: instance of
            :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
        """
        res = self._get_resource(_replication_pair.ReplicationPair,
                                 replication)
        try:
            del_in = res.delete(self, server_group_id=server_group_id,
                                delete_target_volume=delete_target_volume)
        except exceptions.ResourceNotFound:
            if ignore_missing:
                return None
            raise
        return del_in

    def replication_pairs(self, **query):
        """Retrieve a generator of Replication pairs

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * 'availability_zone': Production site AZ
            * `limit`: Number of records displayed per page
            * `marker`: ID of the last record displayed
            * `name`: Replication pair name
            * `offset`: Offset value
            * 'protected_instance_id': Protected instance ID
            * 'protected_instance_ids': Protected instances ID list
            * 'query_type': Query type of replication pair
                Values: status_abnormal, general
            * 'server_group_id': Protection group ID
            * 'server_group_ids': Protection groups ID list
            * `status`: Status

        :returns: A generator of replication pairs
            :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
            instances
        """
        return self._list(_replication_pair.ReplicationPair,
                          **query)

    def get_replication_pair(self, replication):
        """Get the SDRS replication pair by UUID.

        :param replication: key id or an instance of
            :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`

        :returns: instance of
            :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
        """
        return self._get(_replication_pair.ReplicationPair,
                         replication)

    def find_replication_pair(self, name_or_id, ignore_missing=True):
        """Find a single SDRS replication pair by name or id

        :param name_or_id: The name or ID of a replication pair
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the pair does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent replication pair

        :returns: a :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
        """
        return self._find(
            _replication_pair.ReplicationPair,
            name_or_id,
            ignore_missing=ignore_missing
        )

    def expand_replication_pair(self, replication, new_size):
        """Expand replication pair

        :param replication: The value can be the ID of a replication pair
            or a :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
        :param int new_size: Replication pair new size
        """
        replication = self._get_resource(_replication_pair.ReplicationPair,
                                         replication)
        return replication.expand_replication(self,
                                              replication=replication.id,
                                              new_size=new_size)

    def update_replication_pair(self, replication, name):
        """Update SDRS replication pair name

        :param replication: The value can be the ID of a replication pair
            or a :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
            instance.
        :param str name: name to be updated for replication pair

        :rtype: :class:`~otcextensions.sdk.sdrs.v1.replication_pair.ReplicationPair`
        """
        replication = self._get_resource(
            _replication_pair.ReplicationPair, replication
        )
        return self._update(
            _replication_pair.ReplicationPair,
            replication,
            name=name
        )

    # ======== Disaster recovery drill ========

    def create_dr_drill(self, **attrs):
        """Creating a disaster recovery drill using attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill`,
            comprised of the properties on the DR drill class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill`
        """
        return self._create(
            _dr_drill.DRDrill,
            **attrs
        )

    def delete_dr_drill(self, dr_drill, ignore_missing=True):
        """Delete a single SDRS DR drill

        :param dr_drill: The value can be the ID of a dr_drill
             or a :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill` will
            be raised when the dr_drill does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent DR drill
        """
        return self._delete(
            _dr_drill.DRDrill,
            dr_drill,
            ignore_missing=ignore_missing,
        )

    def dr_drills(self, **query):
        """Retrieve a generator of DR drills

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * 'drill_vpc_id': VPC ID used for DR drill
            * `limit`: Number of records displayed per page
            * `marker`: ID of the last record displayed
            * `name`: DR drill name
            * `offset`: Offset value
            * 'server_group_id': Protection group ID
            * `status`: Status

        :returns: A generator of dr drills
            :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill`
            instances
        """
        return self._list(_dr_drill.DRDrill,
                          **query)

    def get_dr_drill(self, dr_drill):
        """Get the SDRS DR drill by UUID.

        :param dr_drill: key id or an instance of
            :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill`

        :returns: instance of
            :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill`
        """
        return self._get(_dr_drill.DRDrill,
                         dr_drill)

    def find_dr_drill(self, name_or_id, ignore_missing=True):
        """Find a single SDRS DR drill by name or id

        :param name_or_id: The name or ID of a DR drill
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the pair does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent DR drill

        :returns: a :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill`
        """
        return self._find(
            _dr_drill.DRDrill,
            name_or_id,
            ignore_missing=ignore_missing
        )

    def update_dr_drill(self, dr_drill, name):
        """Update SDRS DR drill name

        :param dr_drill: The value can be the ID of a DR drill
            or a :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill`
            instance.
        :param str name: name to be updated for DR drill

        :rtype: :class:`~otcextensions.sdk.sdrs.v1.dr_drill.DRDrill`
        """
        dr_drill = self._get_resource(
            _dr_drill.DRDrill, dr_drill
        )
        return self._update(
            _dr_drill.DRDrill,
            dr_drill,
            name=name
        )

    # ======== Failed tasks ========

    def failed_tasks(self, **query):
        """Retrieve a generator of Failed tasks

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * 'failure_status': query the task failure status
            * `limit`: Number of records displayed per page
            * `marker`: ID of the last record displayed
            * `offset`: Offset value
            * 'resource_name': protection group name
            * `resource_type`: type of the resource
            * `server_group_id`: protection group ID

        :returns: A generator of failed tasks
            :class:`~otcextensions.sdk.sdrs.v1.task_center.FailedTask`
            instances
        """
        return self._list(_task_center.FailedTask,
                          **query)

    def delete_failed_task(self, failed_job_id, ignore_missing=True):
        """Delete a single Failed task

        :param failed_job_id: The value can be the ID of a failed task
             or a :class:`~otcextensions.sdk.sdrs.v1.task_center.FailedTask`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.sdrs.v1.task_center.FailedTask` will
            be raised when the dr_drill does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent Failed task
        """
        return self._delete(
            _task_center.FailedTask,
            failed_job_id,
            ignore_missing=ignore_missing,
        )

    def delete_all_failed_tasks(self):
        """Delete all failed tasks of all protection
        groups
        """
        endpoint = self.get_endpoint()
        return _task_center.FailedTask.delete_all_tasks(self.session, endpoint)

    def delete_protection_group_tasks(self, protection_group):
        """Delete all failed tasks of a single
        protection group

        :param protection_group: The value can be the ID of a protection group
             or a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
             instance.
        """
        protection_group = self._get_resource(
            _protection_group.ProtectionGroup,
            protection_group
        )
        endpoint = self.get_endpoint()
        return _task_center.FailedTask.delete_protection_tasks(self.session,
                                                               endpoint,
                                                               protection_group.id)

    # ======== Tenant SDRS quota ========

    def quotas(self):
        """Retrieve a generator of SDRS quotas

        :returns: A generator of resource quotas
            :class:`~otcextensions.sdk.sdrs.v1.quota.Quota`
            instances
        """
        return self._list(_quota.Quota)
