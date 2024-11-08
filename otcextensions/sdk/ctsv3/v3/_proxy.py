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

from otcextensions.sdk.ctsv3.v3 import key_event as _key_event


class Proxy(proxy.Proxy):

    skip_discovery = True

    def create_key_event(self, **attrs):
        """Create an event

        :param dict attrs: Keyword arguments which will be used to create a
             :class:`~otcextensions.sdk.ctsv3.v3.key_event.KeyEvent`
        :returns: The key event
        :rtype: :class:`~otcextensions.sdk.ctsv3.v3.key_event.KeyEvent`
         """
        return self._create(_key_event.KeyEvent, **attrs)

    def update_key_event(self, **attrs):
        """Update an event

        :param dict kwargs: Keyword arguments which will be used to overwrite a
             :class:`~otcextensions.sdk.ctsv3.v3.key_event.KeyEvent`
        :returns: The updated key event
        :rtype: :class:`~otcextensions.sdk.ctsv3.v3.key_event.KeyEvent`
         """
        return self._update(_key_event.KeyEvent, **attrs)

    def delete_key_event(self, notification):
        """Delete an event

        :param notification: The key event to delete a
            :class:`~otcextensions.sdk.ctsv3.v3.key_event.KeyEvent`
        :returns: None
         """
        notification.delete_key(self)

    def key_events(self, notification_type, **attrs):
        """Query notification events

        :param notification_type The type of notification to query
        :returns: A generator of key event object of
        :class:`~otcextensions.sdk.ctsv3.v3.key_event.KeyEvent`
        """
        base_path = f'{_key_event.KeyEvent.base_path}/{notification_type}'
        return self._list(_key_event.KeyEvent,
                          base_path=base_path,
                          **attrs)
