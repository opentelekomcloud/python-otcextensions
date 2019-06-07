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
from otcextensions.sdk.anti_ddos.v1 import alert_config as _alert
from otcextensions.sdk.anti_ddos.v1 import config as _config
from otcextensions.sdk.anti_ddos.v1 import floating_ip as _floating_ip
from otcextensions.sdk.anti_ddos.v1 import status as _status


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Alert Config ========
    def get_alert_config(self, **kwargs):
        """Get Alarm configuration

        :returns: one object of class
            :class:`~otcextensions.sdk.anti_ddos.v1.alert_config.AlertConfig`
        """
        return self._get(_alert.AlertConfig, None, requires_id=False)

    # ======== Configurations ========
    def configs(self, **kwargs):
        """Get Alarm configuration

        :returns: one object of class
            :class:`~otcextensions.sdk.anti_ddos.v1.config.Config`
        """
        return self._list(_config.Config, paginated=False, **kwargs)

    # ======== FloatIP DDoS ========
    def floating_ips(self, **query):
        """Get the list of anti-ddos Floating IPs

        :param kwargs query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of FloatingIP object
        :rtype: class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`
        """

        return self._list(_floating_ip.FloatingIP, paginated=False, **query)

    def protect_floating_ip(self, floating_ip_id, **kwargs):
        """Enable anti-ddos on the given Floating IP

        :param floating_ip_id: The Floating IP id or an instance of
            :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`
        :param dict kwargs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`

        :rtype: :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`
        """
        return self._create(_floating_ip.FloatingIP,
                            floating_ip_id=floating_ip_id, **kwargs)

    def unprotect_floating_ip(self, floating_ip, ignore_missing=True):
        """Diable anti-ddos on the given Floating IP

        :param floating_ip_id: The EIP id or an instance of
            :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`
        :param bool ignore_missing: When set to ``False``
            :class:`~otcextensions.sdk.exceptions.ResourceNotFound` will be
            raised when the floating IP does not exist.

        :rtype: :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`
        """
        return self._delete(_floating_ip.FloatingIP,
                            floating_ip,
                            ignore_missing=ignore_missing)

    def get_floating_ip_policies(self, floating_ip):
        """Get detail about an Floating IP policy

        :param floating_ip: The Floating IP id or an instance of
            :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`

        :rtype: :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`
        """
        return self._get(_floating_ip.FloatingIP, floating_ip)

    def update_floating_ip_policies(self, floating_ip, **attrs):
        """Update Floating IP policy

        :param floating_ip: The Floating IP id or an instance of
            :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`

        :rtype: :class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`
        """
        return self._update(_floating_ip.FloatingIP, floating_ip, **attrs)

    def get_floating_ip_status(self, floating_ip_id):
        """Get specific floating ip status by floating ip id.

        :param floating_ip_id: The floating ip id
        :returns: The status of floating ip
        :rtype:
            :class:`~otcextensions.sdk.anti_ddos.v1.status.FloatingIPStatus`
        """
        return self._get(
            _status.FloatingIPStatus,
            floating_ip_id,
            requires_id=False,
        )

    def floating_ip_events(self, floating_ip_id, **query):
        """List specific floating ip events by floating ip id.

        :param floating_ip_id: The floating ip id
        :param dict query: Optional query parameters to be sent to limit
                                 the resources being returned.

        :returns: A generator of FloatingIPLog object
        :rtype: :class:`~otcextensions.sdk.anti_ddos.v1.status.FloatingIPLog`
        """
        return self._list(_status.FloatingIPEvent, paginated=False,
                          floating_ip_id=floating_ip_id, **query)

    def floating_ip_stat_day(self, floating_ip_id):
        """List statistic for last 24 hours by floating ip id.

        :param floating_ip_id: The floating ip id

        :returns: A generator of FloatingIPDayStat object
        :rtype:
            :class:`~otcextensions.sdk.anti_ddos.v1.status.FloatingIPDayStat`
        """
        return self._list(_status.FloatingIPDayStat, paginated=False,
                          floating_ip_id=floating_ip_id)

    def floating_ip_stat_week(self, **query):
        """List weekly defence statisticsabout all floating ips.

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned:
            * period_start_date - start day of the 7 day period to query

        :returns: A generator of FloatingIPWeekStat object
        :rtype:
            :class:`~otcextensions.sdk.anti_ddos.v1.status.FloatingIPWeekStat`
        """
        return self._get(_status.FloatingIPWeekStat, requires_id=False,
                         value=None, **query)
