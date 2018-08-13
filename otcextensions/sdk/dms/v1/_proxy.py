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

from otcextensions.sdk import sdk_proxy
from otcextensions.sdk.dms.v1 import queue as _queue
from otcextensions.sdk.dms.v1 import quota as _quota
from otcextensions.sdk.dms.v1 import group as _group
from otcextensions.sdk.dms.v1 import message as _message
from otcextensions.sdk.dms.v1 import group_message as _group_message


class Proxy(sdk_proxy.Proxy):

    # ======== Queues ========
    def create_queue(self, **kwargs):
        """Create a queue

        :param dict kwargs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        """
        return self._create(_queue.Queue, **kwargs)

    def queues(self):
        """List all queues

        :returns: A generator of Queue object of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        """
        return self._list(_queue.Queue, paginated=False)

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
    def create_group(self, queue, group):
        """Create a list consume groups for a queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param dict kwargs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.dms.v1.queue.Group`
        :returns: A list of object
            :class:`~otcextensions.sdk.dms.v1.queue.Group`
        """

        queue_id = queue
        if isinstance(queue, _queue.Queue):
            queue_id = queue.id

        # Use a dummy group first to have control over create request
        res = _group.Group.new(queue_id=queue_id)

        return res.create(self, group=group)

    def groups(self, queue, include_deadletter=False):
        """List all groups for a given queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :returns: A generator of Group object
        :rtype: :class:`~otcextensions.sdk.dms.v1.queue.Group`
        """
        queue_id = queue
        if isinstance(queue, _queue.Queue):
            queue_id = queue.id

        return self._list(_group.Group,
                          queue_id=queue_id,
                          include_deadletter=include_deadletter,
                          paginated=False)

    def delete_group(self, queue, group):
        """Delete a consume on the queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param group: The consume group id or an instance of
            :class:`~otcextensions.sdk.dms.v1.group.Group`
        :returns: ``None``
        """
        queue_id = queue
        if isinstance(queue, _queue.Queue):
            queue_id = queue.id

        self._delete(_group.Group, group, queue_id=queue_id)

    # ======== Messages ========
    def send_messages(self, queue, **kwargs):
        """Send messages for a given queue

        :param queue: The queue id or an instance of
            :class:`~otcextensions.sdk.dms.v1.queue.Queue`
        :param dict kwargs: Keyword to create messages
        :returns: dict
        """
        queue_id = queue
        if isinstance(queue, _queue.Queue):
            queue_id = queue.id

        return self._create(_message.Message, queue_id=queue_id, **kwargs)

    def consume_message(self, queue, consume_group, **query):
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
        queue_id = queue
        if isinstance(queue, _queue.Queue):
            queue_id = queue.id
        consumer_group_id = consume_group
        if isinstance(consume_group, _group.Group):
            consumer_group_id = consume_group.id

        return self._list(
            _group_message.GroupMessage,
            queue_id=queue_id,
            consumer_group_id=consumer_group_id,
            **query)

    def ack_consumed_message(self, consumed_message, status='success'):
        """Confirm consumed message

        :param consumed_message: An object of an instance of
          :class:`~otcextensions.sdk.dms.v1.group_message.GroupMessage
        :param status: The expeced status of the consumed message
        :returns: An object of an instance of
          :class:`~otcextensions.sdk.dms.v1.group_message.GroupMessage`
        """
        return consumed_message.ack(self.session, status=status)

    def quotas(self):
        """List quota

        :returns: A generator of Quota object
        :rtype: :class:`~otcextensions.sdk.dms.v1.quota.Quota`
        """
        return self._list(_quota.Quota)
