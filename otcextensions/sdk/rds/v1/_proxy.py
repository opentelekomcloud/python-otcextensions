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
from openstack import utils
from openstack import proxy

# from otcextensions.sdk import proxy as sdk_proxy

from otcextensions.sdk.rds.v1 import backup as _backup
from otcextensions.sdk.rds.v1 import configuration as _configuration
from otcextensions.sdk.rds.v1 import datastore as _datastore
from otcextensions.sdk.rds.v1 import flavor as _flavor
from otcextensions.sdk.rds.v1 import instance as _instance

_logger = _log.setup_logging('openstack')


class Proxy(proxy.BaseProxy):

    # RDS requires those headers to be present in the request, to native API
    # otherwise 404
    RDS_HEADERS = {
        'Content-Type': 'application/json',
        'X-Language': 'en-us'
    }

    # RDS requires those headers to be present in the request, to OS-compat API
    # otherwise 404
    OS_HEADERS = {
        'Content-Type': 'application/json',
    }

    def get_os_endpoint(self, **kwargs):
        """Return OpenStack compliant endpoint

        """
        endpoint = super(Proxy, self).get_endpoint(**kwargs)
        endpoint_override = self.endpoint_override
        if endpoint.endswith('/rds/v1') and not endpoint_override:
            endpoint_override = endpoint.rstrip('/rds/v1')
            endpoint_override = utils.urljoin(endpoint_override, 'v1.0')
            return endpoint_override
        else:
            _logger.debug('RDS endpoint_override is set. Return it')
            return endpoint_override

    def get_rds_endpoint(self, **kwargs):
        """Return OpenStack compliant endpoint

        """
        endpoint = super(Proxy, self).get_endpoint(**kwargs)
        endpoint_override = self.endpoint_override
        if endpoint.endswith('/rds/v1') and not endpoint_override:
            return endpoint
        elif endpoint_override:
            _logger.debug('RDS endpoint_override is set. Return it')
            return endpoint_override
        else:
            return endpoint

    @proxy._check_resource(strict=False)
    def _get(self, resource_type, value=None, requires_id=True,
             endpoint_override=None, headers=None,
             **attrs):
        """Get a resource

        overriden to incorporate optional headers and endpoint_override

        :param resource_type: The type of resource to get.
        :type resource_type: :class:`~openstack.resource.Resource`
        :param value: The value to get. Can be either the ID of a
                      resource or a :class:`~openstack.resource.Resource`
                      subclass.
        :param dict attrs: Attributes to be passed onto the
                           :meth:`~openstack.resource.Resource.get`
                           method. These should correspond
                           to either :class:`~openstack.resource.Body`
                           or :class:`~openstack.resource.Header`
                           values on this resource.

        :returns: The result of the ``get``
        :rtype: :class:`~openstack.resource.Resource`
        """

        res = self._get_resource(resource_type, value, **attrs)

        _logger.debug('resource %s' % res)

        return res.get(
            self, requires_id=requires_id,
            error_message="No {resource_type} found for {value}".format(
                resource_type=resource_type.__name__, value=value),
            # endpoint_override=endpoint_override,
            # headers=headers
        )

    def datastore_types(self):
        """List supported datastore types

        :returns: A generator of supported datastore types
        :rtype :string
        """
        for ds in ['MySQL', 'PostgreeSQL', 'SQLServer']:
            yield ds

        return

    def datastores(self, db_name):
        """List datastores

        :param dbId: database store name
            (MySQL, PostgreSQL, or SQLServer and is case-sensitive.)

        :returns: A generator of datastore versions
        :rtype: :class:`~otcextensions.sdk.rds_os.v1.flavor.Flavor
        """
        headers = {
            'Content-Type': 'application/json',
            'X-Language': 'en-us'
        }
        return self._list(
            _datastore.Datastore,
            paginated=False,
            endpoint_override=self.get_rds_endpoint(),
            headers=headers,
            project_id=self.session.get_project_id(),
            datastore_name=db_name
        )

    def flavors(self):
        """List flavors of given datastore id and region

        :param dbId: database store id
        :param region: region

        :returns: A generator of flavor
        :rtype: :class:`~otcextensions.sdk.rds_os.v1.flavor.Flavor
        """
        return self._list(_flavor.Flavor, paginated=False,
                          endpoint_override=self.get_os_endpoint(),
                          project_id=self.session.get_project_id())

    def get_flavor(self, flavor):
        """Get the detail of a flavor

        :param id: Flavor id or an object of class
                   :class:`~otcextensions.sdk.rds_os.v1.flavor.Flavor
        :returns: Detail of flavor
        :rtype: :class:`~otcextensions.sdk.rds_os.v1.flavor.Flavor
        """
        return self._get(
            _flavor.Flavor,
            flavor,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_os_endpoint(),
        )

    def find_flavor(self, name_or_id, ignore_missing=True):
        raise NotImplementedError

    def create_instance(self, **attrs):
        """Create a new instance from attributes

        :param dict attrs: Keyword arguments which will be used to create
                   a :class:`~otcextensions.sdk.rds.v1.instance.Instance`,
                   comprised of the properties on the Instance class.

        :returns: The results of server creation
        :rtype: :class:`~otcextensions.sdk.rds.v1.instance.Instance`
        """
        raise NotImplementedError
        return self._create(_instance.Instance, **attrs)

    def delete_instance(self, instance, ignore_missing=True):
        """Delete an instance

        :param instance: The value can be either the ID of an instance or a
               :class:`~otcextensions.sdk.rds.v1.instance.Instance` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the instance does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent instance.

        :returns: ``None``
        """
        raise NotImplementedError
        self._delete(_instance.Instance, instance,
                     ignore_missing=ignore_missing,
                     project_id=self.session.get_project_id(),
                     endpoint_override=self.get_os_endpoint())

    # def find_database(self, name_or_id, ignore_missing=True):
    #     """Find a single instance
    #
    #     :param name_or_id: The name or ID of a instance.
    #     :param bool ignore_missing: When set to ``False``
    #                 :class:`~openstack.exceptions.ResourceNotFound` will be
    #                 raised when the resource does not exist.
    #                 When set to ``True``, None will be returned when
    #                 attempting to find a nonexistent resource.
    #     :returns: One :class:`~otcextensions.sdk.rds.v1.instance.Instance`
    #               or None
    #     """
    #     raise NotImplementedError
    #     return self._find(_instance.Instance, name_or_id,
    #                       ignore_missing=ignore_missing,
    #                       project_id=self.session.get_project_id())

    def get_instance(self, instance):
        """Get a single instance

        :param instance: The value can be the ID of an instance or a
                         :class:`~otcextensions.sdk.rds.v1.instance.Instance`
                         instance.

        :returns: One :class:`~otcextensions.sdk.rds.v1.instance.Instance`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(
            _instance.Instance,
            instance,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_os_endpoint()
        )

    def instances(self):
        """Return a generator of instances

        :returns: A generator of instance objects
        :rtype: :class:`~otcextensions.sdk.rds.v1.instance.Instance`
        """
        return self._list(_instance.Instance, paginated=False,
                          project_id=self.session.get_project_id(),
                          endpoint_override=self.get_os_endpoint()
                          )

    def update_instance(self, instance, **attrs):
        """Update a instance

        :param instance: Either the id of a instance or a
                         :class:`~otcextensions.sdk.rds.v1.instance.Instance`
                         instance.
        :attrs kwargs: The attributes to update on the instance represented
                       by ``value``.

        :returns: The updated instance
        :rtype: :class:`~otcextensions.sdk.rds.v1.instance.Instance`
        """
        raise NotImplementedError
        return self._update(_instance.Instance, instance, **attrs)

    def configuration_groups(self, **attrs):
        """Obtaining a Parameter Group List

        :returns: A generator of ParameterGroup object
        :rtype: :class:`~otcextensions.sdk.rds.v1.configuration.ParameterGroup
        """
        return self._list(
            _configuration.ParameterGroup,
            paginated=False,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_os_endpoint(),
        )

    def get_configuration_group(self, configuration_group):
        """Obtaining a Parameter Group

        :param cg: The value can be the ID of a Parameter Group or a object of
               :class:`~otcextensions.sdk.rds.v1.configuration.Configurations`.
        :returns: A Parameter Group Object
        :rtype: :class:`~otcextensions.rds.v1.configuration.ParameterGroup`.

        """
        return self._get(
            _configuration.ParameterGroup,
            configuration_group,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_os_endpoint())

    def create_configuration_group(self, parameter_group, **attrs):
        """Creating a Parameter Group

        :param dict \*\*attrs: Dict to overwrite ParameterGroup object
        :returns: A Parameter Group Object
        :rtype: :class:`~otcextensions.sdk.rds.v1.configuration.ParameterGroup`
        """
        raise NotImplementedError
        return self._create(_configuration.ParameterGroup,
                            endpoint_override=self.get_os_endpoint(),
                            **attrs)

    def delete_configuration_group(self, cg, ignore_missing=True):
        """Deleting a Parameter Group

        :param cg: The value can be the ID of a Parameter Group or a object of
               :class:`~otcextensions.sdk.rds.v1.configuration.ParameterGroup`.
        :param bool ignore_missing: When set to ``False``
                :class:`~openstack.exceptions.ResourceNotFound` will be
                raised when the Parameter Group does not exist.
                When set to ``True``, no exception will be set when
                attempting to delete a nonexistent Parameter Group.

        :returns: None
        """
        raise NotImplementedError
        self._delete(_configuration.ParameterGroup, cg,
                     ignore_missing=ignore_missing)

    def update_configuration_group(self, cg, **attrs):
        """Adding a Self-defined Parameter

        :param cg: The value can be the ID of a Parameter Group or a object of
               :class:`~otcextensions.sdk.rds.v1.configuration.ParameterGroup`.
        :param dict \*\*attrs: Dict to use create Self-defined Parameter
        :returns: An updated Parameter Group Object
        """
        raise NotImplementedError
        return self._update(_configuration.ParameterGroup, cg, **attrs)

    def backups(self):
        """List Backups

        :returns: A generator of backup
        :rtype: :class:`~otcextensions.sdk.rds.v1.backup.Backup
        """
        return self._list(_backup.Backup, paginated=False,
                          endpoint_override=self.get_rds_endpoint(),
                          project_id=self.session.get_project_id(),
                          headers=self.RDS_HEADERS)

    def create_backup(self, instance, **attrs):
        """Create a backups of instance

        :returns: A new backup object
        :rtype: :class:`~otcextensions.sdk.rds.v1.backup.Backup
        """
        instance = self._get_resource(_instance.Instance, instance)
        return self._create(
            _backup.Backup,
            instance_id=instance.id,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_rds_endpoint(),
            headers=self.RDS_HEADERS,
            **attrs
        )

    def delete_backup(self, backup, ignore_missing=True):
        """Deletes given backup

        :param instance: The value can be either the ID of an instance or a
               :class:`~openstack.database.v1.instance.Instance` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the instance does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent instance.

        :returns: ``None``
        """
        return self._delete(
            _backup.Backup,
            backup,
            ignore_missing=ignore_missing,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_rds_endpoint(),
            headers=self.RDS_HEADERS
        )

    def get_backup_policy(self, instance):
        """Obtaining a backup policy of the instance

        :param instance: This parameter can be either the ID of an instance
                     or a :class:`~openstack.sdk.rds.v1.instance.Instance`
        :returns: A Backup policy
        :rtype: :class:`~otcextensions.sdk.rds.v1.configuration.BackupPolicy`

        """
        instance = self._get_resource(_instance.Instance, instance)
        return self._get(
            _backup.BackupPolicy,
            requires_id=False,
            instance_id=instance.id,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_rds_endpoint(),
            headers=self.RDS_HEADERS
        )

    def set_backup_policy(self, backup_policy, instance, **attrs):
        """Sets the backup policy of the instance

        :param instance: This parameter can be either the ID of an instance
                     or a :class:`~openstack.sdk.rds.v1.instance.Instance`
        :param dict attrs: The attributes to update on the backup_policy
                           represented by ``backup_policy``.

        :returns: ``None``
        """
        instance = self._get_resource(_instance.Instance, instance)
        return self._update(
            _backup.BackupPolicy,
            backup_policy,
            instance_id=instance.id,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_rds_endpoint(),
            headers=self.RDS_HEADERS,
            **attrs)
