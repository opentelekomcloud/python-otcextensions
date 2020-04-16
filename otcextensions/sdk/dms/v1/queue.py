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
from openstack import resource

from otcextensions.sdk.dms.v1 import _base


class Queue(_base.Resource):

    resources_key = 'queues'

    base_path = '/queues'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'include_deadletter',
        'include_messages_num'
    )

    # Properties
    #: Created time
    #: *Type: int*
    created = resource.Body('created', type=int)
    #: Description for the queue.
    #: The value is a string of a maximum of 160 characters and cannot
    #: contain the angle brackets (<>).
    description = resource.Body('description')
    #: Queue Id
    id = resource.Body('id')
    #: Max consume count number
    #: *Type: int*
    #: Value range: 1–100.
    max_consume_count = resource.Body('max_consume_count', type=int)
    #: Queue name
    name = resource.Body('name')
    #: Queue mode:
    #: `NORMAL`: Standard queue, which supports high concurrency performance
    #: but cannot guarantee that messages are retrieved in the exact
    #: sequence as how they are received.
    #: `FIFO`: First-in-first-out (FIFO) queue, which guarantees that messages
    #: are retrieved in the exact sequence as how they are received.
    #: `KAFKA_HA`: High-reliability Kafka queue. All message replicas are
    #: flushed to a disk synchronously, ensuring message reliability.
    #: `KAFKA_HT`: High-throughput Kafka queue. All message replicas are
    #: flushed to a disk asynchronously, ensuring high performance.
    queue_mode = resource.Body('queue_mode')
    #: Redrive policy.
    #: Supported values: `enable`, `disable`. Default: `disable
    redrive_policy = resource.Body('redrive_policy')
    #: Indicates the hours of storing messages in the Kafka queue.
    #: This parameter is valid only when queue_mode is set to KAFKA_HA or
    #: KAFKA_HT. Value range: 1–72.
    #: *Type: int*
    retention_hours = resource.Body('retention_hours', type=int)
