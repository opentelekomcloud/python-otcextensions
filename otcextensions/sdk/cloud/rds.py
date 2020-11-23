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
import time

from openstack import exceptions


class RdsMixin:
    def create_rds_instance(self, name,
                            wait=True, wait_timeout=600, wait_interval=5,
                            **kwargs):
        """Create RDS instance with all the checks

        :param str availability_zone:
        :param str backup: Name or ID of the backup to create
            instance from (when from_instance is passed).
        :param int backup_keepdays:
        :param str backup_timeframe:
        :param str charge_mode: Charge mode.
        :param str configuration: dict(type=str),
        :param str datastore_type: dict(type=str, default='postgresql'),
        :param str datastore_version: dict(type=str),
        :param str disk_encryption_id: dict(type=str),
        :param str flavor: dict(required=True, type=str),
        :param str from_instance: Name or ID of the instance to create
            instance from (requires from_backup of restore_time).
        :param str ha_mode: HA mode. choices=['async', 'semisync', 'sync']
        :param str name: dict(required=True, type=str),
        :param str network: dict(type=str),
        :param str password: dict(type=str, no_log=True),
        :param int port: dict(type=int),
        :param str region: dict(type=str, choices=['eu-de'], default='eu -de'),
        :param str replica_of: dict(type=str),
        :param str restore_time: Restoration time.
        :param str router: dict(type=str),
        :param str security_group: dict(type=str),
        :param str volume_type: dict(required=True, type=str),
        :param int volume_size: dict(required=True, type=int),
        :param bool wait: dict(type=bool, default=True),
        :param int wait_timeout: dict(type=int, default=180)
        :param int wait_interval: Check interval.

        :returns: The results of server creation
        :rtype: :class:`~otcextensions.sdk.rds.v3.instance.Instance`
        """

        availability_zone = kwargs.get('availability_zone')
        backup = kwargs.get('backup')
        backup_keepdays = kwargs.get('backup_keepdays')
        backup_timeframe = kwargs.get('backup_timeframe')
        charge_mode = kwargs.get('charge_mode')
        configuration = kwargs.get('configuration')
        datastore_type = kwargs.get('datastore_type')
        datastore_version = kwargs.get('datastore_version')
        disk_encryption_id = kwargs.get('disk_encryption_id')
        flavor = kwargs.get('flavor')
        from_instance = kwargs.get('from_instance')
        ha_mode = kwargs.get('ha_mode')
        network = kwargs.get('network')
        password = kwargs.get('password')
        port = kwargs.get('port')
        region = kwargs.get('region')
        replica_of = kwargs.get('replica_of')
        restore_time = kwargs.get('restore_time')
        router = kwargs.get('router')
        security_group = kwargs.get('security_group')
        volume_type = kwargs.get('volume_type')
        volume_size = kwargs.get('volume_size')

        attrs = {}

        attrs['name'] = name

        if availability_zone:
            attrs['availability_zone'] = availability_zone
        if backup_keepdays and backup_timeframe:
            backup_attrs = {}
            backup_attrs['keep_days'] = backup_keepdays
            backup_attrs['start_time'] = backup_timeframe
            attrs['backup_strategy'] = backup_attrs
        elif backup_keepdays or backup_timeframe:
            raise exceptions.SDKException(
                '`backup_keepdays` and `backup_timeframe` must be passed'
                'together'
            )
        if charge_mode:
            attrs['charge_info'] = {'charge_mode': charge_mode}
        if configuration:
            # TODO(not_gtema): find configuration
            attrs['configuration_id'] = configuration
        if datastore_type:
            datastore = {
                'type': datastore_type,
                'version': datastore_version
            }
            attrs['datastore'] = datastore
        if disk_encryption_id:
            attrs['disk_encryption_id'] = disk_encryption_id
        if flavor:
            attrs['flavor_ref'] = flavor
        if ha_mode:
            ha = {'mode': 'ha', 'replication_mode': ha_mode}
            attrs['ha'] = ha
        if port:
            attrs['port'] = port
        if password:
            attrs['password'] = password
        if region:
            attrs['region'] = region

        volume = {}
        if volume_size:
            volume = {"size": volume_size}
            if volume_type:
                volume['type'] = volume_type
            attrs['volume'] = volume

        new_instance_required = [
            router,
            network,
            security_group,
            password
        ]

        if (not replica_of
                and not (datastore_type and datastore_version)):
            raise exceptions.SDKException(
                '`--datastore-type` and `--datastore-version` are '
                'required'
            )

        if replica_of:
            # Create replica
            if (
                password or port
                or router or security_group
                or network
            ):
                raise exceptions.SDKException(
                    'Setting password/port/router/network/sg is not '
                    'supported when creating replica'
                )
            src = self.rds.find_instance(replica_of, ignore_missing=False)
            datastore_type = src['datastore']['type']
            datastore_version = src['datastore']['version']
            attrs['replica_of_id'] = src.id
            attrs.pop('datastore', None)
        elif from_instance:
            source = self.rds.find_instance(
                from_instance, ignore_missing=False)
            if backup:
                # Create from backup
                backup_obj = self.rds.find_backup(
                    name_or_id=backup,
                    instance=source,
                    ignore_missing=False)
                attrs['restore_point'] = {
                    'type': 'backup',
                    'backup_id': backup_obj.id,
                    'instance_id': backup_obj.instance_id
                }
            elif restore_time:
                attrs['restore_point'] = {
                    'type': 'timestamp',
                    'restore_time': restore_time,
                    'instance_id': source.id
                }
        elif backup or restore_time:
            raise exceptions.SDKException(
                '`from-instance` is required when restoring from '
                'backup or using PITR.'
            )
        elif not all(new_instance_required):
            raise exceptions.SDKException(
                '`router`, `subnet`, `security-group`, '
                '`password` parameters are required when creating '
                'new primary instance.'
            )

        flavors = list(self.rds.flavors(
            datastore_name=datastore_type,
            version_name=datastore_version)
        )
        flavor_obj = None
        for f in flavors:
            if f.name == flavor:
                flavor_obj = f
        if not flavor_obj:
            raise exceptions.SDKException(
                'Flavor {flavor} can not be found'.format(
                    flavor=flavor)
            )
        if flavor_obj.instance_mode == 'ha' and not ha_mode:
            raise exceptions.SDKException(
                '`ha_mode` is required when using HA enabled flavor'
            )
        if flavor_obj.instance_mode != 'ha' and ha_mode:
            raise exceptions.SDKException(
                '`ha` enabled flavor must be '
                'chosen when setting ha_mode'
            )
        if flavor_obj.instance_mode != 'replica' and replica_of:
            raise exceptions.SDKException(
                '`replica` enabled flavor must be '
                'chosen when creating replica'
            )
        if ha_mode:
            if ',' not in availability_zone:
                raise exceptions.SDKException(
                    'List of availability zones must be used when '
                    'creating ha instance'
                )
        if ha_mode:
            mode = ha_mode
            if (datastore_type.lower() == 'postgresql'
                    and mode not in ['async', 'sync']):
                raise exceptions.SDKException(
                    '`async` or `sync` ha_mode can be used for '
                    'PostgreSQL isntance'
                )
            elif (datastore_type.lower() == 'mysql'
                    and mode not in ['async', 'semisync']):
                raise exceptions.SDKException(
                    '`async` or `semisync` ha_mode can be used for '
                    'MySQL isntance'
                )
            elif (datastore_type.lower() == 'sqlserver'
                    and mode not in ['sync']):
                raise exceptions.SDKException(
                    'Only `sync` ha_mode can be used for '
                    'SQLServer isntance'
                )
        if wait_interval and not wait:
            raise exceptions.SDKException(
                '`wait-interval` is only valid with `wait`'
            )
        if network:
            network_obj = self.network.find_network(
                network, ignore_missing=False)
            attrs['network_id'] = network_obj.id
        if security_group:
            security_group_obj = self.network.find_security_group(
                security_group, ignore_missing=False)
            attrs['security_group_id'] = security_group_obj.id
        if router:
            router_obj = self.network.find_router(router, ignore_missing=False)
            attrs['router_id'] = router_obj.id

        obj = self.rds.create_instance(**attrs)

        if obj.job_id and wait:
            wait_args = {}
            if wait_interval:
                wait_args['interval'] = wait_interval
            if wait_timeout:
                wait_args['wait'] = wait_timeout

            # RDS is so bad, that job_id appears only some time after it is
            # returned
            time.sleep(10)

            self.rds.wait_for_job(obj.job_id, **wait_args)
            obj = self.rds.get_instance(obj.id)

        return obj

    def delete_rds_instance(
        self, instance, wait=True, wait_timeout=180, wait_interval=5
    ):
        """Delete RDS instance

        :param str instance: Name, ID or instance
        :param bool wait: dict(type=bool, default=True),
        :param int wait_timeout: dict(type=int, default=180)
        :param int wait_interval: Check interval.
        """

        inst = self.rds.find_instance(instance, ignore_missing=False)

        obj = self.rds.delete_instance(inst.id)

        if obj.job_id and wait:
            wait_args = {}
            if wait_interval:
                wait_args['interval'] = wait_interval
            if wait_timeout:
                wait_args['wait'] = wait_timeout

            # RDS is so bad, that job_id appears only some time after it is
            # returned
            time.sleep(10)

            self.rds.wait_for_job(obj.job_id, **wait_args)
