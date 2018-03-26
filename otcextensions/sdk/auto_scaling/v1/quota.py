# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from openstack import resource

from otcextensions.sdk.auto_scaling.v1 import _base


class Quota(_base.Resource):
    """AutoScaling Quota resource"""
    resources_key = 'quotas.resources'
    base_path = '/quotas'

    # capabilities
    allow_list = True

    #: Properties
    #: Quota of type, current only ``alarm`` is valid
    type = resource.Body('type')
    #: Quota amount has been used
    used = resource.Body('used', type=int)
    #: Quota max amount
    max = resource.Body('max', type=int)
    #: Quota amount
    quota = resource.Body('quota', type=int)

    @classmethod
    def list(cls, session, paginated=False,
             endpoint_override=None, headers=None, **params):
        return super(Quota, cls).list_ext(
            session, paginated,
            endpoint_override, headers,
            **params)


class ScalingQuota(Quota):
    base_path = '/quotas/%(scaling_group_id)s'

    scaling_group_id = resource.URI('scaling_group_id')
