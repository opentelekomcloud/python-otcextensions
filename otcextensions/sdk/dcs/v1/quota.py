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
from otcextensions.sdk import quotamixin


class Quota(quotamixin.QuotaProxyMixin, resource.Resource):
    """Distributed Cache Service Quota resource"""
    resources_key = 'quotas.resources'
    base_path = '/quota'

    # capabilities
    allow_list = True

    #: Properties
    #: Quota type, value is ``instance`` or ``ram``
    type = resource.Body('type')
    #: Quota amount of created instances and used memory
    used = resource.Body('used', type=int)
    #: Quota amount
    quota = resource.Body('quota', type=int)
    #: Resource unit, when ``type`` is set to ``ram`` ``GB`` is returned
    unit = resource.Body('unit')
    #: Max limit of instance or memory quota
    max = resource.Body('max', type=int)
    #: Min limit of instance or memory quota
    min = resource.Body('min', type=int)
