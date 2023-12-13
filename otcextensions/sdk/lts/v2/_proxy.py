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

from otcextensions.sdk.lts.v2 import group as _group
from otcextensions.sdk.lts.v2 import stream as _stream


class Proxy(proxy.Proxy):

    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {"Accept": "application/json",
                                   "Content-type": "application/json"}

    # ======== Group ========
    def groups(self):
        """Query all log groups of an account.

        :returns: A generator of log group
            :class:`~otcextensions.sdk.lts.v2.group.Group` instances
        """
        return self._list(_group.Group)

    def create_group(self, **attrs):
        """Creating a log group for log retention and query

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.lts.v2.group.Group`,
            comprised of the properties on the Group class.
        :returns: The results of config creation
        :rtype: :class:`~otcextensions.sdk.lts.v2.group.Group`
        """
        return self._create(
            _group.Group,
            **attrs
        )

    def update_group(self, group, **attrs):
        """Update log group attributes

        :param group: The id or an instance of
            :class:`~otcextensions.sdk.lts.v2.group.Group`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.lts.v2.group.Group`

        :rtype: :class:`~otcextensions.sdk.lts.v2.group.Group`
        """
        return self._update(_group.Group, group, **attrs)

    def delete_group(self, group, ignore_missing=True):
        """Delete a single log group.

        :param group: The value can be the ID of a log group
             or a :class:`~otcextensions.sdk.lts.v2.group.Group`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent log group.
        :returns:  None
        """
        self._delete(
            _group.Group, group, ignore_missing=ignore_missing
        )
        return None

    # ======== Stream ========
    def streams(self, log_group):
        """List log stream in log group

        :param log_group: The value can be the ID of a log group
            or a :class:`~otcextensions.sdk.lts.v2.group.Group`
            instance.
        :returns: A generator of log stream
            :class:`~otcextensions.sdk.lts.v2.stream.Stream` instances
        :rtype: :class:`~otcextensions.sdk.lts.v2.stream.Stream`
        """
        log_group = self._get_resource(_group.Group, log_group)
        return self._list(
            _stream.Stream,
            log_group_id=log_group.id
        )

    def create_stream(self, log_group, **query):
        """Create a log stream in log group

        :param log_group: The value can be the ID of a log group
            or a :class:`~otcextensions.sdk.lts.v2.group.Group`
            instance.
        :param dict query: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.lts.v2.stream.Stream`,
            comprised of the properties on the Stream class.
        :returns: The result of stream creation.
        """
        log_group = self._get_resource(_group.Group, log_group)
        stream = log_group.create_stream(self, query=query)
        return stream

    def delete_stream(self, log_group, log_stream, ignore_missing=True):
        """Delete log stream from log group

        :param log_group: The value can be the ID of a log group
            or a :class:`~otcextensions.sdk.lts.v2.group.Group`
            instance.
        :param log_stream: The value can be the ID of a log stream
            or a :class:`~otcextensions.sdk.lts.v2.stream.Stream`
            instance.
        :returns:  None
        """
        log_group = self._get_resource(_group.Group, log_group)
        log_stream = self._get_resource(_stream.Stream, log_stream)
        log_group.delete_stream(self, log_stream_id=log_stream.id,
                                ignore_missing=ignore_missing)
        return None
