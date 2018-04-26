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
from openstack import _log

from otcextensions.sdk.dms.v1 import _base
_logger = _log.setup_logging('openstack')


class Queue(_base.Resource):

    resources_key = 'queues'

    base_path = '/queues'

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True

    # Properties
    #: Queue Id
    id = resource.Body('id')
    #: Queue name
    name = resource.Body('name')
    #: Queue mode
    queue_mode = resource.Body('queue_mode')
    #: Description for the queue
    description = resource.Body('description')
    #: Redrive policy
    redrive_policy = resource.Body('redrive_policy')
    #: Max consume count number
    #: *Type: int*
    max_consume_count = resource.Body('max_consume_count', type=int)
    #: Retentions hours
    #: *Type: int*
    retention_hours = resource.Body('retention_hours', type=int)
    #: Created time
    #: *Type: int*
    created = resource.Body('created', type=int)


class Quota(_base.Resource):

    base_path = '/quotas/dms'

    allow_list = True

    # Properties
    #: Quota resource type
    type = resource.Body('type')
    #: Quota of this resource
    #: *Type: int*
    quota = resource.Body('quota', type=int)
    #: Used of this resource
    #: *Type: int*
    used = resource.Body('used', type=int)

    @classmethod
    def list(cls, session, paginated=False, **params):

        more_data = True
        query_params = cls._query_mapping._transpose(params)
        uri = cls.base_path % params
        headers = {"Accept": "application/json",
                   "Content-type": "application/json"}

        while more_data:
            resp = session.get(
                uri,
                headers=headers,
                params=query_params)
            resp = resp.json()

            # Quota for dms are a list of resources
            resp = resp['quotas']['resources']

            if not resp:
                more_data = False

            # Keep track of how many items we've yielded. If we yielded
            # less than our limit, we don't need to do an extra request
            # to get back an empty data set, which acts as a sentinel.
            yielded = 0
            new_marker = None
            for data in resp:

                value = cls.existing(**data)
                new_marker = value.id
                yielded += 1
                yield value

            if not paginated:
                return
            if "limit" in query_params and yielded < query_params["limit"]:
                return
            query_params["limit"] = yielded
            query_params["marker"] = new_marker
