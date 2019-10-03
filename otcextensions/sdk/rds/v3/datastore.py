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
from otcextensions.sdk import sdk_resource


class Datastore(sdk_resource.Resource):

    base_path = '/datastores/%(datastore_name)s'
    resources_key = 'dataStores'

    # capabilities
    allow_list = True

    datastore_name = resource.URI('datastore_name')

    # Indicates the database version ID. Its value is unique.
    # :*Type:string*
    id = resource.Body('id')
    # Indicates the database version.
    # :*Type:string*
    name = resource.Body('name')
