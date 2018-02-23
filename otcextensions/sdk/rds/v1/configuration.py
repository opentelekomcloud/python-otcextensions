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
from openstack import utils

from otcextensions.sdk.rds import rds_service

from otcextensions.sdk import sdk_resource


_logger = _log.setup_logging('openstack')


class InstanceConfiguration(sdk_resource.Resource):
    # TODO(agoncharov) most likely useless

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


class Parameter(sdk_resource.Resource):
    # TODO(agoncharov) most likely useless

    base_path = '/%(project_id)s/datastores/versions/'
    '%(datastore_version_id)s/parameters/'
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


class ParameterGroup(sdk_resource.Resource):

    base_path = '/%(project_id)s/configurations'
    resource_key = 'configuration'
    resources_key = 'configurations'
    service = rds_service.RdsService()

    # capabilities
    allow_create = True
    allow_delete = True
    allow_update = False
    allow_get = True
    allow_list = True

    # Properties
    project_id = resource.URI('project_id')
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
    parameters = resource.Body('parameters', type=list)
    #: Datastore dict
    #: *Type:dict*
    datastore = resource.Body('datastore', type=dict)

    def get_associated_instances(self, session, endpoint_override=None):
        """Get associated instancs

        :param session: session (adapter)
        :param endpoint_override: optional endpoint_override

        :returns list of instance id/name dicts with instances
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
            additional_headers={"Content-Type": "application/json"}
        )

        # URL is a subpoin
        url = utils.urljoin(request.url, 'instances')

        resp = session.get(url, **args)
        resp = resp.json()

        if resp:
            return resp['instances']

    def add_custom_parameter(self, session, endpoint_override=None, **attrs):
        """Add a custom parameter into the ConfigurationGroup

        :param session: session (adapter)
        :param endpoint_override: optional endpoint_override
        :param **attrs: dict with parameter key/value

        :returns RDS response if not success otherwise updated group
        :rtype: modified ConfigurationGroup
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
            # additional_headers={"Content-Type": "application/json"}
        )

        body = {
            "configuration": {
                "values": attrs
            }
        }

        response = session.patch(
            request.url, json=body, **args)

        resp = response.json()
        if resp:
            errCode = resp.get('errCode', None)
            if errCode and errCode == 'RDS.0041':
                self._body.attributes.update({"values": attrs})
                self._body.clean()
                return self

        return resp

    def change_parameter_info(self, session, endpoint_override=None, **attrs):
        """Add a custom parameter into the ConfigurationGroup

        :param session: session (adapter)
        :param endpoint_override: optional endpoint_override
        :param **attrs: dict with the parameter description structure
            (name, description, values[])

        :returns RDS response
        :rtype: modified ConfigurationGroup
        """
        request = self._prepare_request()
        session = self._get_session(session)

        if not endpoint_override:
            if getattr(self, 'endpoint_override', None):
                # If we have internal endpoint_override - use it
                endpoint_override = self.endpoint_override

        # Build additional arguments to the PUT call
        args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            # additional_headers={"Content-Type": "application/json"}
        )

        body = {
            "configuration": attrs
        }

        response = session.put(
            request.url, json=body, **args)

        resp = response.json()
        if resp:
            errCode = resp.get('errCode', None)
            if errCode and errCode == 'RDS.0041':
                self._body.attributes.update({"values": attrs})
                self._body.clean()
                return self

        return resp
