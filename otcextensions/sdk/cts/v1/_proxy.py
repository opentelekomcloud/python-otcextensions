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

from otcextensions.sdk.cts.v1 import tracker as _tracker
from otcextensions.sdk.cts.v1 import trace as _trace


class Proxy(proxy.Proxy):

    skip_discovery = True

    def traces(self, tracker='system', limit=50, **query):
        """List all traces

        :param tracker: The name or an tracker of
            :class:`~otcextensions.sdk.cts.v1.tracker.Tracker`
        :param limit: default limit of resources
        :returns: A generator of tracker object of
            :class:`~otcextensions.sdk.cts.v1.trace.Trace`
        """
        if isinstance(tracker, str):
            tracker = self._get_resource(_tracker.Tracker, {'name': tracker})
        query['limit'] = limit
        return self._list(_trace.Trace, tracker_name=tracker.name, **query)

    def get_tracker(self, tracker):
        """Get detail about a given tracker

        :param tracker: The tracker id, name or an tracker of
            :class:`~otcextensions.sdk.cts.v1.tracker.Tracker`
        :returns: one object of class
            :class:`~otcextensions.sdk.dcs.v1.tracker.Tracker`
        """
        return self._get(_tracker.Tracker, tracker, requires_id=False)

    def create_tracker(self, **kwargs):
        """Create a tracker

        :param dict kwargs: Keyword arguments which will be used to overwrite a
            :class:`~otcextensions.sdk.dcs.v1.tracker.Tracker`
        """
        return self._create(_tracker.Tracker, **kwargs)

    def update_tracker(self, tracker, **attrs):
        """Update tracker with attributes

        :param tracker: The value can be the ID of an tracker
            or a :class:`~otcextensions.sdk.dcs.v1.tracker.tracker`
            tracker.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dcs.v1.tracker.tracker`,
            comprised of the properties on the tracker class.
        :returns: The updated tracker
        :rtype: :class:`~otcextensions.sdk.dcs.v1.tracker.tracker`
        """
        return self._update(_tracker.Tracker, tracker, **attrs)

    def delete_tracker(self, tracker, ignore_missing=True):
        """Delete a tracker

        :param tracker: The value can be the ID of a tracker or a
            :class:`~otcextensions.sdk.cts.v2.tracker.Tracker`
            instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the backup_policy does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent backup_policy.

        :returns: tracker been deleted
        :rtype:
            :class:`~otcextensions.sdk.cts.v2.tracker.Tracker`
        """
        return self._delete(_tracker.Tracker,
                            tracker,
                            ignore_missing=ignore_missing)
