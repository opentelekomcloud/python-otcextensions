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

from otcextensions.sdk.dns.v2 import _proxy
from otcextensions.sdk.dns.v2 import zone as _zone
from otcextensions.sdk.dns.v2 import nameserver as _ns
from otcextensions.sdk.dns.v2 import ptr as _ptr
from otcextensions.sdk.dns.v2 import recordset as _rs

from openstack.tests.unit import test_proxy_base


class TestDNSProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestDNSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_zones(self):
        self.verify_list(
            self.proxy.zones, _zone.Zone, paginated=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            expected_kwargs={
            }
        )

    def test_get_zone(self):
        self.verify_get(
            self.proxy.get_zone, _zone.Zone,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
        )

    def test_find_zone(self):
        self.verify_find(
            self.proxy.find_zone, _zone.Zone,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._find',
        )

    def test_create_zone(self):
        self.verify_create(
            self.proxy.create_zone, _zone.Zone,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_kwargs={
                'x': 1,
                'y': '2'
            },
            expected_kwargs={
                'prepend_key': False,
                'x': 1,
                'y': '2'
            }
        )

    def test_delete_zone(self):
        self.verify_delete(
            self.proxy.delete_zone, _zone.Zone, ignore=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
        )

    def test_update_zone(self):
        self.verify_update(
            self.proxy.update_zone, _zone.Zone,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._update',
        )

    def test_associate_router(self):
        self._verify2(
            'otcextensions.sdk.dns.v2.zone.Zone.associate_router',
            self.proxy.add_router_to_zone,
            method_args=['zone_id'],
            method_kwargs={'x': 1},
            expected_args=[self.proxy],
            expected_kwargs={'x': 1}
        )

    def test_disassociate_router(self):
        self._verify2(
            'otcextensions.sdk.dns.v2.zone.Zone.disassociate_router',
            self.proxy.remove_router_from_zone,
            method_args=['zone_id'],
            method_kwargs={'x': 1},
            expected_args=[self.proxy],
            expected_kwargs={'x': 1}
        )

    def test_ns(self):
        self.verify_list(
            self.proxy.nameservers, _ns.NameServer, paginated=False,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'zone': 'zone_id'
            },
            expected_kwargs={
                'zone_id': 'zone_id'
            }
        )

    def test_recordset_all(self):
        self.verify_list(
            self.proxy.recordsets, _rs.Recordset, paginated=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'zone': None
            },
            expected_kwargs={
            }
        )

    def test_recordset_zone(self):
        self.verify_list(
            self.proxy.recordsets, _rs.ZoneRecordset, paginated=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={
                'zone': 'zoneid'
            },
            expected_kwargs={
                'zone_id': 'zoneid'
            }
        )

    def test_get_rs(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._get',
            self.proxy.get_recordset,
            method_args=['zone_id', 'rs_id'],
            method_kwargs={},
            expected_args=[_rs.ZoneRecordset],
            expected_kwargs={
                'zone_id': 'zone_id'
            }
        )

    def test_create_recordset(self):
        self.verify_create(
            self.proxy.create_recordset, _rs.ZoneRecordset,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_args=['zone_id'],
            method_kwargs={
                'x': 1,
                'y': '2'
            },
            expected_kwargs={
                'prepend_key': False,
                'zone_id': 'zone_id',
                'x': 1,
                'y': '2'
            }
        )

    def test_update_recordset(self):
        self.verify_update(
            self.proxy.update_recordset, _rs.ZoneRecordset,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._update',
        )

    def test_delete_recordset(self):
        self.verify_delete(
            self.proxy.delete_recordset, _rs.ZoneRecordset, ignore=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
        )

    def test_ptrs(self):
        self.verify_list(
            self.proxy.ptrs, _ptr.PTR, paginated=True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
        )

    def test_get_ptr(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._get',
            self.proxy.get_ptr,
            method_args=['region', 'flop'],
            method_kwargs={},
            expected_args=[_ptr.PTR, 'region:flop'],
        )

    def test_create_ptr(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._update',
            self.proxy.create_ptr,
            method_args=['region', 'flop'],
            method_kwargs={
                'x': 1,
                'y': 2
            },
            expected_args=[_ptr.PTR],
            expected_kwargs={
                'prepend_key': False,
                'id': 'region:flop',
                'x': 1,
                'y': 2
            }
        )

    def test_delete_ptr(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._update',
            self.proxy.restore_ptr,
            method_args=['region', 'flop'],
            method_kwargs={},
            expected_args=[_ptr.PTR, 'region:flop'],
            expected_kwargs={
                'has_body': False,
                'prepend_key': False,
                'ptrdname': None
            }
        )
