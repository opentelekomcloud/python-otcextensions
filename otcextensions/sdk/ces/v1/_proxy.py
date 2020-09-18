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

from otcextensions.sdk.ces.v1 import alarm as _alarm
from otcextensions.sdk.ces.v1 import event_data as _event_data
from otcextensions.sdk.ces.v1 import metric as _metric
from otcextensions.sdk.ces.v1 import metric_data as _metric_data
from otcextensions.sdk.ces.v1 import quota as _quota


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Alarms ========
    def alarms(self, **query):
        """Return a generator of alarms

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
        :returns: A generator of alarm objects
        :rtype: :class:`~otcextensions.sdk.ces.v1.alarm.Alarm`
        """
        return self._list(_alarm.Alarm, **query)

    def get_alarm(self, alarm):
        """Return a single alarm

        :param alarm: The value can be the ID of a alarm or a
                       :class:`~otcextensions.sdk.ces.v1.alarm.Alarm`
                        instance.
        :returns: A generator of alarm objects
        :rtype: :class:`~otcextensions.sdk.ces.v1.alarm.Alarm`
        """
        return self._get(_alarm.Alarm, alarm)

    def create_alarm(self, **attrs):
        """Create a new Alarm from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`otcextensions.sdk.ces.v1.alarm.Alarm`
        """
        return self._create(_alarm.Alarm, **attrs)

    def delete_alarm(self, alarm, ignore_missing=True):
        """Delete a Alarm

        :param alarm: key id or an instance of
            :class:`otcextensions.sdk.ces.v1.alarm.Alarm`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the alarm does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent alarm.
        :returns: Alarm been deleted
        :rtype: :class:`otcextensions.sdk.ces.v1.alarm.Alarm`
        """
        return self._delete(_alarm.Alarm, alarm,
                            ignore_missing=ignore_missing)

    def find_alarm(self, name_or_id, ignore_missing=True):
        """Find a single alarm

        :param name_or_id: The name or ID of a alarm
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the alarm does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent alarm.

        :returns: ``None``
        """
        return self._find(_alarm.Alarm, name_or_id,
                          ignore_missing=ignore_missing)

    def switch_alarm_state(self, alarm):
        """Enables or disables Alarm

        :param alarm: The value can be the ID of an alarm
             or a :class:`~otcextensions.sdk.ces.v1.alarm.Alarm` instance.
        :returns: None
        """
        alarm = self._get_resource(_alarm.Alarm, alarm)
        alarm.change_alarm_status(self)

    # ======== Event-Data ========
    def event_data(self, **query):
        """Return a generator of host configurations for a specified
           event type in a specified period of time.

        :param kwargs query: Optional query parameters to be sent to limit
                              the resources being returned.
        :returns: A generator of event data objects
        :rtype: :class:`~otcextensions.sdk.ces.v1.event_data.EventData`
        """
        return self._list(_event_data.EventData, **query)

    # ======== Metrics ========
    def metrics(self, **query):
        """Return a generator of metrics

        :param kwargs query: Optional query parameters to be sent to limit
                              the resources being returned.
        :returns: A generator of metric objects
        :rtype: :class:`~otcextensions.sdk.ces.v1.metric.Metric`
        """
        return self._list(_metric.Metric, **query)

    # ======== Metric-Data ========
    def metric_data(self, **query):
        """Return a generator of Metric Data

        :param kwargs query: Optional query parameters to be sent to limit
                              the resources being returned.
        :returns: A generator of metric data objects
        :rtype: :class:`~otcextensions.sdk.ces.v1.metric_data.MetricData`
        """
        return self._list(_metric_data.MetricData, **query)

    # skipped due to lag of compliant API (resource is list not JSON)
    '''
    def create_metric_data(self, **attrs):
       """Create a new Alarm from attributes

       :param dict attrs: Keyword arguments which will be used to create
           a :class:`~otcextensions.sdk.ces.v1.metric_data.MetricData`
       """
       return self._create(_metric_data.MetricData, **attrs)
    '''

    # ======== Quotas ========
    def quotas(self):
        """Return a generator of quotas

        :returns: A generator of quota objects
        :rtype: :class:`~otcextensions.sdk.ces.v1.quota.Quota`
        """
        return self._list(_quota.Quota)
