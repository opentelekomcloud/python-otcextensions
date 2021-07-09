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
    def create_dds_instance(self, name, **kwargs):
        """Create DDS instance with all the checks

        :param str name: dict(required=True, type=str),
        :param str datastore_type: dict(type=str, default='DDS-Community'),
        :param str datastore_version: dict(type=str),
        :param str datastore_storage_engine:
            dict(type=str, default='wiredTiger'),
        :param str region:
            dict(type=str, default='eu-de'),
        :param str availability_zone: dict(type=str),
        :param str router: dict(type=str),
        :param str network: dict(type=str),
        :param str security_group: dict(type=str),
        :param str password: dict(type=str, no_log=True),
        :param str disk_encryption_id: dict(type=str),
        :param str mode: choices=['Sharding', 'ReplicaSet']
        :param str flavors: dict(required=True, type=list, elements=dict),
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
        flavors = kwargs.get('flavors')
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
        elif datastore_version or datastore_storage_engine:
            raise exceptions.SDKException(
                '`datastore_type` and `datastore_version`'
                ' and `datastore_storage_engine` must be passed together'
            )

        if region:
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

        flavors_ref = list(self.dds.flavors(
            region=region,
            engine_name=datastore_type)
        )
        flavors_specs = [flavor.spec_code for flavor in flavors_ref]
        if flavors:
            for flavor in flavors:
                if flavor['type'] in ['mongos', 'shard'] \
                        and flavor['num'] not in range(2, 16):
                    raise exceptions.SDKException(
                        '`num` value must be in ranges from 2 to 16 '
                        'for mongos and shard'
                    )
                if flavor['type'] in ['config', 'replica'] \
                        and flavor['num'] != 1:
                    raise exceptions.SDKException(
                        '`num` value must be 1 '
                        'for config and replica'
                    )
                if flavor['type'] == 'mongos':
                    if all(k in flavor for k in ('storage', 'size')):
                        raise exceptions.SDKException(
                            '`storage` and `size` parameters'
                            ' is invalid for the mongos nodes'
                        )
                if 'size' in flavor:
                    if flavor['type'] == 'replica' \
                            and not (10 <= flavor['size'] <= 2000):
                        raise exceptions.SDKException(
                            '`size` value for `replica` must be'
                            ' between 10 and 2000 GB.'
                        )
                    elif flavor['type'] == 'config' \
                            and flavor['size'] != 20:
                        raise exceptions.SDKException(
                            '`size` value for `config` must be 20 GB.'
                        )
                    elif not (10 <= flavor['size'] <= 1000):
                        raise exceptions.SDKException(
                            '`size` value for `shard` must be'
                            ' between 10 and 1000 GB.'
                        )
                if flavor['spec_code'] not in flavors_specs:
                    raise exceptions.SDKException(
                        '`spec_code` not valid'
                    )
            attrs['flavor'] = flavors

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

        obj = self.dds.create_instance(**attrs)
        obj = self.dds.get_instance(obj.id)

        return obj

    def delete_dds_instance(self, instance):
        """Delete DDS instance

        :param str instance: Name or ID of instance
        """

        inst = self.dds.find_instance(
            name_or_id=instance,
            ignore_missing=False
        )
        self.dds.delete_instance(inst.id)

        return None
