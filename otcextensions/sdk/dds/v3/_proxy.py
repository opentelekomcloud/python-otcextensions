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
from openstack import resource

from otcextensions.sdk.dds.v3 import datastore as _datastore
from otcextensions.sdk.dds.v3 import flavor as _flavor
from otcextensions.sdk.dds.v3 import instance as _instance
from otcextensions.sdk.dds.v3 import job as _job
from otcextensions.sdk.dds.v3 import eip as _eip
from otcextensions.sdk.dds.v3 import recycle_policy as _recycle_policy
from otcextensions.sdk.dds.v3 import recycle_instance as _recycle_instance


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

        :param datastore_name: database store name
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

        :returns: job ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.restart(self)

    def enlarge_instance(self, instance, size, group_id=None):
        """Enlarge storage space of a DB instance

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param size: New instance size.
        :param group_id: ID of the group to enlarge storage space.
        :returns: job ID.

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
        :returns: job ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.add_nodes(self, **attrs)

    def resize_instance(self, instance, **attrs):
        """Change specifications of a DB instance

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param dict attrs: Keyword arguments which will be used to add node to
        a :class:`~otcextensions.sdk.dds.v3.instance.Instance`.
        :returns: job ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.resize(self, **attrs)

    def switchover_instance(self, instance):
        """Perform a primary/secondary switchover in a replica set instance.

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :returns: job ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.switchover(self)

    def enable_instance_ssl(self, instance, enable=True):
        """Enable SSL in a replica set instance.

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param bool enable: enable or disable
        :returns: job ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.switch_ssl(self, enable)

    def change_instance_name(self, instance, name):
        """Change name of a DB instance

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param name: New name of an instance

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        instance.modify_name(self, name)

    def change_instance_port(self, instance, port):
        """Change port of a DB instance

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param port: New port of an instance
        :returns: DB instance object.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.change_port(self, port)

    def change_instance_security_group(self, instance, security_group_id):
        """Change security group of a DB instance

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param security_group_id: New security group ID
        :returns: job ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.change_security_group(self, security_group_id)

    def change_instance_private_ip(self, instance, **attrs):
        """Change private IP of a DB instance

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param dict attrs: Keyword arguments which will be used to change ip.
        :returns: job ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.change_private_ip(self, **attrs)

    def create_instance_ip(self, instance, **attrs):
        """Add IP for a DB instance

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.
        :param dict attrs: Keyword arguments which will be used to add ip
        :returns: workflow ID.

        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.create_ip(self, **attrs)

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

    def wait_job(self, job, status='Completed', failures=None,
                 interval=20, wait=None):
        """Wait for the job to complete

        :param job: The value can be either the ID of a job or a
        :param status: Desired status of the job.
        :param failures: List of failure statuses.
        :param interval: Seconds to wait between retries.
        :param wait: Seconds to wait for response.

        :returns: One :class:`~otcextensions.sdk.dds.v3.job.Job`
        """
        if failures is None:
            failures = ['ERROR']
        job = self._find(_job.Job, job, failures=failures)
        if job is not None:
            return resource.wait_for_status(self, job, status, failures,
                                            interval, wait)

    def wait_normal_instance(self, instance, status='normal',
                             failures=None, interval=60, wait=None):
        """Wait for normal status of an instance

        :param instance: The value can be either the ID of an instance or a
        :class:`~otcextensions.sdk.dds.v3.instance.Instance` instance.

        :param status: The status of the instance to wait for.
        :param failures: The list of failures.
        :param interval: The number of seconds to wait between failures.
        :param wait: Seconds to wait for response.

        :returns: One :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """
        if failures is None:
            failures = ['ERROR']
        instance = self.get_instance(instance)
        return resource.wait_for_status(self, instance, status,
                                        failures, interval, wait)

    def bind_eip(self, node, public_ip, public_ip_id):
        """Bind an IP to a node

        :param node: The value is the ID of a node
        :param public_ip: The public IP address of the node.
        :param public_ip_id: The public IP address of the node.

        :returns: The IP address of the node.
        """
        eip = _eip.Eip()
        return eip.bind(self, node, public_ip, public_ip_id)

    def unbind_eip(self, node):
        """Unbind an IP to a node

        :param node: The value is the ID of a node

        :returns: The ID of the node.
        """
        eip = _eip.Eip()
        return eip.unbind(self, node)

    def get_policy(self):
        """Get the current policy

        :returns: The current policy.
        """
        return self._get(_recycle_policy.RecyclePolicy, requires_id=False)

    def create_policy(self, **attrs):
        """Create a new policy from attributes

        :param dict attrs: Keyword arguments which will be used to create
        a :class:`~otcextensions.sdk.dds.v3.recycle_policy.RecyclePolicy`,
        comprised of the properties on the RecyclePolicy class.

        :returns: The result of creation.

        :rtype: :class:`~otcextensions.sdk.dds.v3.recycle_policy.RecyclePolicy`
        """
        return self._create(_recycle_policy.RecyclePolicy, **attrs)

    def recycle_instances(self, **params):
        """Get list of instances in recycle bin

        :param dict params: Keyword arguments which will be used to get list
        :returns: A generator of recycle instance objects.
        """
        base_path = _recycle_instance.RecycleInstance.base_path
        return self._list(_recycle_instance.RecycleInstance, **params,
                          base_path=base_path)
