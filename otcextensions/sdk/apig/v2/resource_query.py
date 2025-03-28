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


class ApiQuantities(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/resources/outline/apis'

    allow_fetch = True

    # Properties
    gateway_id = resource.URI('gateway_id')

    # Attributes
    # Total number of APIs.
    apis_num = resource.Body('instance_num', type=int)
    # Number of APIs that have been published in the RELEASE environment.
    apis_in_release = resource.Body('nums_on_release', type=int)
    # Number of APIs that have not been published in the RELEASE environment.
    apis_not_in_release = resource.Body('nums_off_release', type=int)


class ApiGroupQuantities(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/resources/outline/groups'

    allow_fetch = True

    # Properties
    gateway_id = resource.URI('gateway_id')

    # Attributes
    # Number of API groups that have not been listed on KooGallery.
    not_in_koogallery = resource.Body('offsell_nums', type=int)
    # Number of API groups that have been listed on KooGallery.
    in_koogallery = resource.Body('onsell_nums', type=int)


class AppQuantities(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/resources/outline/apps'

    allow_fetch = True

    # Properties
    gateway_id = resource.URI('gateway_id')

    # Attributes
    # Number of apps that have been authorized to access APIs.
    authorized = resource.Body('authed_nums', type=int)
    # Number of apps that have not been authorized to access APIs.
    not_authorized = resource.Body('unauthed_nums', type=int)
