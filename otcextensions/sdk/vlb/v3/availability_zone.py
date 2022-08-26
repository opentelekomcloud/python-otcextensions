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


class AvailabilityZone(resource.Resource):
    base_path = '/elb/availability-zones'

    # capabilities
    allow_list = True

    # Properties
    #: Specifies the AZ code.
    code = resource.Body('code', type=str)
    #: Specifies the AZ status.
    state = resource.Body('state', type=str)

    @classmethod
    def list(cls, session, paginated=True, base_path=None,
             allow_unknown_params=False, **params):

        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        session = cls._get_session(session)
        microversion = cls._get_microversion(session, action='list')

        if base_path is None:
            base_path = cls.base_path

        response = session.get(
            base_path,
            headers={"Accept": "application/json"},
            microversion=microversion)
        exceptions.raise_from_response(response)
        data = response.json()

        resources = data['availability_zones']

        if not isinstance(resources, list):
            resources = [resources]

        for raw_resource in resources[0]:
            value = cls.existing(
                microversion=microversion,
                connection=session._get_connection(),
                **raw_resource)
            yield value
