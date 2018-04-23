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

class GroupSpec(_base.Resource):
    # Properties
    #: Consume group Id
    id = resource.Body('id')    
    #: Name
    name = resource.Body('name')
    #: Consume group name
    name = resource.Body('name')
    #: Total message number, not including deleted message
    #: *Type: int*
    produced_messages = resource.Body('produced_messages', type=int)
    #: Consumed message number
    #: *Type: int*
    consumed_messages = resource.Body('consumed_messages', type=int)
    #: Available message number
    #: *Type: int*
    available_messages = resource.Body('available_messages', type=int)    
    #: Total deadletters number
    #: *Type: int*
    produced_deadletters = resource.Body('produced_deadletters', type=int)
    #: Available deadletters number
    #: *Type: int*
    available_deadletters = resource.Body('available_deadletters', type=int)    


class Group(GroupSpec):

    resources_key = 'groups'

    base_path = 'queues/%(queue_id)s/groups'
    service = dms_service.DmsService()

    # capabilities
    allow_create = True
    allow_list = True
    allow_delete = True

    # Properties
    #: Queue id
    queue_id = resource.URI('queue_id')
    #: groups (mandatory)
    groups = resource.Body('groups', type=list, list_type=GroupSpec)
    #: Redrive policy
    redrive_policy = resource.Body('redrive_policy')    


"""     # This does a post and return a list of self
    @classmethod
    def create_groups(cls, session, queue_id=queue_id, **kwargs):
        uri = cls.base_path % {'queue_id': queue_id}

        headers = {}
        headers.update({'Content-type': 'application/json'})
        headers.update({'Content-Length': str(len(str(kwargs)))})

        response = session.post(uri,json=kwargs, headers=headers)

        if response is not None:
            response = response.json()
            resp = response['groups']

            ret = []
            for r in resp:
                r['queue_id'] = queue_id
                ret.append(cls.existing(**r))

            return ret """

