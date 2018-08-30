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
# import mock

from otcextensions.sdk.anti_ddos.v1 import _proxy
from otcextensions.sdk.anti_ddos.v1 import config as _config
from otcextensions.sdk.anti_ddos.v1 import floating_ip as _floating_ip
from otcextensions.sdk.anti_ddos.v1 import status as _status

from openstack.tests.unit import test_proxy_base


class TestAntiDdosProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestAntiDdosProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_floating_ips(self):
        self.verify_list(
            self.proxy.floating_ips, _floating_ip.FloatingIP,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
        )

    def test_unprotect_floating_ip(self):
        self.verify_delete(
            self.proxy.unprotect_floating_ip, _floating_ip.FloatingIP, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
        )

    def test_get_floating_ip_policies(self):
        self.verify_get(
            self.proxy.get_floating_ip_policies, _floating_ip.FloatingIP,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
        )

    def test_update_floating_ip_policies(self):
        self.verify_update(
            self.proxy.update_floating_ip_policies, _floating_ip.FloatingIP,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._update',
        )

    def test_configs(self):
        self.verify_list(
            self.proxy.configs, _config.Config, False,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
        )

    def test_get_floating_ip_status(self):
        self.verify_get(
            self.proxy.get_floating_ip_status, _status.FloatingIPStatus,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={
                'requires_id': False,
            }
        )

    def test_float_ip_logs(self):
        self.verify_list(
            self.proxy.floating_ip_logs, _status.FloatingIPLog, False,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'floating_ip_id': 'ip_id'
            },
            expected_kwargs={
                'floating_ip_id': 'ip_id'
            }
        )

    def test_float_ip_stat_day(self):
        self.verify_list(
            self.proxy.floating_ip_stat_day, _status.FloatingIPDayStat,
            False,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'floating_ip_id': 'ip_id'
            },
            expected_kwargs={
                'floating_ip_id': 'ip_id'
            }
        )

    def test_float_ip_stat_week(self):
        self.verify_list(
            self.proxy.floating_ip_stat_week, _status.FloatingIPWeekStat,
            False,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'floating_ip_id': 'ip_id',
                'period_start_date': 'fake'
            },
            expected_kwargs={
                'floating_ip_id': 'ip_id',
                'period_start_date': 'fake'
            }
        )
