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


class LocalNameSpec(resource.Resource):
    en_us = resource.Body('en_us')
    zh_cn = resource.Body('zh_cn')


class AZ(resource.Resource):
    resource_name = 'AZ'
    resources_key = 'available_zones'
    base_path = '/apigw/available-zones'

    allow_list = True

    name = resource.Body('name')
    id = resource.Body('id')
    code = resource.Body('code')
    port = resource.Body('port')
    local_name = resource.Body('local_name', type=LocalNameSpec)
    specs = resource.Body('specs', type=dict)
