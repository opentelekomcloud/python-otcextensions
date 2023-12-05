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
from otcextensions.sdk.ctsv2.v2 import trace as _trace


class Proxy(proxy.Proxy):

    skip_discovery = True

    def traces(self, tracker='system', **query):
        """List all traces

        :param tracker: The name or an tracker of
            :class:`~otcextensions.sdk.cts.v1.tracker.Tracker`
        :param limit: default limit of resources
        :returns: A generator of tracker object of
            :class:`~otcextensions.sdk.cts.v1.trace.Trace`
        """
        if isinstance(tracker, str):
            tracker = self._get_resource(_tracker.Tracker, {'name': tracker})
        return self._list(_trace.Trace, paginated=False,
                          tracker_name=tracker.name, **query)
