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

from openstack import _log
# from openstack import exceptions

from otcextensions.sdk import sdk_proxy

# from otcextensions.i18n import _

from otcextensions.sdk.auto_scaling.v1 import group as _group
from otcextensions.sdk.auto_scaling.v1 import config as _config
from otcextensions.sdk.auto_scaling.v1 import policy as _policy
from otcextensions.sdk.auto_scaling.v1 import activity as _activity
from otcextensions.sdk.auto_scaling.v1 import instance as _instance
from otcextensions.sdk.auto_scaling.v1 import quota as _quota

_logger = _log.setup_logging('openstack')


class Proxy(sdk_proxy.Proxy):

    # ======== Groups ========
    def groups(self, **query):
        """Retrieve a generator of groups

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * ``name``: group name
            * ``status``: group status, ``INSERVICE``, ``PAUSED``, ``ERROR``
            * ``scaling_configuration_id``: scaling configuration id
            * ``marker``:  pagination marker, known as ``start_number``
            * ``limit``: pagination limit

        :returns: A generator of group
            (:class:`~otcextensions.sdk.auto_scaling.v1.group.Group`) instances
        """
        return self._list(
            _group.Group, paginated=True,
            **query
        )

    def create_group(self, **attrs):
        """Create a new group from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`,
            comprised of the properties on the Group class.
        :returns: The results of group creation
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
        """
        return self._create(
            _group.Group, prepend_key=False, **attrs
        )

    def update_group(self, group, **attrs):
        """update group with attributes

        :param group: The value can be the ID of a group
            or a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
            instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`,
            comprised of the properties on the Group class.
        :returns: The results of group creation
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
        """
        return self._update(
            _group.Group, group, prepend_key=False, **attrs)

    def get_group(self, group):
        """Get a group

        :param group: The value can be the ID of a group
             or a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
             instance.
        :returns: Group instance
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
        """
        return self._get(
            _group.Group, group,
        )

    def delete_group(self, group, ignore_missing=True):
        """Delete a group

        :param group: The value can be the ID of a group
             or a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent group.
        """
        return self._delete(
            _group.Group, group, ignore_missing=ignore_missing,
        )

    def find_group(self, name_or_id, ignore_missing=True):
        """Find a single group

        :param name_or_id: The name or ID of a group
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent group.

        :returns: ``None``
        """
        return self._find(
            _group.Group, name_or_id,
            ignore_missing=ignore_missing,
        )

    def resume_group(self, group):
        """resume group

        :param group: The value can be the ID of a group
             or a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
             instance.
        """
        group = self._get_resource(
            _group.Group, group)
        return group.resume(self)

    def pause_group(self, group):
        """pause group

        :param group: The value can be the ID of a group
             or a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
             instance.
        """
        group = self._get_resource(
            _group.Group, group
        )
        return group.pause(self)

    # ======== Configurations ========
    def configs(self, **query):
        """Retrieve a generator of configs

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * ``name``: configuration name
            * ``image_id``: image id
            * ``marker``:  pagination marker
            * ``limit``: pagination limit

        :returns: A generator of config
            (:class:`~otcextensions.sdk.auto_scaling.v1.config.Config`)
            instances
        """
        return self._list(
            _config.Config, paginated=True,
            **query)

    def create_config(self, name, **attrs):
        """Create a new config from config name and instance-config attributes

        :param name: auto scaling config name
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.auto_scaling.v1.config.InstanceConfig`
            , comprised of the properties on the InstanceConfig class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`
        """
        return self._create(
            _config.Config,
            prepend_key=False,
            name=name,
            **attrs
        )

    def get_config(self, config):
        """Get a config

        :param config: The value can be the ID of a config
             or a :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`
             instance.
        :returns: Config instance
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`
        """
        return self._get(
            _config.Config, config
        )

    # Name is not unique, so find might return multiple results
    def find_config(self, name_or_id, ignore_missing=True):
        """Get a config

        :param name_or_id: The name or ID of a config
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the config does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent config.
        :returns: Config instance
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`
        """
        return self._find(
            _config.Config, name_or_id,
            ignore_missing=ignore_missing,
        )

    def delete_config(self, config, ignore_missing=True):
        """Delete a config

        :param config: The value can be the ID of a config
            or a :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`
            instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the config does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent config.

        :returns: Config been deleted
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`
        """
        return self._delete(
            _config.Config, config,
            ignore_missing=ignore_missing,
        )

    def batch_delete_configs(self, configs):
        """batch delete configs

        :param configs: The list item value can be the ID of a config
            or a :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`
            instance.
        """
        config = _config.Config()
        return config.batch_delete(self, configs)

    # ======== Policy ========
    def policies(self, group, **query):
        """Retrieve a generator of policies

        :param group: The value can be the ID of a group
            or a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
            instance.
        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * ``name``: policy name
            * ``type``: policy type
            * ``scaling_group_id``: scaling group id the policy applied to
            * ``marker``:  pagination marker
            * ``limit``: pagination limit

        :returns: A generator of policy
            (:class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`)
            instances
        """
        group = self._get_resource(_group.Group, group)
        return self._list(
            _policy.Policy, paginated=True,
            scaling_group_id=group.id,
            **query)

    def create_policy(self, **attrs):
        """Create a new policy from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`,
            comprised of the properties on the Policy class.
        :returns: The results of policy creation
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
        """
        return self._create(_policy.Policy, prepend_key=False, **attrs)

    def update_policy(self, policy, **attrs):
        """update policy with attributes

        :param policy: The value can be the ID of a policy
             or a :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
             instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`,
            comprised of the properties on the Policy class.
        :returns: The results of policy creation
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
        """
        return self._update(_policy.Policy, policy, prepend_key=False, **attrs)

    def get_policy(self, policy):
        """Get a policy

        :param policy: The value can be the ID of a policy
             or a :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
             instance.
        :returns: Policy instance
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
        """
        return self._get(_policy.Policy, policy)

    def delete_policy(self, policy, ignore_missing=True):
        """Delete a policy

        :param policy: The value can be the ID of a policy
             or a :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the policy does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent policy.

        :returns: Policy been deleted
        :rtype: :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
        """
        return self._delete(_policy.Policy, policy,
                            ignore_missing=ignore_missing)

    def find_policy(self, name_or_id, ignore_missing=True):
        """Find a single policy

        :param name_or_id: The name or ID of a policy
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the policy does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent policy.

        :returns: ``None``
        """
        return self._find(_policy.Policy, name_or_id,
                          ignore_missing=ignore_missing)

    def execute_policy(self, policy):
        """execute policy

        :param policy: The value can be the ID of a policy
             or a :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
             instance.
        """
        policy = self._get_resource(_policy.Policy, policy)
        policy.execute(self)

    def resume_policy(self, policy):
        """resume policy

        :param policy: The value can be the ID of a policy
             or a :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
             instance.
        """
        policy = self._get_resource(_policy.Policy, policy)
        policy.resume(self)

    def pause_policy(self, policy):
        """pause policy

        :param policy: The value can be the ID of a policy
             or a :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`
             instance.
        """
        policy = self._get_resource(_policy.Policy, policy)
        policy.pause(self)

    # ======== Instances ========
    def instances(self, group, **query):
        """Retrieve a generator of instances

        :param group: The value can be the ID of a group
             or a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
             instance.
        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * ``health_status``: instance health status
            * ``lifecycle_status``: policy type
            * ``scaling_group_id``: scaling group id the policy applied to
            * ``marker``:  pagination marker
            * ``limit``: pagination limit

        :returns: A generator of instances with type
            (:class:`~otcextensions.sdk.auto_scaling.v1.instance.Instance`)
        """
        group = self._get_resource(_group.Group, group)
        return self._list(
            _instance.Instance, paginated=True,
            scaling_group_id=group.id, **query)

    def remove_instance(self, instance, delete_instance=False,
                        ignore_missing=True):
        """Remove an instance of auto scaling group

        :precondition:
            * the instance must in ``INSERVICE`` status
            * after remove the instance number of auto scaling group should not
                be less than min instance number
            * The own auto scaling group should not in scaling status

        :param instance: The value can be the ID of a instance or a
            :class:`~otcextensions.sdk.auto_scaling.v1.instance.Instance`
            instance.
        :param bool delete_instance: When set to ``True``, instance will be
            deleted after removed.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the config does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent config.

        :returns: None
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.remove(self,
                               delete_instance=delete_instance,
                               ignore_missing=ignore_missing)

    def batch_instance_action(
            self, group, instances,
            action, delete_instance=False):
        """Batch add instances for auto scaling group

        :param group: The group which instances will be added to,
            The value can be the ID of a group or a
            :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
            instance.
        :param instances: The list item value can be ID of an instance or a
            :class:`~otcextensions.sdk.auto_scaling.v1.instance.Instance`
            instance
        :param action: Action type
            [``ADD``, ``REMOVE``, ``PROTECT``, ``UNPROTECT``]
        :param delete_instance: When set to ``True``, instance will be
            deleted after removed
        """
        group = self._get_resource(_group.Group, group)
        instance = _instance.Instance(scaling_group_id=group.id)
        return instance.batch_action(self, instances, action, delete_instance)

    # ======== Activities ========
    def activities(self, group, **query):
        """Retrieve a generator of Activity

        :param group: The value can be the ID of a group
            or a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
            instance.
        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * ``start_time``: activity start time
            * ``end_time``: activity end time
            * ``marker``:  pagination marker, known as ``start_number``
            * ``limit``: pagination limit

        :returns: A generator of group
            (:class:`~otcextensions.sdk.auto_scaling.v1.activity.Activity`)
            instances
        """
        group = self._get_resource(_group.Group, group)
        return self._list(_activity.Activity,
                          paginated=True,
                          scaling_group_id=group.id,
                          **query)

    # ======== Quotas ========
    def quotas(self, group=None):
        """Retrieve a generator of Quota

        :param group: If group is set, will query quota for the group instead
            of quota of user. The value can be the ID of a group or a
            :class:`~otcextensions.sdk.auto_scaling.v1.group.Group` instance.
        :returns: A generator of quota
            (:class:`~otcextensions.sdk.auto_scaling.v1.quota.Quota`) instances
        """
        if group:
            group = self._get_resource(_group.Group, group)
            return self._list(_quota.ScalingQuota,
                              paginated=False,
                              scaling_group_id=group.id)
        else:
            return self._list(_quota.Quota, paginated=False)
