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


class Datastore(resource.Resource):
    base_path = '/datastores'

    # capabilities
    allow_list = True

    datastore_name = resource.URI('datastore_name')

    #: Storage engine
    storage_engine = resource.Body('storage_engine')
    #: Datastore type
    type = resource.Body('type')
    # Indicates the database version.
    # :*Type:string*
    version = resource.Body('version')

    @classmethod
    def list(cls, session, paginated=True, base_path=None,
             allow_unknown_params=False, **params):

        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        session = cls._get_session(session)
        microversion = cls._get_microversion(session)

        if base_path is None:
            base_path = cls.base_path

        datastore_type = params.get('datastore_name', 'DDS-Community')
        uri = utils.urljoin(
            base_path,
            datastore_type,
            'versions'
        )

        response = session.get(
            uri,
            headers={"Accept": "application/json"},
            microversion=microversion)
        exceptions.raise_from_response(response)
        data = response.json()

        resources = data['versions']

        if not isinstance(resources, list):
            resources = [resources]

        for raw_resource in resources:
            value = cls.existing(
                microversion=microversion,
                connection=session._get_connection(),
                type=datastore_type,
                storage_engine='wiredTiger',
                version=raw_resource)
            yield value
