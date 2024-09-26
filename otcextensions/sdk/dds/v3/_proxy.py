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
from otcextensions.sdk.dds.v3 import job as _job

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

    def restart_instance(self, instance):
        """Restart an existing instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.

        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.restart(self)

    def enlarge_instance(self, instance, size, group_id=None):
        """Enlarge storage space of a DB instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param size: New instance size.
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self.get_instance(instance)
        return instance.enlarge(self, size, group_id)

    def add_instance_nodes(self, instance, **attrs):
        """Add nodes for a specific instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param dict attrs: Keyword arguments which will be used to add node to
            a :class:`~otcextensions.sdk.dds.v3.instance.Instance`.
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.add_nodes(self, **attrs)

    def resize_instance(self, instance, *attrs):
        """Change specifications of a DB instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param dict attrs: Keyword arguments which will be used to add node to
            a :class:`~otcextensions.sdk.dds.v3.instance.Instance`.
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.resize(self, *attrs)

    def switchover_instance(self, instance):
        """Perform a primary/secondary switchover in a replica set instance.

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.switchover(self)

    def enable_instance_ssl(self, instance, enable=True):
        """Perform a primary/secondary switchover in a replica set instance.

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param bool enable: Perform a primary/secondary switchover
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.switch_ssl(self, enable)

    def change_instance_name(self, instance, name):
        """Change name of a DB instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param name: New name of an instance
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.modify_name(self, name)

    def change_instance_port(self, instance, port):
        """Change name of a DB instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param port: New port of an instance
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.change_port(self, port)

    def change_instance_security_group(self, instance, security_group_id):
        """Change security group of a DB instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param security_group_id: New security group ID
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.change_security_group(self, security_group_id)

    def change_instance_private_ip(self, instance, *attrs):
        """Change private IP of a DB instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param dict attrs: Keyword arguments which will be used to change ip.
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.change_private_ip(self, *attrs)

    def create_instance_ip(self, instance, *attrs):
        """Add config for a DB instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param dict attrs: Keyword arguments which will be used to add ip
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.create_ip(self, *attrs)

    def configure_client_network(self, instance, network_ranges):
        """Configure client network of a DB instance
        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param list network_ranges: List of network ranges
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.configure_client_network(self, network_ranges)

    def set_recycle_bin_policy(self, instance, *attrs):
        # TODO: измени ссылку запроса
        """Set the recycle bin policy for an instance.

        :param instance: The value can be either the ID of an instance or a
                    :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param dict attrs: Keyword arguments which will be used to set policy
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.set_recycle_bin_policy(self, *attrs)
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

    def get_job(self, job):
        """Get information about a job

        :param job: The value can be either the ID of a job or a
            :class:`~otcextensions.sdk.dds.v3.job.Job` job.

        :returns: One :class:`~otcextensions.sdk.dds.v3.job.Job`
        """
        return self._get(_job.Job, job)