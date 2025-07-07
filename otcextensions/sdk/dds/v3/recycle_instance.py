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

from otcextensions.sdk.dds.v3.instance import DatastoreSpec


class RecycleInstanceSpec(resource.Resource):
    id = resource.Body('id')
    name = resource.Body('name')
    mode = resource.Body('mode')
    datastore = resource.Body('datastore', type=DatastoreSpec)
    pay_mode = resource.Body('pay_mode')
    enterprise_project_id = resource.Body('enterprise_project_id')
    backup_id = resource.Body('backup_id')
    created_at = resource.Body('created_at')
    deleted_at = resource.Body('deleted_at')
    retained_until = resource.Body('retained_until')
    status = resource.Body('status')


class RecycleInstance(resource.Resource):
    base_path = '/recycle-instances'

    allow_list = True
    requires_id = False
    total_count = resource.Body('total_count', type=int)
    instances = resource.Body('instances', type=list,
                              list_type=RecycleInstanceSpec)

    @classmethod
    def list(cls, session, paginated=True, base_path=None, **params):
        session = cls._get_session(session)
        microversion = cls._get_microversion(session)
        response = session.get(
            base_path,
            headers={"Content-Type": "application/json"},
            params={},
            microversion=microversion,
        )
        exceptions.raise_from_response(response)
        data = response.json()
        resources = data
        if not isinstance(resources, list):
            resources = [resources]

        for raw_resource in resources:
            raw_resource.pop('self', None)
            value = cls.existing(
                microversion=microversion,
                connection=session._get_connection(),
                **raw_resource,)
            yield value
        else:
            return
