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

from otcextensions.sdk.sdrs.v1 import _proxy

from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.sdrs.v1 import job as _job
from otcextensions.sdk.sdrs.v1 import active_domains as _active_domains
from otcextensions.sdk.sdrs.v1 import protection_group as _protection_group
from otcextensions.sdk.sdrs.v1 import protected_instance as _protected_instance


class TestSDRSProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestSDRSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestSDRSJob(TestSDRSProxy):

    def test_get_job(self):
        self.verify_get(self.proxy.get_job, _job.Job)


class TestSDRSActiveDomains(TestSDRSProxy):

    def test_get_domains(self):
        self.verify_list(self.proxy.get_domains, _active_domains.ActiveDomains)


class TestSDRSProtectionGroup(TestSDRSProxy):

    def test_protection_group_create(self):
        self.verify_create(self.proxy.create_protection_group,
                           _protection_group.ProtectionGroup,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_protection_groups(self):
        self.verify_list(self.proxy.protection_groups,
                         _protection_group.ProtectionGroup)

    def test_protection_group_get(self):
        self.verify_get(self.proxy.get_protection_group,
                        _protection_group.ProtectionGroup)

    def test_protection_group_delete(self):
        self.verify_delete(self.proxy.delete_protection_group,
                           _protection_group.ProtectionGroup,
                           True)

    def test_protection_group_find(self):
        self.verify_find(self.proxy.find_protection_group,
                         _protection_group.ProtectionGroup)

    def test_protection_group_update(self):
        group = _protection_group.ProtectionGroup()
        name = 'name'
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.update_protection_group,
            method_args=[group, name],
            expected_args=[_protection_group.ProtectionGroup, group],
            expected_kwargs={
                'name': name
            }
        )

    def test_enable_protection(self):
        group = _protection_group.ProtectionGroup()
        self._verify(
            'otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup.enable_protection_group',
            self.proxy.enable_protection,
            method_args=[group],
            expected_args=[self.proxy],
            expected_kwargs={
                'protection_group': group.id
            }
        )

    def test_disable_protection(self):
        group = _protection_group.ProtectionGroup()
        self._verify(
            'otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup.disable_protection_group',
            self.proxy.disable_protection,
            method_args=[group],
            expected_args=[self.proxy],
            expected_kwargs={
                'protection_group': group.id
            }
        )

    def test_perfrom_failover(self):
        group = _protection_group.ProtectionGroup()
        self._verify(
            'otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup.perform_failover',
            self.proxy.perform_failover,
            method_args=[group],
            expected_args=[self.proxy],
            expected_kwargs={
                'protection_group': group.id
            }
        )

    def test_perfrom_planned_failover(self):
        group = _protection_group.ProtectionGroup()
        priority_station = 'target'
        self._verify(
            'otcextensions.sdk.sdrs.v1.protection_group.ProtectionGroup.perform_planned_failover',
            self.proxy.perform_planned_failover,
            method_args=[group, priority_station],
            expected_args=[self.proxy],
            expected_kwargs={
                'protection_group': group.id,
                'priority_station': priority_station
            }
        )


class TestSDRSProtectionGroup(TestSDRSProxy):

    def test_protected_instance_create(self):
        self.verify_create(self.proxy.create_protected_instance,
                           _protected_instance.ProtectedInstance,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_protected_instance_delete(self):
        protected_instance = _protected_instance.ProtectedInstance()
        delete_target_server = True
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance.delete',
            test_method=self.proxy.delete_protected_instance,
            method_args=[protected_instance, delete_target_server],
            expected_args=[self.proxy],
            expected_kwargs={
                'delete_target_server': delete_target_server,
                'delete_target_eip': False
            }
        )

    def test_protected_instance(self):
        self.verify_list(self.proxy.protected_instances,
                         _protected_instance.ProtectedInstance)

    def test_protected_instance_get(self):
        self.verify_get(self.proxy.get_protected_instance,
                        _protected_instance.ProtectedInstance)

    def test_protected_instance_update(self):
        protected_instance = _protected_instance.ProtectedInstance()
        name = 'name'
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.update_protected_instance,
            method_args=[protected_instance, name],
            expected_args=[_protected_instance.ProtectedInstance, protected_instance],
            expected_kwargs={
                'name': name
            }
        )

    def test_protected_instance_find(self):
        self.verify_find(self.proxy.find_protected_instance,
                         _protected_instance.ProtectedInstance)

    def test_attach_replication_pair(self):
        protected_instance = _protected_instance.ProtectedInstance()
        replication_id = 'replication_id'
        device = 'device_name'
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance.attach_pair',
            test_method=self.proxy.attach_replication_pair,
            method_args=[protected_instance, replication_id, device],
            expected_args=[self.proxy],
            expected_kwargs={
                'protected_instance': protected_instance.id,
                'replication_id': replication_id,
                'device': device
            }
        )

    def test_detach_replication_pair(self):
        protected_instance = _protected_instance.ProtectedInstance()
        replication_id = 'replication_id'
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance.detach_pair',
            test_method=self.proxy.detach_replication_pair,
            method_args=[protected_instance, replication_id],
            expected_args=[self.proxy],
            expected_kwargs={
                'protected_instance': protected_instance.id,
                'replication_id': replication_id
            }
        )

    def test_add_nic(self):
        protected_instance = _protected_instance.ProtectedInstance()
        subnet_id = 'subnet_id'
        security_groups = ['security_group_id_1', 'security_group_id_2']
        ip_address = 'ip_address'
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance.add_nic',
            test_method=self.proxy.add_nic,
            method_args=[protected_instance, subnet_id, security_groups, ip_address],
            expected_args=[self.proxy],
            expected_kwargs={
                'protected_instance': protected_instance.id,
                'subnet_id': subnet_id,
                'security_groups': security_groups,
                'ip_address': ip_address
            }
        )

    def test_delete_nic(self):
        protected_instance = _protected_instance.ProtectedInstance()
        nic_id = 'nic_id'
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance.delete_nic',
            test_method=self.proxy.delete_nic,
            method_args=[protected_instance, nic_id],
            expected_args=[self.proxy],
            expected_kwargs={
                'protected_instance': protected_instance.id,
                'nic_id': nic_id
            }
        )

    def test_protected_instance_modify(self):
        protected_instance = _protected_instance.ProtectedInstance()
        flavor = 'flavor_id'
        production_flavor = 'production_flavor'
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.ProtectedInstance.modify_instance',
            test_method=self.proxy.modify_protected_instance,
            method_args=[protected_instance, flavor, production_flavor],
            expected_args=[self.proxy],
            expected_kwargs={
                'protected_instance': protected_instance.id,
                'flavor': flavor,
                'production_flavor': production_flavor,
                'dr_flavor': None
            }
        )
