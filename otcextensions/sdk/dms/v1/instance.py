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


class Instance(_base.Resource):
    """DMS Instance resource"""
    resources_key = 'instances'
    base_path = '/instances'

    _query_mapping = resource.QueryParameters(
        'engine', 'name', 'status', 'include_failure',
        'exact_match_name',
        include_failure='includeFailure',
        exact_match_name='exactMatchName'
    )

    # capabilities
    allow_list = True
    allow_fetch = True
    allow_create = True
    allow_delete = True
    allow_commit = True

    #: Properties
    #: The username of an instance.
    access_user = resource.Body('access_user')
    #: List of availability zones the instance belongs to
    availability_zones = resource.Body('available_zones', type=list)
    #: Billing mode
    charging_mode = resource.Body('charging_mode')
    #: IP address of the instance
    connect_address = resource.Body('connect_address')
    #: Instance creation time
    created_at = resource.Body('created_at')
    #: Instance description
    description = resource.Body('description')
    #: Message engine.
    engine = resource.Body('engine')
    #: Engine version
    engine_version = resource.Body('engine_version')
    #: Instance id
    instance_id = resource.Body('instance_id', alternate_id=True)
    #: Associate floating IP
    is_public = resource.Body('enable_publicip', type=bool)
    #: Enable SSL
    is_ssl = resource.Body('ssl_enable', type=bool)
    #: Kafka public status
    kafka_public_status = resource.Body('kafka_public_status')
    #: End time of the maintenance window
    maintenance_end = resource.Body('maintain_end')
    #: Beginning of the maintenance window
    maintenance_start = resource.Body('maintain_begin')
    #: Maximum number of partitions
    max_partitions = resource.Body('partition_num', type=int)
    #: User password
    password = resource.Body('password')
    #: Port number of the instance
    port = resource.Body('port', type=int)
    #: Product ID
    product_id = resource.Body('product_id')
    #: Bandwidth of the public access
    public_bandwidth = resource.Body('public_bandwidth', type=int)
    #: Retention policy
    retention_policy = resource.Body('retention_policy')
    #: Router ID
    router_id = resource.Body('vpc_id')
    #: Router name
    router_name = resource.Body('vpc_name')
    #: Security group ID
    security_group_id = resource.Body('security_group_id')
    #: Security group Name
    security_group_name = resource.Body('security_group_name')
    #: Service type
    service_type = resource.Body('service_type')
    #: specification of the instance
    spec = resource.Body('specification')
    #: Specification code of the instance:
    #:  `dms.instance.kafka.cluster.c3.min`
    #:  `dms.instance.kafka.cluster.c3.small.2`
    #:  `dms.instance.kafka.cluster.c3.middle.2`
    #:  `dms.instance.kafka.cluster.c3.high.2`
    spec_code = resource.Body('resource_spec_code')
    #: Instance status
    #: CREATING, CREATEFAILED, RUNNING, ERROR, STARTING,
    #: RESTARTING, CLOSING, FROZEN
    status = resource.Body('status')
    #: Storage resource ID
    storage_resource_id = resource.Body('storage_resource_id')
    #: Storage I/O specification code
    storage_spec_code = resource.Body('storage_spec_code')
    #: Storage type
    storage_type = resource.Body('storage_type')
    #: Storage space GB
    storage = resource.Body('storage_space', type=int)
    #: Subnet ID
    subnet_id = resource.Body('subnet_id')
    #: Total storage space GB
    total_storage = resource.Body('total_storage_space', type=int)
    #: Instance type
    type = resource.Body('type')
    #: Used storage GB
    used_storage = resource.Body('used_storage_space', type=int)
    #: User ID
    user_id = resource.Body('user_id')
    #: User name
    user_name = resource.Body('user_name')

    def _action(self, session, action, id_list):
        body = {
            'action': action,
            'instances': id_list
        }

        response = session.post(
            '/instances/action',
            body
        )

        exceptions.raise_from_response(response)

        return

    def restart(self, session):
        """Restart specified instances
        """
        return self._action(session, 'restart', [self.id])

    def restart_batch(self, session, id_list):
        return self._action(session, 'restart', id_list)

    def delete_batch(self, session, id_list):
        """Delete batch of instances
        """
        return self._action(session, 'delete', id_list)

    def delete_failed(self, session):
        body = {
            'action': 'delete',
            'allFailure': 'kafka'
        }

        response = session.post(
            '/instances/action',
            body
        )
        exceptions.raise_from_response(response)
        return
