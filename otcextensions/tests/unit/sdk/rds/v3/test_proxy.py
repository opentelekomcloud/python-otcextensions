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

from otcextensions.sdk.rds.v3 import _proxy
from otcextensions.sdk.rds.v3 import backup
from otcextensions.sdk.rds.v3 import configuration
from otcextensions.sdk.rds.v3 import datastore
from otcextensions.sdk.rds.v3 import flavor
from otcextensions.sdk.rds.v3 import instance

from openstack.tests.unit import test_proxy_base


class TestRdsProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestRdsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestFlavor(TestRdsProxy):
    def test_flavors(self):
        self.verify_list(self.proxy.flavors,
                         flavor.Flavor,
                         method_kwargs={
                             'datastore_name': 'MySQL',
                             'version_name': '5.7'
                         },
                         expected_kwargs={
                             'datastore_name': 'MySQL',
                             'version_name': '5.7'
                         })


class TestDatastore(TestRdsProxy):
    def test_datastores(self):
        self.verify_list(self.proxy.datastores,
                         datastore.Datastore,
                         method_args=['ss'],
                         expected_kwargs={
                             'database_name': 'ss'
                         })


class TestConfiguration(TestRdsProxy):
    def test_configurations(self):
        self.verify_list(self.proxy.configurations,
                         configuration.Configuration,
                         expected_kwargs={'paginated': False})

    def test_get_configuration(self):
        self.verify_get(
            self.proxy.get_configuration,
            configuration.Configuration)

    def test_create_configuration(self):
        self.verify_create(
            self.proxy.create_configuration,
            configuration.Configuration,
            method_kwargs={'a': 'b'},
            expected_kwargs={'prepend_key': False, 'a': 'b'})

    def test_delete_configuration(self):
        self.verify_delete(self.proxy.delete_configuration,
                           configuration.Configuration, False)

    def test_delete_configuration_ignore(self):
        self.verify_delete(self.proxy.delete_configuration,
                           configuration.Configuration, True)

    def test_update_configuration(self):
        self.verify_update(self.proxy.update_configuration,
                           configuration.Configuration)

    def test_apply_configuration(self):
        self._verify2(
            'otcextensions.sdk.rds.v3.configuration.Configuration.apply',
            self.proxy.apply_configuration,
            method_args=["val", ['a', 'b']],
            expected_args=[self.proxy, ['a', 'b']]
        )


class TestBackup(TestRdsProxy):
    def test_backups(self):
        self.verify_list(self.proxy.backups,
                         backup.Backup, method_args=['inst'],
                         expected_kwargs={'instance_id': 'inst'})

    def test_create_backup(self):
        self.verify_create(
            self.proxy.create_backup,
            backup.Backup,
            method_args=['inst'],
            method_kwargs={'x': 1, 'y': 2, 'z': 3},
            expected_kwargs={
                'instance_id': 'inst',
                'x': 1, 'y': 2, 'z': 3
            })

    def test_delete_backup(self):
        self.verify_delete(self.proxy.delete_backup,
                           backup.Backup, False)

    def test_delete_backup_ignore(self):
        self.verify_delete(self.proxy.delete_backup,
                           backup.Backup, True)

    def test_find_backup(self):
        self.verify_find(self.proxy.find_backup, backup.Backup,
                         value=['name_or_id', 'iid'],
                         expected_kwargs={'instance_id': 'iid'})

    def test_wait_for_backup(self):
        value = backup.Backup(id='fake')
        self.verify_wait_for_status(
            self.proxy.wait_for_backup,
            method_args=[value],
            expected_args=[
                value,
                'COMPLETED',
                ['FAILED'],
                2, 300
            ])

    def test_download_links(self):
        self.verify_list(self.proxy.backup_download_links,
                         backup.BackupFile,
                         method_args=['bck_id'],
                         expected_kwargs={'backup_id': 'bck_id'})


class TestInstance(TestRdsProxy):
    def test_instances(self):
        self.verify_list(self.proxy.instances,
                         instance.Instance)

    def test_create_instance(self):
        self.verify_create(
            self.proxy.create_instance,
            instance.Instance)

    def test_get_instance(self):
        self.verify_get(
            self.proxy.get_instance,
            instance.Instance)

    def test_find_instance(self):
        self.verify_find(
            self.proxy.find_instance,
            instance.Instance)

    def test_delete_instance(self):
        self.verify_delete(self.proxy.delete_instance,
                           instance.Instance, False)

    def test_delete_instance_ignore(self):
        self.verify_delete(self.proxy.delete_instance,
                           instance.Instance, True)

    def test_fetch_restore_times(self):
        self._verify2(
            'otcextensions.sdk.rds.v3.instance.Instance.fetch_restore_times',
            self.proxy.get_instance_restore_time,
            method_args=["inst"],
            expected_args=[self.proxy]
        )

    def test_restore(self):
        self._verify2(
            'otcextensions.sdk.rds.v3.instance.Instance.restore',
            self.proxy.restore_instance,
            method_args=["inst"],
            method_kwargs={
                'backup': backup.Backup(id='bck'),
                'restore_time': 'rt'},
            expected_args=[self.proxy, backup.Backup(id='bck'), 'rt'],
        )

    def test_get_instance_configuration(self):
        pass

    def test_update_instance_configuration(self):
        pass

    def test_get_instance_backup_policy(self):
        self._verify2(
            'otcextensions.sdk.rds.v3.instance.Instance.get_backup_policy',
            self.proxy.get_instance_backup_policy,
            method_args=["val"],
            expected_args=[self.proxy]
        )

    def test_update_instance_backup_policy(self):
        self._verify2(
            'otcextensions.sdk.rds.v3.instance.Instance.set_backup_policy',
            self.proxy.set_instance_backup_policy,
            method_args=["val"],
            method_kwargs={
                'keep_days': 1,
                'start_time': '2',
                'period': '3'
            },
            expected_kwargs={
                'keep_days': 1,
                'start_time': '2',
                'period': '3'
            },
            expected_args=[self.proxy]
        )
