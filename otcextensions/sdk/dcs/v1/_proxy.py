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

# from openstack import proxy
from otcextensions.sdk import sdk_proxy
from otcextensions.sdk.dcs.v1 import instance as _instance
from otcextensions.sdk.dcs.v1 import statistic as _stat


class Proxy(sdk_proxy.Proxy):

    # ======== Instances ========
    def create_instance(self, **kwargs):
        """Create an instance

        :param dict kwargs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        return self._create(_instance.Instance, **kwargs)

    def instances(self, **query):
        """List all cache instances

        :returns: A generator of Instance object of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        return self._list(_instance.Instance, paginated=False, **query)

    def get_instance(self, instance):
        """Get detail about a given instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: one object of class
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        return self._get(_instance.Instance, instance)

    def find_instance(self, name_or_id, ignore_missing=False):
        """Find instance by name or id

        :param name_or_id: The instance id or name of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: one object of class
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        return self._find(_instance.Instance, name_or_id,
                          ignore_missing=ignore_missing)

    def update_instance(self, instance, **attrs):
        """Update instance with attributes

        :param instance: The value can be the ID of an instance
            or a :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
            instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dcs.v1.instance.Instance`,
            comprised of the properties on the Instance class.
        :returns: The updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self._get_resource(_instance.Instance, instance, **attrs)
        res = res.update(
            self,
            has_body=False
        )
        # NOTE: unfortunately we need to refetch object, since update
        # does not return it
        return self._get(_instance.Instance, res)

    def delete_instance(self, instance, ignore_missing=True):
        """Delete an instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.exceptions.ResourceNotFound` will be
            raised when the queue does not exist.
        :returns: `None`
        """
        self._delete(_instance.Instance, instance,
                     ignore_missing=ignore_missing)

    def extend_instance(self, instance, capacity):
        """Extend capacity of existing instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :param int capacity: New instance capacity
        :returns: Updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self._get_resource(_instance.Instance, instance)
        res.extend(self, capacity)
        return self._get(_instance.Instance, res)

    def stop_instance(self, instance):
        """Stop existing instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: Updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self.find_instance(instance)
        res.stop(self)
        return self._get(_instance.Instance, res)

    def start_instance(self, instance):
        """Start existing instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: Updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self.find_instance(instance)
        res.start(self)
        return self._get(_instance.Instance, res)

    def restart_instance(self, instance):
        """Retart existing instance

        :param instance: The instance id, name or an instance of
            :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        :returns: Updated instance
        :rtype: :class:`~otcextensions.sdk.dcs.v1.instance.Instance`
        """
        res = self.find_instance(instance)
        res.restart(self)
        return self._get(_instance.Instance, res)

    # ======== Misc ========
    def statistics(self):
        """Query statisctics for all instances

        :returns: A generator of Instance object of
            :class:`~otcextensions.sdk.dcs.v1.stat.Statistics`
        """
        return self._list(_stat.Statistic, paginated=False)
