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

from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.rds.v1 import _proxy
from otcextensions.sdk.rds.v1 import backup as _backup
from otcextensions.sdk.rds.v1 import configuration as _configuration
from otcextensions.sdk.rds.v1 import datastore as _datastore
from otcextensions.sdk.rds.v1 import flavor as _flavor
from otcextensions.sdk.rds.v1 import instance as _instance

PROJECT_ID = '123'
ENDPOINT_OS = 'http://rds.example.com/v1.0'
ENDPOINT_RDS = 'http://rds.example.com/rds/v1'

# RDS requires those headers to be present in the request, to native API
# otherwise 404
RDS_HEADERS = {
    'Content-Type': 'application/json',
    'X-Language': 'en-us'
}

# RDS requires those headers to be present in the request, to OS-compat API
# otherwise 404
OS_HEADERS = {
    'Content-Type': 'application/json',
}


class TestRdsProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestRdsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        self.session.get_project_id = mock.Mock(return_value=PROJECT_ID)
        self.session.get_endpoint = mock.Mock(
            return_value=ENDPOINT_RDS
        )

    def test_get_os_endpoint(self):
        self.assertEqual(ENDPOINT_OS, self.proxy.get_os_endpoint())

    def test_get_rds_endpoint(self):
        self.assertEqual(ENDPOINT_RDS, self.proxy.get_rds_endpoint())

    def test_datastore_types(self):
        result = list(self.proxy.datastore_types())
        self.assertEqual(['MySQL', 'PostgreeSQL', 'SQLServer'], result)

    def test_datastores(self):
        self.verify_list(
            self.proxy.datastores, _datastore.Datastore,
            method_kwargs={
                'db_name': 'test',
            },
            paginated=False,
            expected_kwargs={
                'datastore_name': 'test',
                'endpoint_override': ENDPOINT_RDS,
                'headers': RDS_HEADERS,
                'project_id': PROJECT_ID
            }
        )

    def test_flavors(self):
        self.verify_list(
            self.proxy.flavors, _flavor.Flavor,
            paginated=False,
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS
            }
        )

    def test_get_flavor(self):
        self.verify_get(
            self.proxy.get_flavor,
            _flavor.Flavor,
            mock_method='otcextensions.sdk.rds.v1._proxy.Proxy._get',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS
            }
        )

    def test_find_flavor(self):
        self.assertRaises(NotImplementedError, self.proxy.find_flavor, '')

    def test_create_instance(self):
        self.assertRaises(NotImplementedError,
                          self.proxy.create_instance)

    def test_delete_instance(self):
        self.assertRaises(NotImplementedError,
                          self.proxy.delete_instance, None)

    def test_update_instance(self):
        self.assertRaises(NotImplementedError,
                          self.proxy.update_instance, None)

    def test_get_instance(self):
        self.verify_get(
            self.proxy.get_instance,
            _instance.Instance,
            mock_method='otcextensions.sdk.rds.v1._proxy.Proxy._get',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
            }
        )

    def test_instances(self):
        self.verify_list(
            self.proxy.instances, _instance.Instance,
            paginated=False,
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS
            }
        )

    def test_configuration_groups(self):
        self.verify_list(
            self.proxy.configuration_groups, _configuration.ParameterGroup,
            paginated=False,
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                # 'headers': OS_HEADERS
            }
        )

    def test_get_configuration_group(self):
        self.verify_get(
            self.proxy.get_configuration_group,
            _configuration.ParameterGroup,
            mock_method='otcextensions.sdk.rds.v1._proxy.Proxy._get',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                # 'headers': OS_HEADERS
            }
        )

    def test_create_configuration_group(self):
        self.assertRaises(NotImplementedError,
                          self.proxy.create_configuration_group, None)

    def test_update_configuration_group(self):
        self.assertRaises(NotImplementedError,
                          self.proxy.update_configuration_group, None)

    def test_delete_configuration_group(self):
        self.assertRaises(NotImplementedError,
                          self.proxy.delete_configuration_group, None)

    def test_backups(self):
        self.verify_list(
            self.proxy.backups, _backup.Backup,
            paginated=False,
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_RDS,
                'headers': RDS_HEADERS
            }
        )

    def test_create_backup(self):
        self.verify_create(
            self.proxy.create_backup, _backup.Backup,
            method_kwargs={
                'instance': 'test',
                'name': 'some_name'
            },
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_RDS,
                'headers': RDS_HEADERS,
                'instance_id': 'test',
                'name': 'some_name'
            }
        )

    def test_delete_backup(self):
        self.verify_delete(
            self.proxy.delete_backup,
            _backup.Backup, False,
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_RDS,
                'headers': RDS_HEADERS,
            }
        )

    def test_get_backup_policy(self):
        self.verify_get(
            self.proxy.get_backup_policy, _backup.BackupPolicy,
            value=[],
            mock_method='otcextensions.sdk.rds.v1._proxy.Proxy._get',
            method_kwargs={
                'instance': 'id'
            },
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_RDS,
                'headers': RDS_HEADERS,
                'instance_id': 'id',
                'requires_id': False
            }
        )

    def test_set_backup_policy(self):
        # TODO(agoncharov) upstream BaseProxy is renamed to Proxy
        self._verify2(
            'openstack.proxy.BaseProxy._update',
            self.proxy.set_backup_policy,
            method_args=['POLICY', 'INST_ID'],
            expected_args=[_backup.BackupPolicy, 'POLICY'],
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_RDS,
                'instance_id': 'INST_ID',
                'headers': RDS_HEADERS
            }
        )
