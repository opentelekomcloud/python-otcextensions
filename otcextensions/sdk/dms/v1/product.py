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
from openstack import resource

from otcextensions.sdk.dms.v1 import _base


class Product(_base.Resource):
    """DMS Product resource"""
    base_path = '/products'
    resources_key = 'Hourly'

    # capabilities
    allow_list = True

    #: Properties
    engine_name = resource.Body('engine_name')
    engine_version = resource.Body('engine_version')
    #: Indicates the maximum number of messages per unit time.
    tps = resource.Body('tps')
    #: Indicates the message storage space.
    storage = resource.Body('storage')
    #: Indicates the maximum number of topics in a Kafka instance.
    partition_num = resource.Body('partition_num')
    #: Indicates the product ID.
    product_id = resource.Body('product_id')
    #: Indicates the specification ID.
    spec_code = resource.Body('spec_code')
    #: Indicates the I/O information.
    io = resource.Body('io', type=list, list_type=dict)
    #: Indicates the bandwidth of a Kafka instance.
    bandwidth = resource.Body('bandwidth')
    #: Indicates AZs where there are available resources.
    availability_zones = resource.Body('available_zones', type=list)
    #: Indicated AZs where it is not available
    unavailable_zones = resource.Body('unavailable_zones', type=list)
    #: Indicates the VM specifications of the instance resources.
    vm_flavor_id = resource.Body('ecs_flavor_id')
    #: Indicates the instance architecture type.
    #: Currently, only x86 is supported.
    arch_type = resource.Body('arch_type')

    @classmethod
    def list(cls, session, **params):
        # This API is a total disaster (b*****it)
        # Show me who was so smart to develop it...
        session = cls._get_session(session)

        base_path = cls.base_path
        params.pop('paginated', None)
        params.pop('base_path', None)
        params = cls._query_mapping._validate(
            params, base_path=base_path,
            allow_unknown_params=False)
        query_params = cls._query_mapping._transpose(params, cls)
        uri = base_path % params

        # Copy query_params due to weird mock unittest interactions
        response = session.get(
            uri,
            endpoint_override=session.endpoint_override.replace(
                '%(project_id)s', ''),
            headers={"Accept": "application/json"},
            params=query_params.copy())
        exceptions.raise_from_response(response)
        data = response.json()

        for k, v in data.items():
            for rec in v:
                engine = rec
                engine_name = engine.get('name')
                engine_version = engine.get('version')
                for madness in engine.get('values', []):
                    for spec in madness.get('detail', []):
                        value = cls.existing(
                            connection=session._get_connection(),
                            engine_name=engine_name,
                            engine_version=engine_version,
                            **spec)
                        yield value
