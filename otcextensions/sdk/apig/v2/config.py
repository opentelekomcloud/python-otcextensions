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


class Config(resource.Resource):
    base_path = '/apigw/instance/configs'
    resources_key = 'configs'
    allow_list = True

    # Properties

    #: The ID of the configuration item.
    config_id = resource.Body('config_id')
    #: The name of the configuration item.
    config_name = resource.Body('config_name')
    #: The value of the configuration item.
    config_value = resource.Body('config_value')
    #: The time when the configuration item was created.
    config_time = resource.Body('config_time')
    #: The time when the configuration item was last updated.
    remark = resource.Body('remark')
    #: Used quota of the gateway.
    used = resource.Body('used')
