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


class Message(_base.Resource):

    resources_key = 'messages'
    base_path = '/queues/%(queue_id)s/messages'

    # capabilities
    allow_create = True

    # Properties
    #: Queue id
    queue_id = resource.URI('queue_id')
    messages = resource.Body('messages', type=list)
