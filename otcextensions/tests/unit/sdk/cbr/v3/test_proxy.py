#!/usr/bin/env python3
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
from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.cbr.v3 import _proxy
from otcextensions.sdk.cbr.v3 import backup as _backup
from otcextensions.sdk.cbr.v3 import restore as _restore


class TestCBRProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestCBRProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestCBRBackup(TestCBRProxy):

    def test_backups(self):
        self.verify_list(self.proxy.backups, _backup.Backup)

    def test_backup_delete(self):
        self.verify_delete(self.proxy.delete_backup,
                           _backup.Backup, True)

    def test_backup_find(self):
        self.verify_find(self.proxy.find_backup, _backup.Backup)

    def test_backup_get(self):
        self.verify_get(self.proxy.get_backup, _backup.Backup)


class TestCBRRestore(TestCBRProxy):

    def test_restore_server(self):
        attrs = {'a': 'b'}
        backup = _backup.Backup(id='my_backup')
        self._verify2(
            'openstack.proxy.Proxy._create',
            self.proxy.restore_data,
            method_args=[backup],
            method_kwargs=attrs,
            expected_args=[_restore.Restore],
            expected_kwargs=dict(
                backup=backup.id,
                **attrs
            )
        )
