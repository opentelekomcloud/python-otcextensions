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
#

from openstack import exceptions

from otcextensions.tests.unit.sdk import base


class TestRdsMixin(base.TestCase):

    flavor = {'id': 1, 'name': 'test'}

    def setUp(self):
        super(TestRdsMixin, self).setUp()

    def test_create_rds_instance(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_rds_url(
                    base_url_append='flavors/MySQL',
                    qs_elements=['version_name=5.7']
                ),
                status_code=200,
                json={"flavors": [
                     {
                         "vcpus": "2",
                         "ram": 8,
                         "id": "1",
                         "spec_code": "rds.mysql.s1.large",
                         "instance_mode": "single",
                         "az_status": {
                             "eu-de-02": "normal",
                             "eu-de-01": "normal",
                             "eu-de-03": "normal"},
                         "version_name": ["5.7"]}]}),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['test-network-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='security-groups',
                    base_url_append='v2.0',
                    append=['test-sec_grp-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['test-vpc-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='POST',
                uri=self.get_rds_url(
                    resource='instances'
                ),
                status_code=200,
                json={
                    'instance': {'id': 123987},
                    'job_id': '15'
                }
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='jobs',
                    qs_elements=['id=15']
                ),
                status_code=200,
                json={'status': 'completed'}
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='instances',
                    qs_elements=['id=123987']
                ),
                status_code=200,
                json={'instances': [{'id': 123987, 'name': 'inst_name'}]}
            )
        ])

        obj = self.cloud.create_rds_instance(
            availability_zone='test-az-01',
            charge_info={'charge_mode': 'postPaid'},
            configuration='123',
            datastore_type='MySQL',
            datastore_version='5.7',
            disk_encryption_id='234',
            flavor='rds.mysql.s1.large',
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH',
            network='test-network-id'
        )
        self.assert_calls()

        self.assertEqual('inst_name', obj.name)

    def test_create_rds_instance_ha(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_rds_url(
                    base_url_append='flavors/MySQL',
                    qs_elements=['version_name=5.7']
                ),
                status_code=200,
                json={"flavors": [
                     {
                         "vcpus": "2",
                         "ram": 8,
                         "id": "1",
                         "spec_code": "rds.mysql.s1.large.ha",
                         "instance_mode": "ha",
                         "az_status": {
                             "eu-de-02": "normal",
                             "eu-de-01": "normal",
                             "eu-de-03": "normal"},
                         "version_name": ["5.7"]}]}),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['test-network-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='security-groups',
                    base_url_append='v2.0',
                    append=['test-sec_grp-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['test-vpc-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='POST',
                uri=self.get_rds_url(
                    resource='instances'
                ),
                status_code=200,
                json={
                    'instance': {'id': 123987},
                    'job_id': '15'
                }
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='jobs',
                    qs_elements=['id=15']
                ),
                status_code=200,
                json={'status': 'completed'}
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='instances',
                    qs_elements=['id=123987']
                ),
                status_code=200,
                json={'instances': [{'id': 123987, 'name': 'inst_name'}]}
            )
        ])

        obj = self.cloud.create_rds_instance(
            availability_zone='test-az-01,az2',
            charge_info={'charge_mode': 'postPaid'},
            configuration='123',
            datastore_type='MySQL',
            datastore_version='5.7',
            disk_encryption_id='234',
            flavor='rds.mysql.s1.large.ha',
            ha_mode='async',
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH',
            network='test-network-id'
        )

        self.assert_calls()

        self.assertEqual('inst_name', obj.name)

    def test_create_rds_instance_ha_wrong_az(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_rds_url(
                    base_url_append='flavors/MySQL',
                    qs_elements=['version_name=5.7']
                ),
                status_code=200,
                json={"flavors": [
                     {
                         "vcpus": "2",
                         "ram": 8,
                         "id": "1",
                         "spec_code": "rds.mysql.s1.large.ha",
                         "instance_mode": "ha",
                         "az_status": {
                             "eu-de-02": "normal",
                             "eu-de-01": "normal",
                             "eu-de-03": "normal"},
                         "version_name": ["5.7"]}]})
        ])

        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_rds_instance,
            availability_zone='test-az-01',
            charge_info={'charge_mode': 'postPaid'},
            configuration='123',
            datastore_type='MySQL',
            datastore_version='5.7',
            disk_encryption_id='234',
            flavor='rds.mysql.s1.large.ha',
            ha_mode='async',
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH',
            network='test-network-id'
        )

        self.assert_calls()

    def test_create_rds_instance_ha_wrong_mode_pg(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_rds_url(
                    base_url_append='flavors/postgresql',
                    qs_elements=['version_name=5.7']
                ),
                status_code=200,
                json={"flavors": [
                     {
                         "vcpus": "2",
                         "ram": 8,
                         "id": "1",
                         "spec_code": "rds.pg.s1.large.ha",
                         "instance_mode": "ha",
                         "az_status": {
                             "eu-de-02": "normal",
                             "eu-de-01": "normal",
                             "eu-de-03": "normal"},
                         "version_name": ["5.7"]}]})
        ])

        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_rds_instance,
            availability_zone='test-az-01,az2',
            charge_info={'charge_mode': 'postPaid'},
            configuration='123',
            datastore_type='postgresql',
            datastore_version='5.7',
            disk_encryption_id='234',
            flavor='rds.mysql.s1.large.ha',
            ha_mode='semisync',
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH',
            network='test-network-id'
        )

        self.assert_calls()

    def test_create_rds_instance_ha_wrong_mode_mysql(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_rds_url(
                    base_url_append='flavors/MySQL',
                    qs_elements=['version_name=5.7']
                ),
                status_code=200,
                json={"flavors": [
                     {
                         "vcpus": "2",
                         "ram": 8,
                         "id": "1",
                         "spec_code": "rds.pg.s1.large.ha",
                         "instance_mode": "ha",
                         "az_status": {
                             "eu-de-02": "normal",
                             "eu-de-01": "normal",
                             "eu-de-03": "normal"},
                         "version_name": ["5.7"]}]})
        ])

        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_rds_instance,
            availability_zone='test-az-01,az2',
            charge_info={'charge_mode': 'postPaid'},
            configuration='123',
            datastore_type='MySQL',
            datastore_version='5.7',
            disk_encryption_id='234',
            flavor='rds.mysql.s1.large.ha',
            ha_mode='sync',
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH',
            network='test-network-id'
        )

        self.assert_calls()

    def test_create_rds_instance_ha_wrong_mode_mssql(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_rds_url(
                    base_url_append='flavors/sqlserver',
                    qs_elements=['version_name=5.7']
                ),
                status_code=200,
                json={"flavors": [
                     {
                         "vcpus": "2",
                         "ram": 8,
                         "id": "1",
                         "spec_code": "rds.pg.s1.large.ha",
                         "instance_mode": "ha",
                         "az_status": {
                             "eu-de-02": "normal",
                             "eu-de-01": "normal",
                             "eu-de-03": "normal"},
                         "version_name": ["5.7"]}]})
        ])

        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_rds_instance,
            availability_zone='test-az-01,az2',
            charge_info={'charge_mode': 'postPaid'},
            configuration='123',
            datastore_type='sqlserver',
            datastore_version='5.7',
            disk_encryption_id='234',
            flavor='rds.mysql.s1.large.ha',
            ha_mode='async',
            name='inst_name',
            password='testtest',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH',
            network='test-network-id'
        )

        self.assert_calls()

    def test_rds_create_replica(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='instances',
                    qs_elements=['id=fake_name']
                ),
                status_code=200,
                json={'instances': [{
                    'id': 123987,
                    'name': 'fake_name',
                    'datastore': {'type': 'MySQL', 'version': '5.7'}}]}
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    base_url_append='flavors/MySQL',
                    qs_elements=['version_name=5.7']
                ),
                status_code=200,
                json={"flavors": [
                     {
                         "vcpus": "2",
                         "ram": 8,
                         "id": "1",
                         "spec_code": "rds.mysql.s1.large.replica",
                         "instance_mode": "replica",
                         "az_status": {
                             "eu-de-02": "normal",
                             "eu-de-01": "normal",
                             "eu-de-03": "normal"},
                         "version_name": ["5.7"]}]}
            ),
            dict(
                method='POST',
                uri=self.get_rds_url(
                    resource='instances'
                ),
                status_code=200,
                json={
                    'instance': {'id': 1239876},
                    'job_id': '15'
                }
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='jobs',
                    qs_elements=['id=15']
                ),
                status_code=200,
                json={'status': 'completed'}
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='instances',
                    qs_elements=['id=1239876']
                ),
                status_code=200,
                json={'instances': [{
                    'id': 1239876,
                    'name': 'copy_name'}]}
            )
        ])

        obj = self.cloud.create_rds_instance(
            availability_zone='test-az-01',
            configuration='123',
            disk_encryption_id='234',
            flavor='rds.mysql.s1.large.replica',
            name='inst_name',
            replica_of='fake_name',
            volume_size=100,
            volume_type='ULTRAHIGH'
        )

        self.assert_calls()

        self.assertEqual('copy_name', obj.name)

    def test_create_rds_instance_replica_exception(self):
        """setting port with replica not allowed"""

        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_rds_instance,
            configuration='123',
            datastore_type='MySQL',
            datastore_version='5.7',
            disk_encryption_id='234',
            flavor='test-flavor',
            replica_of='fake_name',
            ha_mode='semisync',
            name='inst_name',
            port=5432,
            region='test-region',
            volume_size=100,
            volume_type='ULTRAHIGH',
        )

        self.assert_calls()

    def test_rds_create_from_instance_pir(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='instances',
                    qs_elements=['id=source_instance']
                ),
                status_code=200,
                json={'instances': [{
                    'id': 123987,
                    'name': 'source_instance',
                    'datastore': {'type': 'MySQL', 'version': '5.7'}}]}
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    base_url_append='flavors/MySQL',
                    qs_elements=['version_name=5.7']
                ),
                status_code=200,
                json={"flavors": [
                     {
                         "vcpus": "2",
                         "ram": 8,
                         "id": "1",
                         "spec_code": "rds.mysql.s1.large",
                         "instance_mode": "single",
                         "az_status": {
                             "eu-de-02": "normal",
                             "eu-de-01": "normal",
                             "eu-de-03": "normal"},
                         "version_name": ["5.7"]}]}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['test-network-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='security-groups',
                    base_url_append='v2.0',
                    append=['test-sec_grp-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['test-vpc-id']
                ),
                json={'id': 'fake'}
            ),

            dict(
                method='POST',
                uri=self.get_rds_url(
                    resource='instances'
                ),
                status_code=200,
                json={
                    'instance': {'id': 1239876},
                    'job_id': '15'
                },
                validate=dict(
                    json={
                        'availability_zone': 'test-az-01',
                        'configuration_id': '123',
                        'datastore': {'type': 'MySQL', 'version': '5.7'},
                        'disk_encryption_id': '234',
                        'flavor_ref': 'rds.mysql.s1.large',
                        'name': 'inst_name',
                        'port': 12345,
                        'region': 'test-region',
                        'restore_point': {'instance_id': 123987,
                                          'restore_time': 'abcde',
                                          'type': 'timestamp'},
                        'security_group_id': 'fake',
                        'subnet_id': 'fake',
                        'volume': {'size': 100, 'type': 'ULTRAHIGH'},
                        'vpc_id': 'fake'}
                )
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='jobs',
                    qs_elements=['id=15']
                ),
                status_code=200,
                json={'status': 'completed'}
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='instances',
                    qs_elements=['id=1239876']
                ),
                status_code=200,
                json={'instances': [{
                    'id': 1239876,
                    'name': 'inst_name'}]}
            )
        ])

        obj = self.cloud.create_rds_instance(
            availability_zone='test-az-01',
            configuration='123',
            datastore_type='MySQL',
            datastore_version='5.7',
            disk_encryption_id='234',
            flavor='rds.mysql.s1.large',
            from_instance='source_instance',
            name='inst_name',
            network='test-network-id',
            port=12345,
            region='test-region',
            restore_time='abcde',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH'
        )

        self.assert_calls()

        self.assertEqual('inst_name', obj.name)

    def test_rds_create_from_backup(self):
        self.register_uris([
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='instances',
                    qs_elements=['id=source_instance']
                ),
                status_code=200,
                json={'instances': [{
                    'id': 123987,
                    'name': 'source_instance',
                    'datastore': {'type': 'MySQL', 'version': '5.7'}}]}
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='backups',
                    qs_elements=['instance_id=123987',
                                 'backup_id=source_backup']
                ),
                status_code=200,
                json={'backups': [{
                    'id': 12,
                    'name': 'source_backup',
                    'datastore': {'type': 'MySQL', 'version': '5.7'}}]}
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    base_url_append='flavors/MySQL',
                    qs_elements=['version_name=5.7']
                ),
                status_code=200,
                json={"flavors": [
                     {
                         "vcpus": "2",
                         "ram": 8,
                         "id": "1",
                         "spec_code": "rds.mysql.s1.large",
                         "instance_mode": "single",
                         "az_status": {
                             "eu-de-02": "normal",
                             "eu-de-01": "normal",
                             "eu-de-03": "normal"},
                         "version_name": ["5.7"]}]}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='networks',
                    base_url_append='v2.0',
                    append=['test-network-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='security-groups',
                    base_url_append='v2.0',
                    append=['test-sec_grp-id']
                ),
                json={'id': 'fake'}
            ),
            dict(
                method='GET',
                uri=self.get_mock_url(
                    'network',
                    resource='routers',
                    base_url_append='v2.0',
                    append=['test-vpc-id']
                ),
                json={'id': 'fake'}
            ),

            dict(
                method='POST',
                uri=self.get_rds_url(
                    resource='instances'
                ),
                status_code=200,
                json={
                    'instance': {'id': 1239876},
                    'job_id': '15'
                },
                validate=dict(
                    json={
                        'availability_zone': 'test-az-01',
                        'configuration_id': '123',
                        'datastore': {'type': 'MySQL', 'version': '5.7'},
                        'disk_encryption_id': '234',
                        'flavor_ref': 'rds.mysql.s1.large',
                        'name': 'inst_name',
                        'port': 12345,
                        'region': 'test-region',
                        'restore_point': {
                            'backup_id': 12,
                            'instance_id': 123987,
                            'type': 'backup'},
                        'security_group_id': 'fake',
                        'subnet_id': 'fake',
                        'volume': {'size': 100, 'type': 'ULTRAHIGH'},
                        'vpc_id': 'fake'}
                )
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='jobs',
                    qs_elements=['id=15']
                ),
                status_code=200,
                json={'status': 'completed'}
            ),
            dict(
                method='GET',
                uri=self.get_rds_url(
                    resource='instances',
                    qs_elements=['id=1239876']
                ),
                status_code=200,
                json={'instances': [{
                    'id': 1239876,
                    'name': 'inst_name'}]}
            )
        ])

        obj = self.cloud.create_rds_instance(
            availability_zone='test-az-01',
            backup='source_backup',
            configuration='123',
            datastore_type='MySQL',
            datastore_version='5.7',
            disk_encryption_id='234',
            flavor='rds.mysql.s1.large',
            from_instance='source_instance',
            name='inst_name',
            network='test-network-id',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH'
        )

        self.assert_calls()

        self.assertEqual('inst_name', obj.name)

    def test_rds_create_from_backup_no_instance(self):
        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_rds_instance,
            availability_zone='test-az-01',
            backup='source_backup',
            configuration='123',
            datastore_type='MySQL',
            datastore_version='5.7',
            disk_encryption_id='234',
            ha_mode='semisync',
            flavor='rds.mysql.s1.large',
            name='inst_name',
            network='test-network-id',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH'
        )

        self.assert_calls()

    def test_rds_create_primary_missing_params(self):
        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_rds_instance,
            availability_zone='test-az-01',
            configuration='123',
            datastore_type='MySQL',
            datastore_version='5.7',
            disk_encryption_id='234',
            ha_mode='semisync',
            flavor='rds.mysql.s1.large',
            name='inst_name',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            volume_size=100,
            volume_type='ULTRAHIGH'
        )

        self.assert_calls()

    def test_rds_create_primary_missing_datastore(self):
        self.assertRaises(
            exceptions.SDKException,
            self.cloud.create_rds_instance,
            availability_zone='test-az-01',
            configuration='123',
            disk_encryption_id='234',
            ha_mode='semisync',
            flavor='rds.mysql.s1.large',
            name='inst_name',
            network='test-network-id',
            port=12345,
            region='test-region',
            router='test-vpc-id',
            security_group='test-sec_grp-id',
            volume_size=100,
            volume_type='ULTRAHIGH'
        )

        self.assert_calls()
