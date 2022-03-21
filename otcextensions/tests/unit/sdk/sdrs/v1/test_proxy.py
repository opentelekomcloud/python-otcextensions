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
from otcextensions.sdk.sdrs.v1 import protected_instance as \
    _protected_instance
from otcextensions.sdk.sdrs.v1 import replication_pair as _replication_pair
from otcextensions.sdk.sdrs.v1 import dr_drill as _dr_drill
from otcextensions.sdk.sdrs.v1 import task_center as _task_center
from otcextensions.sdk.sdrs.v1 import quota as _quota


class TestSDRSProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestSDRSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestSDRSJob(TestSDRSProxy):

    def test_get_job(self):
        self.verify_get(self.proxy.get_job, _job.Job)


class TestSDRSActiveDomains(TestSDRSProxy):

    def test_get_domains(self):
        self.verify_list(self.proxy.get_domains,
                         _active_domains.ActiveDomains)


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
            'otcextensions.sdk.sdrs.v1.'
            'protection_group.ProtectionGroup.enable_protection_group',
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
            'otcextensions.sdk.sdrs.v1.protection_group.'
            'ProtectionGroup.disable_protection_group',
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
            'otcextensions.sdk.sdrs.v1.protection_group.'
            'ProtectionGroup.perform_failover',
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
            'otcextensions.sdk.sdrs.v1.protection_group.'
            'ProtectionGroup.perform_planned_failover',
            self.proxy.perform_planned_failover,
            method_args=[group, priority_station],
            expected_args=[self.proxy],
            expected_kwargs={
                'protection_group': group.id,
                'priority_station': priority_station
            }
        )


class TestSDRSProtedInstance(TestSDRSProxy):

    def test_protected_instance_create(self):
        self.verify_create(self.proxy.create_protected_instance,
                           _protected_instance.ProtectedInstance,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_protected_instance_delete(self):
        protected_instance = _protected_instance.ProtectedInstance()
        delete_target_server = True
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.'
                        'protected_instance.ProtectedInstance.delete',
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
            expected_args=[_protected_instance.ProtectedInstance,
                           protected_instance],
            expected_kwargs={
                'name': name
            }
        )

    def test_protected_instance_find(self):
        self.verify_find(self.proxy.find_protected_instance,
                         _protected_instance.ProtectedInstance)

    def test_attach_replication_pair(self):
        protected_instance = _protected_instance.ProtectedInstance()
        replication = _replication_pair.ReplicationPair()
        device = 'device_name'
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.'
                        'ProtectedInstance.attach_pair',
            test_method=self.proxy.attach_replication_pair,
            method_args=[protected_instance, replication, device],
            expected_args=[self.proxy],
            expected_kwargs={
                'protected_instance': protected_instance.id,
                'replication_id': replication.id,
                'device': device
            }
        )

    def test_detach_replication_pair(self):
        protected_instance = _protected_instance.ProtectedInstance()
        replication = _replication_pair.ReplicationPair()
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.'
                        'ProtectedInstance.detach_pair',
            test_method=self.proxy.detach_replication_pair,
            method_args=[protected_instance, replication],
            expected_args=[self.proxy],
            expected_kwargs={
                'protected_instance': protected_instance.id,
                'replication_id': replication.id
            }
        )

    def test_add_nic(self):
        protected_instance = _protected_instance.ProtectedInstance()
        subnet_id = 'subnet_id'
        security_groups = ['security_group_id_1', 'security_group_id_2']
        ip_address = 'ip_address'
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.'
                        'ProtectedInstance.add_nic',
            test_method=self.proxy.add_nic,
            method_args=[protected_instance, subnet_id,
                         security_groups, ip_address],
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
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.'
                        'ProtectedInstance.delete_nic',
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
            mock_method='otcextensions.sdk.sdrs.v1.protected_instance.'
                        'ProtectedInstance.modify_instance',
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


class TestSDRSReplicationPair(TestSDRSProxy):

    def test_replication_pair_create(self):
        self.verify_create(self.proxy.create_replication_pair,
                           _replication_pair.ReplicationPair,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_replication_pair_delete(self):
        replication_pair = _replication_pair.ReplicationPair()
        server_group_id = 'server_group_id'
        delete_target_volume = True
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.replication_pair.'
                        'ReplicationPair.delete',
            test_method=self.proxy.delete_replication_pair,
            method_args=[replication_pair,
                         server_group_id,
                         delete_target_volume],
            expected_args=[self.proxy],
            expected_kwargs={
                'server_group_id': server_group_id,
                'delete_target_volume': delete_target_volume
            }
        )

    def test_replication_pair(self):
        self.verify_list(self.proxy.replication_pairs,
                         _replication_pair.ReplicationPair)

    def test_replication_pair_get(self):
        self.verify_get(self.proxy.get_replication_pair,
                        _replication_pair.ReplicationPair)

    def test_replication_pair_find(self):
        self.verify_find(self.proxy.find_replication_pair,
                         _replication_pair.ReplicationPair)

    def test_replication_pair_expand(self):
        replication = _replication_pair.ReplicationPair(id='replication')
        new_size = 100
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.replication_pair.'
                        'ReplicationPair.expand_replication',
            test_method=self.proxy.expand_replication_pair,
            method_args=[replication, new_size],
            expected_args=[self.proxy],
            expected_kwargs={
                'replication': replication.id,
                'new_size': new_size
            }
        )

    def test_replication_pair_update(self):
        replication = _replication_pair.ReplicationPair()
        name = 'name'
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.update_replication_pair,
            method_args=[replication, name],
            expected_args=[_replication_pair.ReplicationPair, replication],
            expected_kwargs={
                'name': name
            }
        )


class TestSDRSDRDrill(TestSDRSProxy):

    def test_dr_drill_create(self):
        self.verify_create(self.proxy.create_dr_drill,
                           _dr_drill.DRDrill,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_dr_drill_delete(self):
        self.verify_delete(self.proxy.delete_dr_drill,
                           _dr_drill.DRDrill)

    def test_dr_drill_list(self):
        self.verify_list(self.proxy.dr_drills,
                         _dr_drill.DRDrill)

    def test_dr_drill_get(self):
        self.verify_get(self.proxy.get_dr_drill,
                        _dr_drill.DRDrill)

    def test_dr_drill_find(self):
        self.verify_find(self.proxy.find_dr_drill,
                         _dr_drill.DRDrill)

    def test_dr_drill_update(self):
        drill = _dr_drill.DRDrill()
        name = 'name'
        self._verify(
            'openstack.proxy.Proxy._update',
            self.proxy.update_dr_drill,
            method_args=[drill, name],
            expected_args=[_dr_drill.DRDrill, drill],
            expected_kwargs={
                'name': name
            }
        )


class TestSDRSTaskCenter(TestSDRSProxy):

    def test_failed_tasks(self):
        self.verify_list(self.proxy.failed_tasks,
                         _task_center.FailedTask)

    def test_failed_task_delete(self):
        self.verify_delete(self.proxy.delete_failed_task,
                           _task_center.FailedTask)

    def test_delete_all_failed_tasks(self):
        endpoint = self.proxy.get_endpoint()
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.task_center.'
                        'FailedTask.delete_all_tasks',
            test_method=self.proxy.delete_all_failed_tasks,
            method_args=[],
            expected_args=[self.session, endpoint]
        )

    def test_delete_protection_group_tasks(self):
        endpoint = self.proxy.get_endpoint()
        group = _protection_group.ProtectionGroup()
        self._verify(
            mock_method='otcextensions.sdk.sdrs.v1.task_center.'
                        'FailedTask.delete_protection_tasks',
            test_method=self.proxy.delete_protection_group_tasks,
            method_args=[group],
            expected_args=[self.session, endpoint, group.id]
        )


class TestSDRSQuotas(TestSDRSProxy):

    def test_quotas(self):
        self.verify_list(self.proxy.quotas,
                         _quota.Quota)
