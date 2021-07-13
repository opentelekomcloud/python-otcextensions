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
    def create_dds_instance(self,
                            name: str,
                            router,
                            network,
                            security_group,
                            flavors: list,
                            password: str,
                            region='eu-de',
                            availability_zone='eu-de-01',
                            datastore_type='DDS-Community',
                            datastore_storage_engine='wiredTiger',
                            datastore_version='3.2',
                            mode='ReplicaSet',
                            disk_encryption_id: str = None,
                            backup_timeframe: str = None,
                            backup_keepdays: str = None,
                            ssl_option: str = None
                            ):
        """

        :param name: instance name, dict(required=True, type=str)
        :param router: router name or id, dict(type=str)
        :param network: network name or id, dict(type=str)
        :param security_group: sg name or id, dict(type=str)
        :param flavors: list of flavors,
            dict(type=list, elements=dict)
        :param password: password, dict(type=str, no_log=True)
        :param region: dict(type=str, default='eu-de')
        :param availability_zone: dict(type=str, default='eu-de-01'),
        :param datastore_type: dict(type=str, default='DDS-Community')
        :param datastore_storage_engine:
            dict(type=str, default='wiredTiger')
        :param datastore_version: dict(type=str, choices=['3.2', '3.4']),
        :param mode: dict(choices=['Sharding', 'ReplicaSet'],
            default='ReplicaSet')
        :param disk_encryption_id: dict(type=str)
        :param backup_timeframe: dict(type=str)
        :param backup_keepdays: dict(type=str)
        :param ssl_option: dict(type=str, choices=['0', '1'])

        :returns: The results of instance creation
        :rtype: :class:`~otcextensions.sdk.dds.v3.instance.Instance`
        """

        attrs = {}
        attrs['name'] = name
        attrs['region'] = region
        attrs['availability_zone'] = availability_zone
        attrs['password'] = password

        datastore = {
            'type': datastore_type,
            'version': datastore_version,
            'storage_engine': datastore_storage_engine
        }
        attrs['datastore'] = datastore

        router_obj = self.network.find_router(router, ignore_missing=False)
        attrs['vpc_id'] = router_obj.id

        network_obj = self.network.find_network(network, ignore_missing=False)
        attrs['subnet_id'] = network_obj.id

        security_group_obj = self.network.find_security_group(
            security_group, ignore_missing=False)
        attrs['security_group_id'] = security_group_obj.id

        if disk_encryption_id:
            attrs['disk_encryption_id'] = disk_encryption_id

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
            attrs['backup_strategy'] = {
                'keep_days': backup_keepdays,
                'start_time': backup_timeframe
            }
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
