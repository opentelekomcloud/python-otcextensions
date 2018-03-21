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
        print('get groups is called')
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
        group.resume(self)

    def pause_group(self, group):
        """pause group

        :param group: The value can be the ID of a group
             or a :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`
             instance.
        """
        group = self._get_resource(
            _group.Group, group
        )
        group.pause(self)

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
                  (:class:`~otcextensions.auto_scaling.v1.config.Config`) instances
        """
        return self._list(
            _config.Config, paginated=True,
            **query)

    def create_config(self, name, **attrs):
        """Create a new config from config name and instance-config attributes

        :param name: auto scaling config name
        :param dict attrs: Keyword arguments which will be used to create
                a :class:`~otcextensions.auto_scaling.v1.config.InstanceConfig`,
                comprised of the properties on the InstanceConfig class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.auto_scaling.v1.config.Config`
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
             or a :class:`~otcextensions.auto_scaling.v1.config.Config` instance.
        :returns: Config instance
        :rtype: :class:`~otcextensions.auto_scaling.v1.config.Config`
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
        :rtype: :class:`~otcextensions.auto_scaling.v1.config.Config`
        """
        return self._find(
            _config.Config, name_or_id,
            ignore_missing=ignore_missing,
        )

    def delete_config(self, config, ignore_missing=True):
        """Delete a config

        :param config: The value can be the ID of a config
             or a :class:`~otcextensions.auto_scaling.v1.config.Config` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the config does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent config.

        :returns: Config been deleted
        :rtype: :class:`~otcextensions.auto_scaling.v1.config.Config`
        """
        return self._delete(
            _config.Config, config,
            ignore_missing=ignore_missing,
        )

    def batch_delete_configs(self, configs):
        """batch delete configs

        :param list configs: The list item value can be the ID of a config
             or a :class:`~otcextensions.auto_scaling.v1.config.Config` instance.
        """
        config = _config.Config()
        return config.batch_delete(self, configs)
