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


class FlavorsSpec(resource.Resource):
    # Properties
    #: Indicates the engine name.
    engine_name = resource.Body('engine_name')
    #: Indicates the node type. DDS contains the following types of nodes:
    # mongos
    # shard
    # config
    # replica
    type = resource.Body('type')
    #: Number of vCPUs.
    vcpus = resource.Body('vcpus')
    #: Indicates the memory size in gigabyte (GB).
    ram = resource.Body('ram')
    #: Indicates the resource specifications code.
    spec_code = resource.Body('spec_code')
    #: Indicates the status of specifications in an AZ.
    az_status = resource.Body('az_status')


class Flavor(resource.Resource):
    base_path = '/flavors'

    # capabilities
    allow_list = True

    region = resource.URI('region')
    #: Storage engine
    engine_name = resource.URI('engine_name')

    # Properties
    #: specification
    flavors = resource.Body('flavors', type=FlavorsSpec)

    @classmethod
    def list(cls, session, paginated=True, base_path=None,
             allow_unknown_params=False, **params):

        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        session = cls._get_session(session)
        microversion = cls._get_microversion_for_list(session)

        if base_path is None:
            base_path = cls.base_path

        query_params = {
            'region': params.get('region', 'eu-de'),
            'engine_name': params.get('engine_name', 'DDS-Community')
        }

        response = session.get(
            base_path,
            headers={"Accept": "application/json"},
            params=query_params,
            microversion=microversion)
        exceptions.raise_from_response(response)
        resources = response.json()

        if not isinstance(resources, list):
            resources = [resources]

        for raw_resource in resources:
            value = cls.existing(
                microversion=microversion,
                connection=session._get_connection(),
                **raw_resource)
            yield value
