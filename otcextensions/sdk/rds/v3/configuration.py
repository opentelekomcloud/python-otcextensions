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
from openstack import utils

from otcextensions.sdk.rds.v3 import _base


class Configuration(_base.Resource):

    base_path = '/configurations'
    resources_key = 'configurations'
    resource_key = 'configuration'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_commit = True
    allow_fetch = True
    allow_list = True

    #: Id of the configuration group
    configuration_id = resource.Body('configuration_id')
    configuration_name = resource.Body('configuration_name')
    #: *Type:str*
    id = resource.Body('id', alias='configuration_id')
    #: Name of the configuration group
    #: *Type:str*
    name = resource.Body('name', alias='configuration_name')
    #: Data store information
    #: *Type: dict*
    datastore = resource.Body('datastore', type=dict)
    #: Description of the configuration group
    #: *Type:str*
    description = resource.Body('description')
    #: Name of Datastore version
    #: *Type:str*
    datastore_version_name = resource.Body('datastore_version_name')
    #: Name of Datastore
    #: *Type:str*
    datastore_name = resource.Body('datastore_name')
    #: Individual Configuration values
    #: *Type:dict*
    configuration_parameters = resource.Body('configuration_parameters',
                                             type=list)
    #: Date of created
    #: *Type:str*
    created_at = resource.Body('created')
    #: Date of updated
    #: *Type:str*
    updated_at = resource.Body('updated')
    #: Indicates whether the parameter group is created by users.
    #: *Type:bool*
    is_user_defined = resource.Body('user_defined', type=bool)
    #: parameter group values defined by users
    #: *Type: dict*
    values = resource.Body('values', type=dict)

    #: Results of the configuration apply per instance
    #: *Type:list*
    apply_results = resource.Body('apply_results', type=list)

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True, **params):
        instance = super(Configuration, cls).find(
            session, name_or_id,
            ignore_missing=ignore_missing,
            **params)
        if instance:
            return instance.fetch(session)
        return

    def create(self, session, prepend_key=False, base_path=None):
        return super(Configuration, self).create(session,
                                                 prepend_key=prepend_key,
                                                 base_path=base_path)

    def commit(self, session, prepend_key=False, **further_attrs):
        return super(Configuration, self).commit(
            session,
            prepend_key=prepend_key,
            **further_attrs)

    def apply(self, session, instances):
        """Apply configuration to the given instances
        """
        url = utils.urljoin(self.base_path, self.id, 'apply')
        body = {'instance_ids': instances}
        response = session.put(
            url,
            json=body)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
