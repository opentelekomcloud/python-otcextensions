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

from openstack import _log
from openstack import resource

from otcextensions.sdk.rds import rds_service

from otcextensions.sdk.rds.v1 import _base


_logger = _log.setup_logging('openstack')


class InstanceConfiguration(_base.Resource):
    # TODO(agoncharov)

    base_path = '/%(project_id)s/instances/%(instanceId)s/configuration'
    resource_key = 'instance'
    service = rds_service.RdsService()

    # capabilities
    allow_get = True

    # Properties
    # Instance of the configuration
    instanceId = resource.URI("instanceId")
    #: Configuration list, key value pairs
    #: *Type:dict*
    configuration = resource.Body('configuration', type=dict)


class Parameter(_base.Resource):
    # TODO(agoncharov)

    base_path = '/%(project_id)s/datastores/versions/%(datastore_version_id)s/parameters/'
    resources_key = 'configuration-parameters'
    service = rds_service.RdsService()

    # capabilities
    allow_list = True
    allow_get = True

    # Properties
    #: Parameter name
    name = resource.Body('name', alternate_id=True)
    #: Minimum value of the parameter
    #: *Type: int*
    min = resource.Body('min', type=int)
    #: Maximum value of the parameter
    #: *Type: int*
    max = resource.Body('max', type=int)
    #: Parameter type
    type = resource.Body('type')
    #: Value range
    value_range = resource.Body('value_range')
    #: Description
    description = resource.Body('description')
    #: Require restart or not
    #: *Type: bool*
    restart_required = resource.Body('restart_required', type=bool)
    #: Datastore version id
    datastore_version_id = resource.Body('datastore_version_id')


class ParameterGroup(_base.Resource):

    base_path = '/%(project_id)s/configurations'
    resource_key = 'configuration'
    resources_key = 'configurations'
    service = rds_service.RdsService()

    # capabilities
    allow_create = True
    allow_delete = True
    allow_update = True
    allow_get = True
    allow_list = True

    # Properties
    #: Id of the configuration group
    id = resource.Body('id')
    #: Name of the configuration group
    name = resource.Body('name')
    #: Description of the configuration group
    description = resource.Body('description')
    #: Id of Datastore version
    datastore_version_id = resource.Body('datastore_version_id')
    #: name of Datastore version
    datastore_version_name = resource.Body('datastore_version_name')
    #: name of Datastore
    datastore_name = resource.Body('datastore_name')
    #: Date of created
    created = resource.Body('created')
    #: Date of updated
    updated = resource.Body('updated')
    #: Allow update or not, 0 for not allowed
    #: *Type:int*
    allowed_updated = resource.Body('allowed_updated', type=int)
    #: Count of associated instance
    #: *Type:int*
    instance_count = resource.Body('instance_count', type=int)
    #: Params values
    #: *Type:dict*
    values = resource.Body('values', type=dict)
    #: Parameter list
    #: *Type:dict*
    parameters = resource.Body('parameters', type=dict)
    #: Datastore dict
    #: *Type:dict*
    datastore = resource.Body('datastore', type=dict)

    # def get_associated_instances(self, session):
    #     """Get associated instancs"""
    #     url = utils.urljoin(self.base_path, self._get_id(self), 'instances')
    #     endpoint_override = self.service.get_endpoint_override()
    #     # construct full http url for rds_os as rds wont' return correct
    #     # endpoint for now and work around with get_endpoint()
    #     if endpoint_override is None:
    #         url = self._get_custom_url(session, url)
    #
    #     resp = session.get(url, endpoint_filter=self.service,
    #                        endpoint_override=endpoint_override,
    #                        headers={"Accept": "application/json",
    #                                 "Content-type": "application/json"})
    #     resp = resp.json()
    #
    #     if resp:
    #         return resp['instances']
    #
    # def patch(self, session, **kwargs):
    #     url = utils.urljoin(self.base_path, self._get_id(self))
    #     endpoint_override = self.service.get_endpoint_override()
    #     body = {
    #         "configuration": {
    #             "values": kwargs
    #         }
    #     }
    #
    #     if endpoint_override is None:
    #         url = self._get_custom_url(session, url)
    #
    #     resp = session.patch(url, endpoint_filter=self.service,
    #                          endpoint_override=endpoint_override,
    #                          headers={"Accept": "application/json",
    #                                   "Content-type": "application/json"},
    #                          json=body)
    #     resp = resp.json
    #     if 'errCode' in resp:
    #         if resp['errorCode'] == 'RDS.0041':
    #             self._body.attributes.update({"values": kwargs})
    #             self._body.clean()
    #             return self
    #
    #     return resp
    #
    # def delete(self, session):
    #     request = self._prepare_request()
    #     endpoint_override = self.service.get_endpoint_override()
    #     if endpoint_override is None:
    #         request.uri = self._get_custom_url(session, request.uri)
    #
    #     response = session.delete(request.uri, endpoint_filter=self.service,
    #                               endpoint_override=endpoint_override,
    #                               headers=request.headers)
    #
    #     self._translate_response(response, has_body=False)
    #     return self
