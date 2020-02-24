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
from otcextensions.sdk.dns.v2 import zone
from otcextensions.sdk.dns.v2 import nameserver as _ns
from otcextensions.sdk.dns.v2 import floating_ip
from otcextensions.sdk.dns.v2 import recordset

from openstack.tests.unit import test_proxy_base


class TestDnsProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestDnsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestDnsZone(TestDnsProxy):
    def test_zone_create(self):
        self.verify_create(self.proxy.create_zone, zone.Zone,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id',
                                            'prepend_key': False})

    def test_zone_delete(self):
        self.verify_delete(self.proxy.delete_zone,
                           zone.Zone, True)

    def test_zone_find(self):
        self.verify_find(self.proxy.find_zone, zone.Zone)

    def test_zone_find_private(self):
        self.verify_find(self.proxy.find_zone, zone.Zone,
                         method_kwargs={
                             'p1': 'v1'
                         },
                         expected_kwargs={'p1': 'v1'})

    def test_zone_get(self):
        self.verify_get(self.proxy.get_zone, zone.Zone)

    def test_zones(self):
        self.verify_list(self.proxy.zones, zone.Zone)

    def test_zone_update(self):
        self.verify_update(self.proxy.update_zone, zone.Zone)

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
            self.proxy.nameservers, _ns.NameServer,
            method_kwargs={
                'zone': 'zone_id'
            },
            expected_kwargs={
                'paginated': False,
                'zone_id': 'zone_id'
            }
        )


class TestDnsRecordset(TestDnsProxy):
    def test_recordset_create(self):
        self.verify_create(self.proxy.create_recordset, recordset.Recordset,
                           method_kwargs={'zone': 'id'},
                           expected_kwargs={'zone_id': 'id',
                                            'prepend_key': False})

    def test_recordset_delete(self):
        self.verify_delete(self.proxy.delete_recordset,
                           recordset.Recordset, True)

    def test_recordset_update(self):
        self.verify_update(self.proxy.update_recordset, recordset.Recordset)

    def test_recordset_get(self):
        self.verify_get(self.proxy.get_recordset, recordset.Recordset,
                        method_kwargs={'zone': 'zid'},
                        expected_kwargs={'zone_id': 'zid'}
                        )

    def test_recordsets(self):
        self.verify_list(self.proxy.recordsets, recordset.Recordset,
                         base_path='/recordsets')

    def test_recordsets_zone(self):
        self.verify_list(self.proxy.recordsets, recordset.Recordset,
                         method_kwargs={'zone': 'zid'},
                         expected_kwargs={'zone_id': 'zid'})

    def test_recordset_find(self):
        self._verify2("openstack.proxy.Proxy._find",
                      self.proxy.find_recordset,
                      method_args=['zone', 'rs'],
                      method_kwargs={},
                      expected_args=[recordset.Recordset, 'rs'],
                      expected_kwargs={'ignore_missing': True,
                                       'zone_id': 'zone'})


class TestDnsFloatIP(TestDnsProxy):
    def test_floating_ips(self):
        self.verify_list(self.proxy.floating_ips, floating_ip.FloatingIP)

    def test_floating_ip_get(self):
        self.verify_get(self.proxy.get_floating_ip, floating_ip.FloatingIP)

    def test_floating_ip_update(self):
        self.verify_update(self.proxy.update_floating_ip,
                           floating_ip.FloatingIP)

    def test_floating_ip_set(self):
        self.verify_update(self.proxy.set_floating_ip,
                           floating_ip.FloatingIP)

    def test_floating_ip_unset(self):
        self._verify2('openstack.proxy.Proxy._update',
                      self.proxy.unset_floating_ip,
                      method_args=['value'],
                      method_kwargs={},
                      expected_args=[floating_ip.FloatingIP, 'value'],
                      expected_kwargs={'ptrdname': None})
