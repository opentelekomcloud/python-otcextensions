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

    @staticmethod
    def find_value_by_accessor(input_dict, accessor):
        """Gets value from a dictionary using a dotted accessor"""
        current_data = input_dict
        for chunk in accessor.split('.'):
            if isinstance(current_data, dict):
                current_data = current_data.get(chunk, {})
            else:
                return None
        return current_data

    @classmethod
    def list(cls, session, paginated=False,
             base_path=None, **params):
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        session = cls._get_session(session)

        # pop scaling_group_id, as it should not be also present in the query
        scaling_group_id = params.pop('scaling_group_id', None)
        uri_params = {}

        if scaling_group_id:
            uri_params = {'scaling_group_id': scaling_group_id}

        cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params, cls)
        uri = cls.base_path % uri_params

        limit = query_params.get('limit')

        total_yielded = 0
        while uri:
            response = session.get(
                uri,
                params=query_params.copy()
            )
            exceptions.raise_from_response(response)
            data = response.json()

            # Discard any existing pagination keys
            query_params.pop('marker', None)
            query_params.pop('limit', None)

            if cls.resources_key:
                resources = cls.find_value_by_accessor(data, cls.resources_key)
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            marker = None
            for raw_resource in resources:
                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                raw_resource.pop("self", None)

                if cls.resource_key and cls.resource_key in raw_resource:
                    raw_resource = raw_resource[cls.resource_key]

                value = cls.existing(**raw_resource)

                marker = value.id
                yield value
                total_yielded += 1

            if resources and paginated:
                uri, next_params = cls._get_next_link(
                    uri, response, data, marker, limit, total_yielded)
                query_params.update(next_params)
            else:
                return


class ScalingQuota(Quota):
    base_path = '/quotas/%(scaling_group_id)s'

    scaling_group_id = resource.URI('scaling_group_id')
