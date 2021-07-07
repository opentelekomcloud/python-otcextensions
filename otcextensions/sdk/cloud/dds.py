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
from openstack import exceptions


class DdsMixin:
    def create_dds_instance(
            self, name,
            wait=True,
            wait_timeout=600,
            wait_interval=5,
            **kwargs
    ):
        """Create DDS instance with all the checks

        :param str name: dict(required=True, type=str),
        :param str datastore_type: dict(type=str, default='DDS-Community'),
        :param str datastore_version: dict(type=str),
        :param str datastore_storage_engine: dict(type=str, default='wiredTiger'),
        :param str region: dict(type=str, choices=['eu-de, eu-nl'], default='eu-de'),
        :param str availability_zone: dict(type=str),
        :param str router: dict(type=str),
        :param str network: dict(type=str),
        :param str security_group: dict(type=str),
        :param str password: dict(type=str, no_log=True),
        :param str disk_encryption_id: dict(type=str),
        :param str mode: choices=['Sharding', 'ReplicaSet']
        :param str flavor: dict(required=True, type=list, elements=dict),
        :param str backup_timeframe: dict(type=str),
        :param str backup_keepdays: dict(type=str),
        :param str ssl_option: dict(type=str),

        :returns: The results of instance creation
        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """

        datastore_type = kwargs.get('datastore_type')
        datastore_version = kwargs.get('datastore_version')
        datastore_storage_engine = kwargs.get('datastore_storage_engine')
        region = kwargs.get('region')
        availability_zone = kwargs.get('availability_zone')
        router = kwargs.get('router')
        network = kwargs.get('network')
        security_group = kwargs.get('security_group')
        password = kwargs.get('password')
        disk_encryption_id = kwargs.get('disk_encryption_id')
        mode = kwargs.get('mode')
        flavor = kwargs.get('flavor')
        backup_timeframe = kwargs.get('backup_timeframe')
        backup_keepdays = kwargs.get('backup_keepdays')
        ssl_option = kwargs.get('ssl_option')

        attrs = {}
        attrs['name'] = name

        if datastore_type:
            datastore = {
                'type': datastore_type,
                'version': datastore_version,
                'storage_engine': datastore_storage_engine
            }
            attrs['datastore'] = datastore
        elif datastore_type or datastore_version or datastore_storage_engine:
            raise exceptions.SDKException(
                '`datastore_type` and `datastore_version`'
                ' and `datastore_storage_engine` must be passed together'
            )

        if region:
            if region not in ['eu-de', 'eu-nl']:
                raise exceptions.SDKException(
                    '`eu-de` or `eu-nl` are supported values'
                )
            attrs['region'] = region

        if availability_zone:
            attrs['availability_zone'] = availability_zone

        if router:
            router_obj = self.network.find_router(router, ignore_missing=False)
            attrs['vpc_id'] = router_obj.id

        if network:
            network_obj = self.network.find_network(
                network, ignore_missing=False)
            attrs['subnet_id'] = network_obj.id

        if security_group:
            security_group_obj = self.network.find_security_group(
                security_group, ignore_missing=False)
            attrs['security_group_id'] = security_group_obj.id

        if password:
            attrs['password'] = password

        if disk_encryption_id:
            attrs['disk_encryption_id'] = disk_encryption_id

        if mode:
            if mode not in ['Sharding', 'ReplicaSet']:
                raise exceptions.SDKException(
                    '`Sharding` or `ReplicaSet` are supported values'
                )
            attrs['mode'] = mode

        if flavor:
            # need to add
            print()

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

        if ssl_option:
            attrs['ssl_option'] = ssl_option

        if wait_interval and not wait:
            raise exceptions.SDKException(
                '`wait-interval` is only valid with `wait`'
            )

        obj = self.dds.create_instance(**attrs)

        if obj.job_id and wait:
            wait_args = {}
            if wait_interval:
                wait_args['interval'] = wait_interval
            if wait_timeout:
                wait_args['wait'] = wait_timeout

        obj = self.dds.get_instance(obj.id)

        return obj

    def delete_dds_instance(
            self, instance, wait=True, wait_timeout=180, wait_interval=5
    ):
        """Delete DDS instance

        :param str instance: Name, ID or instance
        :param bool wait: dict(type=bool, default=True),
        :param int wait_timeout: dict(type=int, default=180)
        :param int wait_interval: Check interval.
        """

        inst = self.dds.find_instance(instance, ignore_missing=False)

        obj = self.dds.delete_instance(inst.id)

        if obj.job_id and wait:
            wait_args = {}
            if wait_interval:
                wait_args['interval'] = wait_interval
            if wait_timeout:
                wait_args['wait'] = wait_timeout

            self.dds.wait_for_job(obj.job_id, **wait_args)
