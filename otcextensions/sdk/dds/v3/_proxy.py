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

from otcextensions.sdk.dds.v3 import datastore as _datastore
from otcextensions.sdk.dds.v3 import flavor as _flavor
from otcextensions.sdk.dds.v3 import instance as _instance


class Proxy(proxy.Proxy):
    skip_discovery = True

    # ======= Datastores =======
    def datastore_types(self):
        """List supported datastore types

        :returns: A generator of supported datastore types
        """
        for ds in ['DDS-Community']:
            obj = type('obj', (object,), {'name': ds})
            yield obj

    def datastores(self, datastore_name):
        """List datastores

        :param database_name: database store name
            (currently only DDS-Community and is case-sensitive.)

        :returns: A generator of supported datastore versions.

        :rtype: :class:`~otcextensions.sdk.dds.v3.datastore.Datastore`
        """
        return self._list(
            _datastore.Datastore,
            datastore_name=datastore_name,
        )

    # ======= Flavors =======
    def flavors(self, region, engine_name):
        """List flavors of all DB instances specifications in specified region

        :param engine_name: database engine name
        :param region: region

        :returns: A generator of flavor
        :rtype: :class:`~otcextensions.sdk.dds.v3.flavor.Flavor`
        """

        return self._list(
            _flavor.Flavor,
            region=region,
            engine_name=engine_name
        )

    # ======= Instance =======
    def create_instance(self, **attrs):
        """Create a new instance from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dds.v3.instance.Instance`,
            comprised of the properties on the Instance class.

        :returns: The result of an instance creation.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        return self._create(_instance.Instance, **attrs)

    def delete_instance(self, instance, ignore_missing=True):
        """Delete an instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
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
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.

        :returns: One :class:`~otcextensions.sdk.dds.v3.instance.Instance`
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
            One :class:`~otcextensions.sdk.dds.v3.instance.Instance` or None.
        """
        return self._find(_instance.Instance,
                          name_or_id,
                          ignore_missing=ignore_missing)

    def instances(self, **params):
        """Return a generator of instances

        :param dict params: Optional query parameters to be sent to limit
            the instances being returned.

        :returns: A generator of instance objects.
        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        return self._list(_instance.Instance, **params)
