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

from otcextensions.sdk.sdrs.v1 import job as _job
from otcextensions.sdk.sdrs.v1 import active_domains as _active_domains
from otcextensions.sdk.sdrs.v1 import protection_group as _protection_group

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
            * `name`: Protection group name
            * `offset`: Offset value
            * 'query_type': Query type of protection group
            * `status`: Status

        :returns: A generator of backup
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
        """Delete a single SDRS protection_group.

        :param protection_group: The value can be the ID of a protection_group
             or a :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent backup.
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
            to delete a nonexistent group.

        :returns: ``None``
        """
        return self._find(
            _protection_group.ProtectionGroup, name_or_id,
            ignore_missing=ignore_missing,
        )

    def update_protection_group(self, protection_group, name):
        """Update SDRS protection group name

        :param protection_group: The value can be the ID of a backup
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
