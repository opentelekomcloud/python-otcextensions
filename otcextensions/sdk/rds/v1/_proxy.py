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
from openstack import exceptions

from otcextensions.sdk import sdk_proxy
from otcextensions.sdk.rds.v1 import backup as _backup
from otcextensions.sdk.rds.v1 import configuration as _configuration
from otcextensions.sdk.rds.v1 import datastore as _datastore
from otcextensions.sdk.rds.v1 import flavor as _flavor
from otcextensions.sdk.rds.v1 import instance as _instance

_logger = _log.setup_logging('openstack')


class Proxy(sdk_proxy.Proxy):

    def get_os_endpoint(self, **kwargs):
        """Return OpenStack compliant endpoint

        """
        return self.get_endpoint(service_type='database')
        # if 'os_endpoint' not in self:
        #     endpoint = super(Proxy, self).get_endpoint(**kwargs)
        #     # endpoint_override = self.endpoint_override
        #     if endpoint.endswith('/rds/v1'):  # and not endpoint_override:
        #         endpoint = endpoint.rstrip('/rds/v1')
        #         endpoint = utils.urljoin(endpoint, 'v1.0')
        #         self.os_endpoint = endpoint
        #     # else:
        #     #     _logger.debug('RDS endpoint_override is set. Return it')
        #     #     return endpoint_override
        # else:
        #     return self.os_endpoint

    def get_rds_endpoint(self, **kwargs):
        """Return RDS propriatary endpoint

        """
        return self.get_endpoint(service_type='rds')
        # endpoint = super(Proxy, self).get_endpoint(**kwargs)
        # endpoint_override = self.endpoint_override
        # if endpoint.endswith('/rds/v1') and not endpoint_override:
        #     return endpoint
        # elif endpoint_override:
        #     _logger.debug('RDS endpoint_override is set. Return it')
        #     return endpoint_override
        # else:
        #     return endpoint

    def get_os_headers(self, language=None):
        """Get headers for request

        Unfortunatels RDS requires 'Content-Type: application/json'
        header even for GET and LIST operations with empty body
        We need to deel with it

        :param language: whether language should be added to headers
            can be either bool (then self.get_language is used)
            or a language code directly (i.e. "en-us")
        :returns dict: dictionary with headers
        """
        headers = {
            'Content-Type': 'application/json',
        }
        if language:
            if isinstance(language, bool):
                headers['X-Language'] = self.get_language()
            elif isinstance(language, str):
                headers['X-Language'] = language
        return headers

    def get_language(self):
        """Returns language code

        """
        return 'en-us'

    # ======= Datastores =======
    def datastore_types(self):
        """List supported datastore types

        :returns: A generator of supported datastore types
        :rtype object: object with name attribte
        """
        for ds in ['MySQL', 'PostgreSQL', 'SQLServer']:
            obj = type('obj', (object,), {'name': ds})
            yield obj

        return

    def datastore_versions(self, datastore):
        """List datastores

        :param dbId: database store name
            (MySQL, PostgreSQL, or SQLServer and is case-sensitive.)

        :returns: A generator of datastore versions
        :rtype: :class:`~otcextensions.sdk.rds.v1.flavor.Flavor`
        """
        return self._list(
            _datastore.Datastore,
            paginated=False,
            endpoint_override=self.get_rds_endpoint(),
            headers=self.get_os_headers(True),
            project_id=self.session.get_project_id(),
            datastore_name=datastore
        )

    def get_datastore_version(self, datastore, datastore_version):
        """Get the detail of a datastore version

        :param datastore: datastore name
        :param datastore_Version: id of the datastore version
        :returns: Detail of datastore version
        :rtype: :class:`~otcextensions.sdk.rds.v1.datastore.Datastore`
        """
        versions = self._list(
            _datastore.Datastore,
            paginated=False,
            endpoint_override=self.get_rds_endpoint(),
            headers=self.get_os_headers(True),
            project_id=self.session.get_project_id(),
            datastore_name=datastore
        )
        for ver in versions:
            if ver.id == datastore_version:
                return ver
        return exceptions.NotFoundException('Resource not found')

    # ======= Flavors =======
    def flavors(self):
        """List flavors of given datastore id and region

        :param dbId: database store id
        :param region: region

        :returns: A generator of flavor
        :rtype: :class:`~otcextensions.sdk.rds_os.v1.flavor.Flavor`
        """
        return self._list(_flavor.Flavor, paginated=False,
                          # endpoint_override=self.get_os_endpoint(),
                          # headers=self.get_os_headers(),
                          project_id=self.session.get_project_id())

    def get_flavor(self, flavor):
        """Get the detail of a flavor

        :param id: Flavor id or an object of class
                   :class:`~otcextensions.sdk.rds_os.v1.flavor.Flavor`
        :returns: Detail of flavor
        :rtype: :class:`~otcextensions.sdk.rds_os.v1.flavor.Flavor`
        """
        return self._get(
            _flavor.Flavor,
            flavor,
            project_id=self.session.get_project_id(),
            # endpoint_override=self.get_os_endpoint(),
            # headers=self.get_os_headers(),
        )

    def find_flavor(self, name_or_id, ignore_missing=True):
        """Find a single flavor

        :param name_or_id: The name or ID of a flavor.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~otcextensions.sdk.rds.v1.flavor.Flavor`
                  or None
        """
        return self._find(_flavor.Flavor, name_or_id,
                          project_id=self.session.get_project_id(),
                          # endpoint_override=self.get_os_endpoint(),
                          # headers=self.get_os_headers(),
                          ignore_missing=ignore_missing)

    # ======= Instance =======
    def create_instance(self, **attrs):
        """Create a new instance from attributes

        :param dict attrs: Keyword arguments which will be used to create
                   a :class:`~otcextensions.sdk.rds.v1.instance.Instance`,
                   comprised of the properties on the Instance class.

        :returns: The results of server creation
        :rtype: :class:`~otcextensions.sdk.rds.v1.instance.Instance`
        """
        return self._create(_instance.Instance,
                            project_id=self.session.get_project_id(),
                            # endpoint_override=self.get_os_endpoint(),
                            # headers=self.get_os_headers(),
                            **attrs)

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
        self._delete(
            _instance.Instance, instance,
            ignore_missing=ignore_missing,
            project_id=self.session.get_project_id(),
            # endpoint_override=self.get_os_endpoint(),
            # headers=self.get_os_headers()
        )

    def find_instance(self, name_or_id, ignore_missing=True):
        """Find a single instance

        :param name_or_id: The name or ID of a instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~otcextensions.sdk.rds.v1.instance.Instance`
                  or None
        """
        return self._find(_instance.Instance, name_or_id,
                          project_id=self.session.get_project_id(),
                          # endpoint_override=self.get_os_endpoint(),
                          # headers=self.get_os_headers(),
                          ignore_missing=ignore_missing)

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
            # endpoint_override=self.get_os_endpoint(),
            # headers=self.get_os_headers(),
        )

    def instances(self):
        """Return a generator of instances

        :returns: A generator of instance objects
        :rtype: :class:`~otcextensions.sdk.rds.v1.instance.Instance`
        """
        return self._list(
            _instance.Instance, paginated=False,
            project_id=self.session.get_project_id(),
            # endpoint_override=self.get_os_endpoint(),
            # headers=self.get_os_headers(),
        )

    def update_instance(self, instance, **attrs):
        """Update a instance

        :param instance: Either the id of a instance or a
                         :class:`~otcextensions.sdk.rds.v1.instance.Instance`
                         instance.
        :attrs attrs: The attributes to update on the instance represented
                       by ``value``.

        :returns: The updated instance
        :rtype: :class:`~otcextensions.sdk.rds.v1.instance.Instance`
        """
        return self._update(
            _instance.Instance,
            instance=instance,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_rds_endpoint(),
            headers=self.get_os_headers(True),
            **attrs
        )

    # ======= Configurations =======
    def configurations(self, **attrs):
        """Obtaining a ConfigurationGroup List

        :returns: A generator of ConfigurationGroup object
        :rtype:
            :class:`~otcextensions.sdk.rds.v1.configuration.ConfigurationGroup`
        """
        return self._list(
            _configuration.ConfigurationGroup,
            paginated=False,
            project_id=self.session.get_project_id(),
            # endpoint_override=self.get_os_endpoint(),
            # headers=self.get_os_headers(),
        )

    def get_configuration(self, cg):
        """Obtaining a ConfigurationGroup

        :param parameter_group: The value can be the ID of a ConfigurationGroup
            or a object of
            :class:`~otcextensions.sdk.rds.v1.configuration.ConfigurationGroup`.

        :returns: A Parameter Group Object
        :rtype: :class:`~otcextensions.rds.v1.configuration.ConfigurationGroup`
        """
        return self._get(
            _configuration.ConfigurationGroup,
            cg,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_os_endpoint(),
            headers=self.get_os_headers(True)
        )

    def create_configuration(self, **attrs):
        """Creating a ConfigurationGroup

        :param dict \*\*attrs: Dict to overwrite ConfigurationGroup object
        :returns: A Parameter Group Object
        :rtype:
            :class:`~otcextensions.sdk.rds.v1.configuration.ConfigurationGroup`
        """
        return self._create(_configuration.ConfigurationGroup,
                            project_id=self.session.get_project_id(),
                            # endpoint_override=self.get_os_endpoint(),
                            # headers=self.get_os_headers(),
                            **attrs)

    def delete_configuration(self, cg, ignore_missing=True):
        """Deleting a ConfigurationGroup

        :param cg: The value can be the ID of a ConfigurationGroup or a
            object of
            :class:`~otcextensions.sdk.rds.v1.configuration.ConfigurationGroup`.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the Parameter Group does not exist.
            When set to ``True``, no exception will be set when
            attempting to delete a nonexistent Parameter Group.

        :returns: None
        :rtype: None
        """
        self._delete(
            _configuration.ConfigurationGroup, cg,
            ignore_missing=ignore_missing,
            project_id=self.session.get_project_id(),
            # endpoint_override=self.get_os_endpoint(),
            # headers=self.get_os_headers()
        )

    def find_configuration(self, name_or_id, ignore_missing=True):
        """Find a ConfigurationGroup

        :param parameter_group: The value can be the ID of a ConfigurationGroup
            or a object of
            :class:`~otcextensions.sdk.rds.v1.configuration.Configurations`.
        :returns: A Parameter Group Object
        :rtype:
            :class:`~otcextensions.rds.v1.configuration.ConfigurationGroup`.
        """
        return self._find(_configuration.ConfigurationGroup, name_or_id,
                          project_id=self.session.get_project_id(),
                          # endpoint_override=self.get_os_endpoint(),
                          # headers=self.get_os_headers(),
                          ignore_missing=ignore_missing)

    # ======= Backups =======
    def backups(self):
        """List Backups

        :returns: A generator of backup
        :rtype: :class:`~otcextensions.sdk.rds.v1.backup.Backup`
        """
        return self._list(
            _backup.Backup, paginated=False,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_rds_endpoint(),
            headers=self.get_os_headers(True)
        )

    def create_backup(self, instance, **attrs):
        """Create a backups of instance

        :returns: A new backup object
        :rtype: :class:`~otcextensions.sdk.rds.v1.backup.Backup`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return self._create(
            _backup.Backup,
            instance_id=instance.id,
            project_id=self.session.get_project_id(),
            endpoint_override=self.get_rds_endpoint(),
            headers=self.get_os_headers(True),
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
            headers=self.get_os_headers(True),
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
            headers=self.get_os_headers(True),
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
            headers=self.get_os_headers(True),
            **attrs)
