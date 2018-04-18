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
from openstack import exceptions
from openstack import resource
from openstack import utils

from otcextensions.sdk import sdk_resource
from otcextensions.sdk.rds import rds_service

_logger = _log.setup_logging('openstack')


# class InstanceConfiguration(sdk_resource.Resource):
#     # TODO(agoncharov) most likely useless
#
#     base_path = '/%(project_id)s/instances/%(instanceId)s/configuration'
#     resource_key = 'instance'
#     service = rds_service.RdsService()
#
#     # capabilities
#     allow_get = True
#
#     # Properties
#     # Instance of the configuration
#     instanceId = resource.URI("instanceId")
#     #: Configuration list, key value pairs
#     #: *Type:dict*
#     configuration = resource.Body('configuration', type=dict)
#
#
# class Parameter(sdk_resource.Resource):
#     # TODO(agoncharov) most likely useless
#
#     base_path = '/%(project_id)s/datastores/versions/'
#     '%(datastore_version_id)s/parameters/'
#     resources_key = 'configuration-parameters'
#     service = rds_service.RdsService()
#
#     # capabilities
#     allow_list = True
#     allow_get = True
#
#     # Properties
#     #: Parameter name
#     name = resource.Body('name', alternate_id=True)
#     #: Minimum value of the parameter
#     #: *Type: int*
#     min = resource.Body('min', type=int)
#     #: Maximum value of the parameter
#     #: *Type: int*
#     max = resource.Body('max', type=int)
#     #: Parameter type
#     type = resource.Body('type')
#     #: Value range
#     value_range = resource.Body('value_range')
#     #: Description
#     description = resource.Body('description')
#     #: Require restart or not
#     #: *Type: bool*
#     restart_required = resource.Body('restart_required', type=bool)
#     #: Datastore version id
#     datastore_version_id = resource.Body('datastore_version_id')


class ConfigurationGroup(sdk_resource.Resource):

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
    project_id = resource.URI('project_id')
    #: Id of the configuration group
    #: *Type:str*
    id = resource.Body('id')
    #: Name of the configuration group
    #: *Type:str*
    name = resource.Body('name')
    #: Description of the configuration group
    #: *Type:str*
    description = resource.Body('description')
    #: Id of Datastore version
    #: *Type:str*
    datastore_version_id = resource.Body('datastore_version_id')
    #: name of Datastore version
    #: *Type:str*
    datastore_version_name = resource.Body('datastore_version_name')
    #: name of Datastore
    #: *Type:str*
    datastore_name = resource.Body('datastore_name')
    #: Date of created
    #: *Type:str*
    created = resource.Body('created')
    #: Date of updated
    #: *Type:str*
    updated = resource.Body('updated')
    # : Allow update or not, 0 for not allowed
    # : *Type:int*
    # allowed_updated = resource.Body('allowed_updated', type=int)
    #: Count of associated instance
    #: *Type:int*
    instance_count = resource.Body('instance_count', type=int)
    #: Params values
    #: *Type:dict*
    values = resource.Body('values', type=dict)
    #: Parameter list
    #: *Type:dict*
    parameters = resource.Body('parameters', type=list)
    #: Datastore dict
    #: *Type:dict*
    datastore = resource.Body('datastore', type=dict)

    def get_associated_instances(self, session, endpoint_override=None):
        """Get associated instancs

        :param session: session (adapter)
        :param endpoint_override: optional endpoint_override

        :returns: list of instance id/name dicts with instances
            with this configuration group
        :rtype: list of dicts
        """

        request = self._prepare_request()
        session = self._get_session(session)

        if not endpoint_override:
            if getattr(self, 'endpoint_override', None):
                # If we have internal endpoint_override - use it
                endpoint_override = self.endpoint_override

        # Build additional arguments to the DELETE call
        args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            additional_headers={'Content-Type': 'application/json'}
        )

        # URL is a subpoin
        url = utils.urljoin(request.url, 'instances')

        resp = session.get(url, **args)
        resp = resp.json()

        if resp:
            return resp['instances']

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data

        'DELETE' operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body
        # exceptions.raise_from_response(response, error_message=error_message)
        if has_body:
            body = response.json()

            errCode = body.get('errCode', None)
            if errCode and errCode == 'RDS.0041':
                if self.resource_key and self.resource_key in body:
                    body = body[self.resource_key]

                body = self._consume_body_attrs(body)
                self._body.attributes.update(body)
                self._body.clean()
            elif errCode and errCode == 'RDS.0028':
                raise exceptions.NotFoundException('Resource not found')
            elif errCode and errCode != 'RDS.0041':
                _logger.error('error during service invokation %s' % errCode)
                raise exceptions.SDKException(
                    body.get('externalMessage', body)
                )
            elif not errCode:
                if self.resource_key and self.resource_key in body:
                    body = body[self.resource_key]

                body = self._consume_body_attrs(body)
                self._body.attributes.update(body)
                self._body.clean()

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
