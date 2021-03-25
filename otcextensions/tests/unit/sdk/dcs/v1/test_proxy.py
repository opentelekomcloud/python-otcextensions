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
import mock

from otcextensions.sdk.dcs.v1 import _proxy
from otcextensions.sdk.dcs.v1 import backup as _backup
from otcextensions.sdk.dcs.v1 import config as _config
from otcextensions.sdk.dcs.v1 import instance as _instance
from otcextensions.sdk.dcs.v1 import restore as _restore
from otcextensions.sdk.dcs.v1 import statistic as _stat

from openstack.tests.unit import test_proxy_base


class TestDCSProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestDCSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_create_instance(self):
        self.verify_create(
            self.proxy.create_instance, _instance.Instance,
        )

    def test_instances(self):
        self.verify_list(
            self.proxy.instances, _instance.Instance,
        )

    def test_instances_query(self):
        self.verify_list(
            self.proxy.instances, _instance.Instance,
            method_kwargs={
                'start': '1',
                'limit': '2',
                'name': '3',
                'status': '4',
                'includeFailure': True,
                'exactMatchName': True
            },
            expected_kwargs={
                'start': '1',
                'limit': '2',
                'name': '3',
                'status': '4',
                'includeFailure': True,
                'exactMatchName': True
            }
        )

    def test_get_instance(self):
        self.verify_get(
            self.proxy.get_instance, _instance.Instance,
        )

    def test_find_instance(self):
        self.verify_find(
            self.proxy.find_instance, _instance.Instance,
        )

    def test_update_instance(self):
        self.sot = _instance.Instance()
        self.sot.update = mock.Mock(return_value=self.sot)
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.update_instance('VALUE', a='b')
        self.proxy._get_resource.assert_called_with(
            _instance.Instance,
            'VALUE',
            a='b'
        )

    def test_extend_instance(self):
        self.sot = _instance.Instance()
        self.sot.extend = mock.Mock(return_value={})
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.extend_instance(self.sot, 4)
        self.proxy._get_resource.assert_called_with(
            _instance.Instance,
            self.sot
        )
        self.sot.extend.assert_called_with(
            self.proxy,
            4
        )
        self.proxy._get.assert_called_with(
            _instance.Instance,
            self.sot
        )

    def test_delete_instance(self):
        self.verify_delete(
            self.proxy.delete_instance, _instance.Instance, True,
        )

    def test_stop_instance(self):
        self.sot = _instance.Instance()
        self.sot.stop = mock.Mock(return_value={})
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._find = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.stop_instance(self.sot)
        self.sot.stop.assert_called_with(
            self.proxy,
        )
        self.proxy._get.assert_called_with(
            _instance.Instance,
            self.sot
        )

    def test_start_instance(self):
        self.sot = _instance.Instance()
        self.sot.start = mock.Mock(return_value={})
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._find = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.start_instance(self.sot)
        self.sot.start.assert_called_with(
            self.proxy,
        )
        self.proxy._get.assert_called_with(
            _instance.Instance,
            self.sot
        )

    def test_restart_instance(self):
        self.sot = _instance.Instance()
        self.sot.restart = mock.Mock(return_value={})
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._find = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.restart_instance(self.sot)
        self.sot.restart.assert_called_with(
            self.proxy,
        )
        self.proxy._get.assert_called_with(
            _instance.Instance,
            self.sot
        )

    def test_change_pwd(self):
        self.sot = _instance.Instance()
        self.sot.change_pwd = mock.Mock(return_value={})
        self.proxy._get = mock.Mock(return_value=self.sot)
        self.proxy._find = mock.Mock(return_value=self.sot)
        self.proxy._get_resource = mock.Mock(return_value=self.sot)

        self.proxy.change_instance_password(self.sot, 'curr', 'new')
        self.sot.change_pwd.assert_called_with(
            self.proxy,
            current_password='curr',
            new_password='new'
        )
        self.proxy._get.assert_not_called()

    def test_statistics(self):
        self.verify_list(
            self.proxy.statistics, _stat.Statistic,
            expected_kwargs={
                'paginated': False
            }
        )

    def test_backups(self):
        self.sot = _backup.Backup()
        self.inst = _instance.Instance(id='1')
        self.proxy._get_resource = mock.Mock(return_value=self.inst)
        self.proxy._list = mock.Mock(return_value=self.sot)

        self.proxy.backups('inst')
        self.proxy._list.assert_called_with(
            _backup.Backup,
            paginated=False,
            instance_id='1'
        )

    def test_backups_query(self):
        self.sot = _backup.Backup()
        self.inst = _instance.Instance(id='1')
        self.proxy._get_resource = mock.Mock(return_value=self.inst)
        self.proxy._list = mock.Mock(return_value=self.sot)

        self.proxy.backups(
            'inst',
            start='1',
            end='2',
            start_time='3',
            end_time='4')
        self.proxy._list.assert_called_with(
            _backup.Backup,
            paginated=False,
            instance_id='1',
            start='1',
            end='2',
            start_time='3',
            end_time='4'
        )

    def test_create_backup(self):
        self.sot = _backup.Backup()
        self.proxy._create = mock.Mock(return_value=self.sot)

        self.proxy.backup_instance('1', remark='rem')
        self.proxy._create.assert_called_with(
            _backup.Backup,
            instance_id='1',
            remark='rem'
        )

    def test_delete_backup(self):
        instance = _instance.Instance(id='instance_id')
        self._verify2(
            'openstack.proxy.Proxy._delete',
            self.proxy.delete_instance_backup,
            method_args=[instance, 'backup_1'],
            expected_args=[_backup.Backup, 'backup_1'],
            expected_kwargs={
                'instance_id': instance.id,
                'ignore_missing': True
            }
        )

    def test_restores_query(self):
        self.sot = _restore.Restore()
        self.proxy._list = mock.Mock(return_value=self.sot)

        self.proxy.restore_records(
            instance='inst',
            start='1',
            end='2',
            start_time='3',
            end_time='4')
        self.proxy._list.assert_called_with(
            _restore.Restore,
            paginated=False,
            instance_id='inst',
            start='1',
            end='2',
            start_time='3',
            end_time='4'
        )

    def test_restore_backup(self):
        self.proxy._create = mock.Mock()

        self.proxy.restore_instance(
            instance='1',
            backup_id='bck',
            remark='rem')
        self.proxy._create.assert_called_with(
            _restore.Restore,
            instance_id='1',
            backup_id='bck',
            remark='rem'
        )

    def test_configs(self):
        self.proxy._list = mock.Mock()

        self.proxy.instance_params('1')
        self.proxy._list.assert_called_with(
            _config.Config,
            paginated=False,
            instance_id='1'
        )

    def test_update_configs(self):
        self.sot = _config.Config()
        self.proxy._get_resource = mock.Mock(return_value=self.sot)
        self.sot._update = mock.Mock()
        params = []

        self.proxy.update_instance_params(
            instance='inst_id',
            params=params)
        self.sot._update.assert_called_with(
            self.proxy,
            params
        )
