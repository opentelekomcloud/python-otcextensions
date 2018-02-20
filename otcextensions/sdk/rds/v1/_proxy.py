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
from openstack import proxy
from openstack import utils

# from openstack import exception

# from otcextensions.sdk.rds.v1 import configuration as _configuration
# from otcextensions.sdk.rds.v1 import datastore as _datastore
from otcextensions.sdk.rds.v1 import datastore as _datastore
from otcextensions.sdk.rds.v1 import flavor as _flavor
from otcextensions.sdk.rds.v1 import instance as _instance
# from otcextensions.sdk.rds.v1 import instance as _instance

_logger = _log.setup_logging('openstack')


class Proxy(proxy.BaseProxy):

    def _fix_endpoint(self, **kwargs):
        """Check if edpoint is broken

        """
        self.endpoint_override = self.get_endpoint(**kwargs)
        # endpoint = super(Proxy, self).get_endpoint(**kwargs)
        # endpoint_override = self.endpoint_override
        # if endpoint.endswith('/rds/v1') and not endpoint_override:
        #     _logger.debug('fixing endpoint')
        #     endpoint_override = endpoint.rstrip('/rds/v1')
        #     endpoint_override = utils.urljoin(endpoint_override, 'v1.0')
        #     self.endpoint_override = endpoint_override

    def get_endpoint(self, **kwargs):
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

    def get_rds_endpoint(self):
        """Return OpenStack compliant endpoint

        """
        endpoint = self.get_endpoint()
        endpoint_override = self.endpoint_override
        if endpoint.endswith('/rds/v1'):
            return endpoint
        else:
            _logger.debug('RDS endpoint_override is set. Return it')
            return endpoint_override

    def datastores(self, db_name):
        """List datastores

        :param dbId: database store name
            (MySQL, PostgreSQL, or SQLServer and is case-sensitive.)

        :returns: A generator of datastore versions
        :rtype: :class:`~openstack.rds_os.v1.flavor.Flavor
        """
        # self.check_endpoint()
        headers = {
            'Content-Type': 'application/json',
            'X-Language': 'en-us'
        }
        return self._list(_datastore.Datastore, paginated=False,
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
        :rtype: :class:`~openstack.rds_os.v1.flavor.Flavor
        """
        self._fix_endpoint()
        return self._list(_flavor.Flavor, paginated=False,
                          # endpoint_override=self.get_os_endpoint(),
                          project_id=self.session.get_project_id())

    def get_flavor(self, flavor):
        """Get the detail of a flavor

        :param id: Flavor id or an object of class
                   :class:`~openstack.rds_os.v1.flavor.Flavor
        :returns: Detail of flavor
        :rtype: :class:`~openstack.rds_os.v1.flavor.Flavor
        """
        self._fix_endpoint()
        self.additional_headers['Content-Type'] = 'application/json'
        return self._get(
            _flavor.Flavor,
            flavor,
            project_id=self.session.get_project_id()
        )

    def find_flavor(self, name_or_id, ignore_missing=True):
        raise NotImplementedError

    def create_instance(self, **attrs):
        """Create a new instance from attributes

        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~openstack.database.v1.instance.Instance`,
                           comprised of the properties on the Instance class.

        :returns: The results of server creation
        :rtype: :class:`~openstack.database.v1.instance.Instance`
        """
        raise NotImplementedError
        return self._create(_instance.Instance, **attrs)

    def delete_instance(self, instance, ignore_missing=True):
        """Delete an instance

        :param instance: The value can be either the ID of an instance or a
               :class:`~openstack.database.v1.instance.Instance` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the instance does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent instance.

        :returns: ``None``
        """
        raise NotImplementedError
        self._delete(_instance.Instance, instance,
                     ignore_missing=ignore_missing)

    def find_instance(self, name_or_id, ignore_missing=True):
        """Find a single instance

        :param name_or_id: The name or ID of a instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~openstack.database.v1.instance.Instance` or None
        """
        raise NotImplementedError
        return self._find(_instance.Instance, name_or_id,
                          ignore_missing=ignore_missing)

    def get_instance(self, instance):
        """Get a single instance

        :param instance: The value can be the ID of an instance or a
                         :class:`~openstack.database.v1.instance.Instance`
                         instance.

        :returns: One :class:`~openstack.database.v1.instance.Instance`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        self._fix_endpoint()
        # self.additional_headers['Content-Type'] = 'application/json'
        return self._get(
            _instance.Instance,
            instance,
            project_id=self.session.get_project_id()
        )
        # raise NotImplementedError
        # return self._get(_instance.Instance, instance)

    def instances(self):
        """Return a generator of instances

        :returns: A generator of instance objects
        :rtype: :class:`~openstack.database.v1.instance.Instance`
        """
        self._fix_endpoint()
        return self._list(_instance.Instance, paginated=False,
                          project_id=self.session.get_project_id())

    def update_instance(self, instance, **attrs):
        """Update a instance

        :param instance: Either the id of a instance or a
                         :class:`~openstack.database.v1.instance.Instance`
                         instance.
        :attrs kwargs: The attributes to update on the instance represented
                       by ``value``.

        :returns: The updated instance
        :rtype: :class:`~openstack.database.v1.instance.Instance`
        """
        raise NotImplementedError
        return self._update(_instance.Instance, instance, **attrs)
