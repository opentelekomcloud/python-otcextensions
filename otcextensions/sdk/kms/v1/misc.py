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

from otcextensions.sdk.kms.v1 import _base


class Random(_base.Resource):

    create_path = '/kms/gen-random'

    allow_create = True
    allow_get = False

    # Properties
    #: Random data length
    #: *Type:str*
    random_data_length = resource.Body('random_data_length', type=int)
    #: Random data content

    #: *Type:str*
    random_data = resource.Body('random_data')


class InstanceNumber(_base.Resource):

    base_path = 'kms/user-instances'
    allow_fetch = True
    # Properties
    #: Instance number
    #: *Type: int*
    instance_num = resource.Body('instance_num', type=int)

    def fetch(self, session):
        return super(InstanceNumber, self).fetch(session, requires_id=False)


class Quota(_base.Resource):

    base_path = 'kms/user-quotas'
    # Properties
    # Resource type
    type = resource.Body('type')
    #: Used resource
    #: *Type: int*
    used = resource.Body('used', type=int)
    #: Quota number for this kind of resource
    #: *Type: int*
    quota = resource.Body('quota', type=int)

    @classmethod
    def list(cls, session):
        session = cls._get_session(session)
        url = cls.base_path
        response = session.get(url)
        resp = response.json()
        if 'error' in resp:
            return
        resources = resp['quotas']['resources']
        for r in resources:
            value = cls.existing(**r)
            yield value
