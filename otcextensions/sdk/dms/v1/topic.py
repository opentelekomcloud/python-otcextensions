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


class Topic(_base.Resource):
    """DMS Topic resource"""
    resources_key = 'topics'
    base_path = '/instances/%(instance_id)s/topics'

    # capabilities
    allow_list = True
    allow_create = True
    allow_delete = True

    instance_id = resource.URI('instance_id')

    #: Properties
    #: Synchronous flushing. Default=false
    is_sync_flush = resource.Body('sync_message_flush', type=bool)
    #: Synchronous replication. Default=false. With replication=1 can be only
    #: false
    is_sync_replication = resource.Body('sync_replication', type=bool)
    #: Number of partitions. Default=3
    partition = resource.Body('partition', type=int)
    #: Replication factor. Default=3
    replication = resource.Body('replication', type=int)
    #: Retention time in hours. Default=72
    retention_time = resource.Body('retention_time', type=int)
