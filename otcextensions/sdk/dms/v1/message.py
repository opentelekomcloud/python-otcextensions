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


from otcextensions.sdk.dms import dms_service
#from otcextensions.sdk.dms.v1 import dmsresource as _base
from otcextensions.sdk.dms.v1 import _base
from otcextensions.sdk import sdk_resource
_logger= _log.setup_logging('openstack')

class Message(_base.Resource):

    # No response for this post method
    base_path = '/queues/%(queue_id)s/messages'

    service = dms_service.DmsService()

    # capabilities
    allow_create = True

    # Properties
    #: Queue id
    queue_id = resource.URI('queue_id')

    # @classmethod
    # def create_messages(cls, session, queue_id=queue_id, **kwargs):
    #     uri = cls.base_path % {'queue_id': queue_id}

    #     headers = {}
    #     headers.update({'Content-type': 'application/json'})
    #     headers.update({'Content-Length': str(len(str(kwargs)))})

    #     response = session.post(uri,json=kwargs, headers=headers)

    #     return response
