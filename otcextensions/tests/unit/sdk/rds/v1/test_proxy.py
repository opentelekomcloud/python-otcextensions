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

        self.additional_headers = RDS_HEADERS

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
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
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
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': OS_HEADERS
            }
        )

    def test_get_flavor(self):
        self.verify_get(
            self.proxy.get_flavor,
            _flavor.Flavor,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': OS_HEADERS
            }
        )

    def test_find_flavor(self):
        self.assertRaises(NotImplementedError, self.proxy.find_flavor, '')

    def test_create_instance(self):
        self.verify_create(
            self.proxy.create_instance, _instance.Instance,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_kwargs={
                'instance': 'test',
                'name': 'some_name'
            },
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': OS_HEADERS,
                'instance': 'test',
                'name': 'some_name'
            }
        )

    def test_delete_instance(self):
        self.verify_delete(
            self.proxy.delete_instance,
            _instance.Instance, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': OS_HEADERS,
            }
        )

    def test_update_instance(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._update',
            self.proxy.update_instance,
            method_args=['INSTANCE'],
            method_kwargs={'test': 't'},
            expected_args=[_instance.Instance],
            expected_kwargs={
                'test': 't',
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_RDS,
                'instance': 'INSTANCE',
                'headers': RDS_HEADERS
            }
        )

    def test_get_instance(self):
        self.verify_get(
            self.proxy.get_instance,
            _instance.Instance,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': OS_HEADERS
            }
        )

    def test_instances(self):
        self.verify_list(
            self.proxy.instances, _instance.Instance,
            paginated=False,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': OS_HEADERS
            }
        )

    def test_parameter_groups(self):
        self.verify_list(
            self.proxy.parameter_groups, _configuration.ParameterGroup,
            paginated=False,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': OS_HEADERS
            }
        )

    def test_get_parameter_group(self):
        self.verify_get(
            self.proxy.get_parameter_group,
            _configuration.ParameterGroup,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': RDS_HEADERS
            }
        )

    def test_create_parameter_group(self):
        self.verify_create(
            self.proxy.create_parameter_group,
            _configuration.ParameterGroup,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
            method_kwargs={
                'instance': 'test',
                'name': 'some_name'
            },
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': OS_HEADERS,
                'instance': 'test',
                'name': 'some_name'
            }
        )
    #
    # def test_update_parameter_group(self):
    #     self.verify_update(
    #         self.proxy.update_parameter_group,
    #         _configuration.ParameterGroup,
    #         mock_method='otcextensions.sdk.sdk_proxy.Proxy._update',
    #         method_kwargs={
    #             'instance': 'test',
    #             'name': 'some_name'
    #         },
    #         expected_kwargs={
    #             'project_id': PROJECT_ID,
    #             'endpoint_override': ENDPOINT_OS,
    #             'headers': OS_HEADERS,
    #             'instance_id': 'test',
    #             'name': 'some_name'
    #         }
    #     )

    def test_delete_parameter_group(self):
        self.verify_delete(
            self.proxy.delete_parameter_group,
            _configuration.ParameterGroup, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_OS,
                'headers': OS_HEADERS,
            }
        )

    def test_backups(self):
        self.verify_list(
            self.proxy.backups, _backup.Backup,
            paginated=False,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            expected_kwargs={
                'project_id': PROJECT_ID,
                'endpoint_override': ENDPOINT_RDS,
                'headers': RDS_HEADERS
            }
        )

    def test_create_backup(self):
        self.verify_create(
            self.proxy.create_backup, _backup.Backup,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._create',
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
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
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
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
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
            'otcextensions.sdk.sdk_proxy.Proxy._update',
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
