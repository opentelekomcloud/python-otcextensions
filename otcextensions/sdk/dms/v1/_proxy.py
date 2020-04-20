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

from otcextensions.sdk.dms.v1 import group as _group
from otcextensions.sdk.dms.v1 import instance as _instance
from otcextensions.sdk.dms.v1 import message as _message
from otcextensions.sdk.dms.v1 import queue as _queue


class Proxy(proxy.Proxy):

    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            'Content-Type': 'application/json',
        }

    # ======== Queues ========
    def create_queue(self, **kwargs):
        """Create a queue

        :param dict kwargs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        """
        return self._create(_queue.Queue, **kwargs)

    def queues(self, **kwargs):
        """List all queues

        :param dict kwargs: List of query parameters

        :returns: A generator of Queue object of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        """
        return self._list(_queue.Queue, paginated=False, **kwargs)

    def find_queue(self, name_or_id):
        """Find queue by name or id

        :param name_or_id: Name or ID
        :returns: one object of class
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        """
        return self._find(_queue.Queue, name_or_id)

    def get_queue(self, queue):
        """Get detail about a given queue id

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :returns: one object of class
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        """
        return self._get(_queue.Queue, queue)

    def delete_queue(self, queue, ignore_missing=True):
        """Delete queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.exceptions.ResourceNotFound` will be
            raised when the queue does not exist.
        :returns: `None`
        """

        self._delete(_queue.Queue, queue, ignore_missing=ignore_missing)

    # ======== Groups ========
    def create_group(self, queue, name):
        """Create a list consume groups for a queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param str name: Group name to create
        :returns: A list of object
            :class:`~otcextensions.sdk.dms.v1.queue.Group`
        """
        queue_obj = self._get_resource(_queue.Queue, queue)

        return self._create(_group.Group, queue_id=queue_obj.id, name=name)

    def groups(self, queue, **kwargs):
        """List all groups for a given queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param dict kwargs: Query parameters

        :returns: A generator of Group object
        :rtype: :class:`~otcextensions.sdk.dms.v1.queue.Group`
        """
        queue_obj = self._get_resource(_queue.Queue, queue)

        return self._list(_group.Group,
                          queue_id=queue_obj.id,
                          paginated=False,
                          **kwargs)

    def find_group(self, queue, name_or_id, ignore_missing=False):
        """Find group by name or id

        :param queue: Queue name or object
        :param name_or_id: Name or ID
        :param ignore_missing:
        :returns: one object of class
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        """
        queue_obj = self._get_resource(_queue.Queue, queue)
        return self._find(_group.Group, name_or_id,
                          ignore_missing=ignore_missing,
                          queue_id=queue_obj.id)

    def delete_group(self, queue, group, ignore_missing=True):
        """Delete a consume on the queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param group: The consume group id or an instance of
            :class:`~otcextensions.sdk.dms.v1.group.Group`
        :returns: ``None``
        """
        queue_obj = self._get_resource(_queue.Queue, queue)

        self._delete(_group.Group, group, queue_id=queue_obj.id,
                     ignore_missing=ignore_missing)

    # ======== Messages ========
    def send_messages(self, queue, messages, return_id=False, **kwargs):
        """Send messages for a given queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param list messages: A list of message dictionaries
        :returns: Messages holder instance
            :class:`otcextensions.sdk.dms.v1.message.Messages`
        """
        queue_obj = self._get_resource(_queue.Queue, queue)
        messages_list = list()
        for msg in messages:
            if not isinstance(msg, _message.Message):
                obj = _message.Message(**msg)
            else:
                obj = msg
            messages_list.append(obj.to_dict(computed=False, ignore_none=True))

        return self._create(_message.Messages,
                            base_path='/queues/%(queue_id)s/messages',
                            queue_id=queue_obj.id,
                            messages=messages_list,
                            return_id=return_id)

    def send_message(self, queue, return_id=True, body=None, **attrs):
        """Send single message into a given queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param bool return_id: Whether response should contain message id
        :param body: A str/json object representing message body
        :param dict attr: Additional message attributes
        :returns: Messages holder instance
            :class:`otcextensions.sdk.dms.v1.message.Message`
        """
        queue_obj = self._get_resource(_queue.Queue, queue)
        msg = _message.Message(body=body, **attrs)

        return self._create(_message.Messages,
                            base_path='/queues/%(queue_id)s/messages',
                            queue_id=queue_obj.id,
                            messages=[msg.to_dict(computed=False,
                                                  ignore_none=True)],
                            return_id=return_id).messages[0]

    def consume_message(self, queue, group, **query):
        """Consume queue's message

        :param queue: The queue id or an instance of
          :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param consume_group: The consume group id or an instance of
          :class:`~otcextensions.sdk.dms.v1.group.Group`
        :param kwargs query: Optional query parameters to be sent to limit
          the resources being returned.
        :returns: A list of object
          :class:`~otcextensions.sdk.dms.v1.group_message.GroupMessage`
        """
        queue_obj = self._get_resource(_queue.Queue, queue)
        group_obj = self._get_resource(_group.Group, group)

        return self._list(
            _message.Message,
            base_path='/queues/%(queue_id)s/groups/%(group_id)s/messages',
            queue_id=queue_obj.id,
            group_id=group_obj.id,
            **query)

    def ack_message(self, queue, group, messages, status='success'):
        """Confirm consumed message

        :param consumed_message: An object of an instance of
          :class:`~otcextensions.sdk.dms.v1.group_message.GroupMessage
        :param status: The expeced status of the consumed message
        :returns: An object of an instance of
          :class:`~otcextensions.sdk.dms.v1.group_message.GroupMessage`
        """
        queue_obj = self._get_resource(_queue.Queue, queue)
        group_obj = self._get_resource(_group.Group, group)

        return group_obj.ack(self, queue_obj, messages, status=status)

    # ======== Instances =======
    def instances(self, **kwargs):
        """List all DMS Instances

        :param dict kwargs: List of query parameters

        :returns: A generator of Instance object of
            :class:`~otcextensions.sdk.dms.v1.instance.Instance`
        """
        return self._list(_instance.Instance, paginated=False, **kwargs)

    def create_instance(self, **attrs):
        """Create an DMS instance

        :param dict attrs: instance attributes
            :class:`~otcextensions.sdk.dms.v1.instance.Instance`
        :returns: An instance class object
            :class:`~otcextensions.sdk.dms.v1.instance.Instance`
        """
        return self._create(_instance.Instance, **attrs)

    def delete_instance(self, instance, ignore_missing=True):
        """Delete DMS Instance

        :param instance: The instance id or an object instance of
            :class:`~otcextensions.sdk.dms.v1.instance.Instance`
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.exceptions.ResourceNotFound` will be
            raised when the instance does not exist.
        :returns: `None`
        """
        self._delete(_instance.Instance, instance,
                     ignore_missing=ignore_missing)

    def find_instance(self, name_or_id, ignore_missing=False):
        """Find DMS Instance by name or id

        :param name_or_id: Name or ID
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.exceptions.ResourceNotFound` will be
            raised when the instance does not exist.

        :returns: one object of class
            :class:`~otcextensions.sdk.dms.v1.instance.Instance`
        """
        return self._find(_instance.Instance, name_or_id,
                          ignore_missing=ignore_missing)

    def get_instance(self, instance):
        """Get detail about a given instance id

        :param instance: The instance id or an instance of
            :class:`~otcextensions.sdk.dms.v1.instance.Instance`
        :returns: one object of class
            :class:`~otcextensions.sdk.dms.v1.instance.Instance`
        """
        return self._get(_instance.Instance, instance)

    def update_instance(self, instance, **attrs):
        """Update an Instance

        :param instance: Either the ID of an instance or a
            :class:`~otcextensions.sdk.dms.v1.instance.Instance` instance.
        :param dict attrs: The attributes to update on the instance
            represented by ``value``.

        :returns: The updated instance
        :rtype: :class:`~otcextensions.sdk.dms.v1.instance.Instance`
        """
        return self._update(_instance.Instance, instance,
                            **attrs)

    def restart_instance(self, instance):
        """Restart instance

        :param instance: Either the ID of an instance or a
            :class:`~otcextensions.sdk.dms.v1.instance.Instance` instance.
        """
        instance = self._get_resource(_instance.Instance, instance)
        return instance.restart(self)

    def restart_instances(self, instances_list):
        """Restart multiple instances
        """
        dummy_instance = _instance.Instance()
        return dummy_instance.restart_batch(self, instances_list)

    def delete_batch(self, instances_list):
        """Delete multiple instances
        """
        dummy_instance = _instance.Instance()
        return dummy_instance.delete_batch(self, instances_list)

    def delete_failed(self):
        """Delete failed Kafka instances
        """
        dummy_instance = _instance.Instance()
        return dummy_instance.delete_failed(self)

#    def quotas(self):
#        """List quota
#
#        :returns: A generator of Quota object
#        :rtype: :class:`~otcextensions.sdk.dms.v1.quota.Quota`
#        """
#        return self._list(_quota.Quota)
