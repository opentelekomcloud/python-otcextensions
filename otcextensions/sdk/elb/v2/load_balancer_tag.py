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

from otcextensions.sdk.elb.v2 import _base_tag


class Tag(_base_tag.Resource):
    base_path = '/loadbalancers/%(loadbalancer_id)s/tags'

    # Properties
    #: Specifies load balancer
    loadbalancer_id = resource.URI('loadbalancer_id')
